#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

# Check dependencies
if ! python3 -c "import PyQt6" 2>/dev/null && ! python3 -c "import PySide6" 2>/dev/null; then
    echo "Installazione dipendenze PyQt6..."
    pip install -r requirements.txt
fi

SCRIPT_PATH="$DIR/smart_disk_info.py"

# If pkexec is available and not running as root and no --no-root / --demo arg passed
if [ "$EUID" -ne 0 ] && [ "$1" != "--no-root" ] && [ "$1" != "--demo" ]; then
    if command -v pkexec >/dev/null 2>&1 && [ -n "$DISPLAY" ]; then
        echo "Avvio con elevazione privilegi root tramite pkexec per accesso completo a smartctl..."
        pkexec env DISPLAY="$DISPLAY" XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}" WAYLAND_DISPLAY="$WAYLAND_DISPLAY" PYTHONPATH="$DIR" python3 "$SCRIPT_PATH" --no-root "$@"
        exit $?
    fi
fi

python3 "$SCRIPT_PATH" "$@"
