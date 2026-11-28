"""User-file transactions. Each revision records both sides before any target changes."""
import base64
import contextlib
import fcntl
import json
import os
import stat
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAYLOAD = ROOT / "desktop"


def xdg(variable, fallback):
    path = Path(os.environ.get(variable) or Path.home() / fallback)
    if not path.is_absolute():
        raise ValueError(f"{variable} must be absolute")
    return path


def atomic(path, data, mode=0o600):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        tmp = Path(handle.name)
        try:
            handle.write(data)
            handle.flush()
            os.fchmod(handle.fileno(), mode)
            os.fsync(handle.fileno())
            os.replace(tmp, path)
        finally:
            tmp.unlink(missing_ok=True)


@contextlib.contextmanager
def locked(directory):
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    if directory.is_symlink() or directory.stat().st_uid != os.getuid() or directory.stat().st_mode & 0o077:
        raise ValueError(f"Expected private state directory: {directory}")
    with (directory / "lock").open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def outside_checkout(path):
    if path.resolve().is_relative_to(ROOT):
        raise ValueError(f"Deployment path is inside the repository: {path}")


def files():
    mapping = json.loads((PAYLOAD / "files.json").read_text())
    roots = {"config": xdg("XDG_CONFIG_HOME", ".config"),
             "data": xdg("XDG_DATA_HOME", ".local/share")}
    destinations = set()
    for source, (base, dest) in mapping.items():
        src = PAYLOAD / source
        if src.resolve() != src or not src.is_relative_to(PAYLOAD) or src.name.endswith(".example"):
            raise ValueError(f"Invalid deployment source: {source}")
        root = roots[base].resolve()
        target = root / dest
        if target == root or ".." in Path(dest).parts or Path(dest).is_absolute():
            raise ValueError(f"Invalid destination: {dest}")
        outside_checkout(target)
        if target in destinations:
            raise ValueError(f"Duplicate destination: {dest}")
        destinations.add(target)
        yield src, target


def snapshot(path):
    if path.parent.resolve() != path.parent or path.is_symlink():
        raise ValueError(f"Symlink conflict: {path}")
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError(f"Expected regular file: {path}")
    return [stat.S_IMODE(path.stat().st_mode), base64.b64encode(path.read_bytes()).decode()]


def restore(path, value):
    if value is None:
        path.unlink(missing_ok=True)
    else:
        atomic(path, base64.b64decode(value[1]), value[0])


def save(path, obj):
    atomic(path, json.dumps(obj).encode())


def run(args):
    state = xdg("XDG_STATE_HOME", ".local/state").resolve() / "dotfiles/deploy"
    journal = state / "history.json"
    outside_checkout(state)
    outside_checkout(journal)
    if journal.is_symlink():
        raise ValueError(f"Symlink conflict: {journal}")
    write = args.apply
    if write and os.geteuid() == 0:
        raise ValueError("Run deployment as your login user")
    mappings = list(files()) if args.action == "install" else []
    if write and args.action == "rollback":
        preview = json.loads(journal.read_text()) if journal.exists() else []
        if not preview:
            print("No deployment to restore.")
            return 0
        for name, _, _ in preview[-1]["files"]:
            outside_checkout(Path(name))
    with locked(state) if write else contextlib.nullcontext():
        history = json.loads(journal.read_text()) if journal.exists() else []
        last = history[-1] if history else None
        if args.action == "rollback":
            if not last:
                print("No deployment to restore.")
                return 0
            items = last["files"]
            for name, old, new in reversed(items):
                outside_checkout(Path(name))
                if snapshot(Path(name)) not in (old, new):
                    raise ValueError(f"Edited after deployment: {name}")
                print("Restore", name)
            if write:
                last["status"] = "rolling back"
                save(journal, history)
                for name, old, new in reversed(items):
                    target = Path(name)
                    current = snapshot(target)
                    if current == new:
                        restore(target, old)
                    elif current != old:
                        raise ValueError(f"Concurrent edit: {name}")
                save(journal, history[:-1])
            return 0
        if last and last["status"] != "complete":
            raise ValueError("Interrupted transaction. Run dotctl deploy rollback --apply first.")
        owned = {name: new for revision in history for name, _, new in revision["files"]}
        items = []
        for source, target in mappings:
            old, new = snapshot(target), snapshot(source)
            if new is None:
                raise ValueError(f"Missing source: {source}")
            if old == new:
                continue
            if old is not None and old != owned.get(str(target)) and not args.replace:
                raise ValueError(f"Conflict: {target} (review before using --replace)")
            items.append([str(target), old, new])
            print("Write", target)
        if not items:
            print("All selected files match.")
        if items and write:
            revision = {"status": "applying", "files": []}
            history.append(revision)
            for name, old, new in items:
                target = Path(name)
                if snapshot(target) != old:
                    raise ValueError(f"Concurrent edit: {name}")
                # An unattempted destination must never block recovery of earlier writes.
                revision["files"].append([name, old, new])
                save(journal, history)
                restore(target, new)
            revision["status"] = "complete"
            save(journal, history)
    return 0
