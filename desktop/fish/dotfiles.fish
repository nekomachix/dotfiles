if status is-interactive; and not set -q STARSHIP_SHELL; and type -q starship
    starship init fish | source
end
