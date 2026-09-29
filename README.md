# S.M.A.R.T disk controller

Lightweight Python and Qt GUI for smartctl on Linux. It monitors drive health (NVMe, SATA SSD, and mechanical HDD), calculates estimated remaining life percentage, and cleanly displays SMART attributes. Supports English, Italian, and Russian out of the box.

---

### Features

- Calculates estimated remaining life percentage (NVMe via Percentage Used and available spare, SATA SSD via flash wearout indicators, HDD via reallocated/pending sectors).
- Automatically detects drive type (NVMe PCIe, SATA SSD, or Mechanical HDD).
- Clean S.M.A.R.T. attributes table with readable names, descriptions, and toggle for decimal/hexadecimal raw values.
- Automatically hides unused normalized columns (Current/Worst/Threshold) on NVMe drives to keep the view clean.
- Native Qt desktop integration (no custom themes or forced styling; adopts your desktop palette).
- Multi-language support with on-the-fly switching from the menu bar (English default, Italian, Russian).
- Root privilege escalation prompt via `pkexec` at startup to allow direct access to disk controllers without having to launch the entire desktop session as root.
- Export health reports to plain text (.txt) or JSON format.

---

### Requirements

- Linux
- Python 3.10 or higher
- `smartmontools` (`smartctl`)
- `PyQt6` (or `PySide6`)
- `pkexec` (standard on most Linux desktop distributions for authentication prompts)

---

### Installation

On Debian / Ubuntu:
```bash
sudo apt update && sudo apt install smartmontools python3-pyqt6
```

On Arch Linux / Manjaro:
```bash
sudo pacman -S smartmontools python-pyqt6
```

On Fedora:
```bash
sudo dnf install smartmontools python3-pyqt6
```

Python dependencies (alternative via pip):
```bash
pip install -r requirements.txt
```

---

### Usage

Make the launcher executable and run:
```bash
chmod +x run.sh
./run.sh
```

Or run directly with Python:
```bash
python3 smart_disk_info.py
```

To run in simulation / demo mode (useful for testing without physical drives or inside virtual machines):
```bash
python3 smart_disk_info.py --demo
```

---

### License

No license.
Contributions, issues, and pull requests are welcome.

---

### Credits

Developed in collaboration with Antigravity.
