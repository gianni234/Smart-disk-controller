#!/usr/bin/env python3
import sys
import os
import shutil
import subprocess
import argparse

try:
    from PyQt6.QtWidgets import QApplication, QMessageBox
    from PyQt6.QtCore import Qt
except ImportError:
    try:
        from PySide6.QtWidgets import QApplication, QMessageBox
        from PySide6.QtCore import Qt
    except ImportError:
        print("Errore: PyQt6 o PySide6 non trovato. Installa le dipendenze con: pip install PyQt6")
        sys.exit(1)

from ui.main_window import MainWindow


def parse_args():
    parser = argparse.ArgumentParser(
        description="smart disk controller by gianni234"
    )
    parser.add_argument(
        "--demo", action="store_true", help="Avvia l'applicazione in modalità Demo (Simulazione)"
    )
    parser.add_argument(
        "--no-root", action="store_true", help="Non richiedere l'elevazione a root all'avvio"
    )
    return parser.parse_args()


def try_elevate_root():
    if os.geteuid() == 0:
        return True

    pkexec = shutil.which("pkexec")
    if pkexec:
        display = os.environ.get("DISPLAY", ":0")
        xauth = os.environ.get("XAUTHORITY", os.path.expanduser("~/.Xauthority"))
        wayland_display = os.environ.get("WAYLAND_DISPLAY", "")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.abspath(__file__)

        env_args = [
            "env",
            f"DISPLAY={display}",
            f"XAUTHORITY={xauth}",
            f"PYTHONPATH={script_dir}",
        ]
        if wayland_display:
            env_args.append(f"WAYLAND_DISPLAY={wayland_display}")

        cmd = [pkexec] + env_args + [sys.executable, script_path, "--no-root"] + sys.argv[1:]
        try:
            res = subprocess.run(cmd)
            if res.returncode == 0:
                sys.exit(0)
        except Exception:
            pass

    return False


def main():
    args = parse_args()

    if not args.demo and not args.no_root and os.geteuid() != 0:
        if shutil.which("pkexec") and os.environ.get("DISPLAY"):
            try_elevate_root()

    if hasattr(Qt.ApplicationAttribute, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("smart disk controller by gianni234")
    app.setApplicationDisplayName("smart disk controller by gianni234")

    window = MainWindow()
    if args.demo:
        window.act_demo.setChecked(True)
        window.is_demo_mode = True
        window.refresh_disks()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
