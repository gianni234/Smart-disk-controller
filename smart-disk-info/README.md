# smart disk controller by gianni234

Interfaccia grafica leggera in Python e Qt per smartctl su Linux. Mostra lo stato di salute dei dischi (NVMe, SATA SSD e HDD), calcola la percentuale di vita residua e visualizza i parametri SMART in modo pulito. Supporta inglese, italiano e russo. Richiede Python 3, smartmontools e PyQt6.

### Requisiti

- Linux
- Python 3.10+
- smartmontools (`smartctl`)
- PyQt6 (o PySide6)
- pkexec (per la lettura dei dati SMART dai dispositivi fisici)

### Installazione

Su Debian / Ubuntu:
```bash
sudo apt update && sudo apt install smartmontools python3-pyqt6
```

Su Arch Linux / Manjaro:
```bash
sudo pacman -S smartmontools python-pyqt6
```

Su Fedora:
```bash
sudo dnf install smartmontools python3-pyqt6
```

Dipendenze Python (alternativa con pip):
```bash
pip install -r requirements.txt
```

### Avvio

```bash
chmod +x run.sh
./run.sh
```

Oppure direttamente con Python:
```bash
python3 smart_disk_info.py
```

Per eseguire in modalità simulazione / demo senza accesso ai dischi fisici:
```bash
python3 smart_disk_info.py --demo
```
