import subprocess
import json
import os
import shutil
from typing import List, Optional, Dict, Any, Tuple
from models import DiskInfo, SmartAttribute
from smart_attributes_db import get_attribute_info


def format_bytes(num_bytes: Optional[int]) -> str:
    if num_bytes is None or num_bytes < 0:
        return "N/D"
    if num_bytes == 0:
        return "0 GB"

    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    val = float(num_bytes)
    unit_idx = 0
    while val >= 1024.0 and unit_idx < len(units) - 1:
        val /= 1024.0
        unit_idx += 1

    if unit_idx >= 3:
        return f"{val:.2f} {units[unit_idx]}"
    return f"{int(val)} {units[unit_idx]}"


def format_hours(hours: Optional[int]) -> str:
    if hours is None:
        return "N/D"
    if hours < 24:
        return f"{hours} ore"
    days = hours // 24
    rem_hours = hours % 24
    if days < 365:
        return f"{days} giorni, {rem_hours} ore ({hours:,} ore)"
    years = days / 365.25
    return f"{years:.1f} anni ({days:,} giorni - {hours:,} ore)"


class DiskScanner:
    def __init__(self):
        self.smartctl_path = shutil.which("smartctl") or "/usr/bin/smartctl"
        self.has_smartctl = os.path.exists(self.smartctl_path)

    def run_smartctl_command(self, args: List[str], use_root: bool = False) -> Tuple[int, str, str]:
        cmd = []
        if use_root and os.geteuid() != 0:
            if shutil.which("pkexec"):
                cmd.extend(["pkexec", self.smartctl_path])
            elif shutil.which("sudo"):
                cmd.extend(["sudo", "-n", self.smartctl_path])
            else:
                cmd.append(self.smartctl_path)
        else:
            cmd.append(self.smartctl_path)

        cmd.extend(args)

        try:
            res = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=15
            )
            return res.returncode, res.stdout, res.stderr
        except Exception as e:
            return -1, "", str(e)

    def scan_devices(self, use_root: bool = False) -> List[str]:
        devices = []

        if self.has_smartctl:
            code, out, _ = self.run_smartctl_command(["--scan", "--json"], use_root=use_root)
            if out.strip():
                try:
                    data = json.loads(out)
                    for dev in data.get("devices", []):
                        dev_name = dev.get("name")
                        if dev_name and dev_name not in devices:
                            devices.append(dev_name)
                except Exception:
                    pass

        if not devices and os.path.exists("/sys/block"):
            for dev in os.listdir("/sys/block"):
                if dev.startswith(("loop", "ram", "zram", "dm-", "sr", "md")):
                    continue
                dev_path = f"/dev/{dev}"
                if os.path.exists(dev_path):
                    devices.append(dev_path)

        return sorted(devices)

    def get_disk_info(self, device_path: str, use_root: bool = False) -> DiskInfo:
        code, stdout, stderr = self.run_smartctl_command(["-x", "--json", device_path], use_root=use_root)

        disk = DiskInfo(device_path=device_path)

        if not stdout.strip():
            disk.error_message = f"Impossibile leggere il dispositivo ({stderr or 'Nessun dato restituito'}). Potrebbero essere necessari i privilegi di root."
            return disk

        try:
            data = json.loads(stdout)
            disk.raw_json = data

            messages = data.get("messages", [])
            for msg in messages:
                if "Permission denied" in msg.get("string", ""):
                    disk.error_message = "Permesso negato: avvia l'app come root o usa pkexec per accedere ai dati SMART."

            self._parse_smart_json(disk, data)
        except Exception as e:
            disk.error_message = f"Errore durante il parsing SMART: {str(e)}"

        return disk

    def _parse_smart_json(self, disk: DiskInfo, data: Dict[str, Any]):
        dev_info = data.get("device", {})
        disk.protocol = dev_info.get("protocol", "SATA")
        disk.interface_type = dev_info.get("type", disk.protocol).upper()

        disk.model_name = (
            data.get("model_name") or 
            data.get("device_model") or 
            dev_info.get("model_name") or 
            data.get("scsi_model_name") or 
            "Dispositivo di archiviazione"
        )
        disk.serial_number = data.get("serial_number", "N/D")
        disk.firmware = data.get("firmware_version", "N/D")

        ff = data.get("form_factor", {})
        if isinstance(ff, dict):
            disk.form_factor = ff.get("name", "N/D")
        elif isinstance(ff, str):
            disk.form_factor = ff

        user_cap = data.get("user_capacity", {})
        disk.capacity_bytes = user_cap.get("bytes", 0)
        disk.capacity_str = format_bytes(disk.capacity_bytes)

        rotation = data.get("rotation_rate", 0)
        if rotation == 0 or "NVMe" in disk.protocol or "nvme" in disk.device_path:
            disk.is_ssd = True
            disk.rotation_rate = "SSD (Solid State Drive)"
        else:
            disk.is_ssd = False
            disk.rotation_rate = f"{rotation} RPM (HDD Meccanico)"

        temp = data.get("temperature", {})
        disk.temperature_c = temp.get("current")
        if disk.temperature_c is None:
            nvme_log = data.get("nvme_smart_health_information_log", {})
            disk.temperature_c = nvme_log.get("temperature")

        smart_stat = data.get("smart_status", {})
        disk.smart_passed = smart_stat.get("passed", True)

        poh = data.get("power_on_time", {})
        disk.power_on_hours = poh.get("hours")
        if disk.power_on_hours is not None:
            disk.power_on_hours_str = format_hours(disk.power_on_hours)

        p_cycle = data.get("power_cycle_count")
        if p_cycle is not None:
            disk.power_cycles = p_cycle

        if "nvme_smart_health_information_log" in data:
            self._parse_nvme_health(disk, data["nvme_smart_health_information_log"])
        elif "ata_smart_attributes" in data:
            self._parse_ata_attributes(disk, data["ata_smart_attributes"])
        elif "scsi_error_counter_log" in data:
            self._parse_scsi_health(disk, data)
        else:
            self._evaluate_generic_health(disk)

    def _parse_nvme_health(self, disk: DiskInfo, log: Dict[str, Any]):
        disk.interface_type = "NVMe"
        disk.is_ssd = True

        pct_used = log.get("percentage_used")
        if pct_used is not None:
            remaining = max(0, 100 - pct_used)
            disk.remaining_life_percent = remaining

        disk.available_spare = log.get("available_spare")
        disk.available_spare_threshold = log.get("available_spare_threshold")
        disk.unsafe_shutdowns = log.get("unsafe_shutdowns")
        disk.media_errors = log.get("media_errors")

        if disk.power_on_hours is None and "power_on_hours" in log:
            disk.power_on_hours = log["power_on_hours"]
            disk.power_on_hours_str = format_hours(disk.power_on_hours)

        if disk.power_cycles is None and "power_cycles" in log:
            disk.power_cycles = log["power_cycles"]

        read_units = log.get("data_units_read")
        if read_units is not None:
            disk.total_bytes_read = read_units * 1000 * 512
            disk.total_read_str = format_bytes(disk.total_bytes_read)

        written_units = log.get("data_units_written")
        if written_units is not None:
            disk.total_bytes_written = written_units * 1000 * 512
            disk.total_written_str = format_bytes(disk.total_bytes_written)

        nvme_fields = [
            ("Critical Warning", log.get("critical_warning", 0), "Avvisi di sistema critici"),
            ("Composite Temperature", disk.temperature_c, f"Temperatura del controller e memoria: {disk.temperature_c}°C" if disk.temperature_c else "Temperatura"),
            ("Available Spare", disk.available_spare, "Percentuale di blocchi di riserva disponibili"),
            ("Available Spare Threshold", disk.available_spare_threshold, "Soglia minima di blocchi di riserva"),
            ("Percentage Used", pct_used, f"Percentuale di vita stimata consumata: {pct_used}%"),
            ("Data Units Read", read_units, f"Totale letto dall'host: {disk.total_read_str}"),
            ("Data Units Written", written_units, f"Totale scritto dall'host: {disk.total_written_str}"),
            ("Host Read Commands", log.get("host_reads"), "Numero totale di comandi di lettura ricevuti"),
            ("Host Write Commands", log.get("host_writes"), "Numero totale di comandi di scrittura ricevuti"),
            ("Controller Busy Time", log.get("controller_busy_time"), "Minuti in cui il controller era occupato"),
            ("Power Cycles", disk.power_cycles, "Cicli di accensione e spegnimento del dispositivo"),
            ("Power On Hours", disk.power_on_hours, f"Ore totali di funzionamento: {disk.power_on_hours_str}"),
            ("Unsafe Shutdowns", disk.unsafe_shutdowns, "Numero di spegnimenti improvvisi non sicuri"),
            ("Media and Data Errors", disk.media_errors, "Errori di integrità del supporto e recupero ECC"),
            ("Error Log Entries", log.get("num_err_log_entries"), "Numero di voci registrate nel log errori"),
        ]

        attr_list = []
        for idx, (name, val, desc) in enumerate(nvme_fields, 1):
            if val is not None:
                status = "OK"
                if name == "Critical Warning" and val != 0:
                    status = "FAIL"
                elif name == "Media and Data Errors" and val > 0:
                    status = "WARN"
                elif name == "Available Spare" and disk.available_spare_threshold and val <= disk.available_spare_threshold:
                    status = "WARN"

                attr_list.append(SmartAttribute(
                    id=idx,
                    name=name,
                    value=None,
                    worst=None,
                    threshold=None,
                    raw_value=val,
                    raw_string=f"{val:,}" if isinstance(val, int) else str(val),
                    status=status,
                    description=desc
                ))
        disk.attributes = attr_list
        self._calculate_health_badge(disk)

    def _parse_ata_attributes(self, disk: DiskInfo, ata_data: Dict[str, Any]):
        table = ata_data.get("table", [])
        attr_list = []

        life_percentages = []

        for item in table:
            attr_id = item.get("id", 0)
            name = item.get("name", f"Unknown Attribute {attr_id}")
            val = item.get("value")
            worst = item.get("worst")
            thresh = item.get("thresh")
            raw_data = item.get("raw", {})
            raw_val = raw_data.get("value", 0)
            raw_str = raw_data.get("string", str(raw_val))

            friendly_name, desc, category = get_attribute_info(attr_id, name)

            status = "OK"
            when_failed = item.get("when_failed")
            if when_failed and when_failed != "-":
                status = "FAIL"
            elif thresh is not None and val is not None and thresh > 0 and val <= thresh:
                status = "FAIL"
            elif category == "critical_if_high" and raw_val > 0:
                status = "WARN" if raw_val < 50 else "FAIL"

            if attr_id == 5:
                disk.reallocated_sectors = raw_val
            elif attr_id == 197:
                disk.pending_sectors = raw_val
            elif attr_id == 198:
                disk.uncorrectable_sectors = raw_val
            elif attr_id == 9 and disk.power_on_hours is None:
                disk.power_on_hours = raw_val
                disk.power_on_hours_str = format_hours(raw_val)
            elif attr_id == 12 and disk.power_cycles is None:
                disk.power_cycles = raw_val
            elif attr_id in (190, 194) and disk.temperature_c is None:
                disk.temperature_c = raw_val & 0xFF
            elif attr_id == 241:
                disk.total_bytes_written = raw_val * 512
                disk.total_written_str = format_bytes(disk.total_bytes_written)
            elif attr_id == 242:
                disk.total_bytes_read = raw_val * 512
                disk.total_read_str = format_bytes(disk.total_bytes_read)

            if attr_id in (231, 202, 169, 233, 173):
                if val is not None and 0 <= val <= 100:
                    life_percentages.append(val)
                elif 0 <= raw_val <= 100:
                    life_percentages.append(raw_val)
            elif attr_id == 177:
                if val is not None and 0 <= val <= 100:
                    life_percentages.append(val)

            attr_list.append(SmartAttribute(
                id=attr_id,
                name=friendly_name,
                value=val,
                worst=worst,
                threshold=thresh,
                raw_value=raw_val,
                raw_string=raw_str,
                status=status,
                description=desc,
                flags=item.get("flags", {})
            ))

        disk.attributes = attr_list

        if disk.is_ssd:
            if life_percentages:
                disk.remaining_life_percent = min(life_percentages)
            else:
                disk.remaining_life_percent = 99 if disk.smart_passed else 50
        else:
            disk.remaining_life_percent = self._calculate_hdd_health(disk)

        self._calculate_health_badge(disk)

    def _parse_scsi_health(self, disk: DiskInfo, data: Dict[str, Any]):
        disk.is_ssd = False
        disk.remaining_life_percent = 100 if disk.smart_passed else 40
        self._calculate_health_badge(disk)

    def _calculate_hdd_health(self, disk: DiskInfo) -> int:
        health = 100

        if disk.reallocated_sectors:
            health -= min(50, disk.reallocated_sectors * 5)
        if disk.pending_sectors:
            health -= min(40, disk.pending_sectors * 8)
        if disk.uncorrectable_sectors:
            health -= min(50, disk.uncorrectable_sectors * 10)

        if disk.power_on_hours and disk.power_on_hours > 30000:
            overage = (disk.power_on_hours - 30000) / 1000
            health -= min(20, int(overage * 0.8))

        if not disk.smart_passed:
            health = min(health, 20)

        return max(0, min(100, health))

    def _evaluate_generic_health(self, disk: DiskInfo):
        if disk.smart_passed:
            disk.remaining_life_percent = 100
            disk.health_status = "Buono"
            disk.health_color = "#10B981"
        else:
            disk.remaining_life_percent = 15
            disk.health_status = "Critico"
            disk.health_color = "#EF4444"

    def _calculate_health_badge(self, disk: DiskInfo):
        pct = disk.remaining_life_percent
        if pct is None:
            pct = 100 if disk.smart_passed else 0
            disk.remaining_life_percent = pct

        has_critical_error = (
            not disk.smart_passed or 
            (disk.reallocated_sectors and disk.reallocated_sectors > 100) or
            (disk.pending_sectors and disk.pending_sectors > 20) or
            (disk.media_errors and disk.media_errors > 10)
        )

        has_warnings = (
            (disk.reallocated_sectors and disk.reallocated_sectors > 0) or
            (disk.pending_sectors and disk.pending_sectors > 0) or
            (disk.media_errors and disk.media_errors > 0) or
            (disk.unsafe_shutdowns and disk.unsafe_shutdowns > 50)
        )

        if has_critical_error or pct < 15:
            disk.health_status = "Critico"
            disk.health_color = "#EF4444"
            disk.health_details = "Rischio imminente di perdita dati. Si consiglia il backup immediato e la sostituzione del disco."
        elif pct < 50 or (has_warnings and pct < 70):
            disk.health_status = "Attenzione"
            disk.health_color = "#F59E0B"
            disk.health_details = "Usura avanzata o anomalie riscontrate. Monitorare costantemente lo stato del disco."
        elif pct < 85:
            disk.health_status = "Buono"
            disk.health_color = "#3B82F6"
            disk.health_details = "Disco in buono stato con normale consumo da utilizzo."
        else:
            disk.health_status = "Ottimo"
            disk.health_color = "#10B981"
            disk.health_details = "Disco in condizioni eccellenti e piena efficienza operativa."


def get_mock_disks() -> List[DiskInfo]:

    nvme = DiskInfo(
        device_path="/dev/nvme0n1",
        model_name="Samsung SSD 990 PRO 2TB",
        serial_number="S73UNJ0W910248X",
        firmware="0B2QJXD7",
        interface_type="NVMe PCIe 4.0 x4",
        protocol="NVMe",
        capacity_bytes=2000398934016,
        capacity_str="1.82 TB (2000 GB)",
        is_ssd=True,
        rotation_rate="SSD (Solid State Drive)",
        form_factor="M.2 2280",
        smart_passed=True,
        remaining_life_percent=98,
        health_status="Ottimo",
        health_color="#10B981",
        health_details="Disco NVMe in perfette condizioni. 2% di usura totale registrata sulle celle V-NAND.",
        temperature_c=38,
        power_on_hours=2140,
        power_on_hours_str="89 giorni (2.140 ore)",
        power_cycles=412,
        total_bytes_written=32849204854784,
        total_written_str="29.88 TB",
        total_bytes_read=41284920485478,
        total_read_str="37.55 TB",
        unsafe_shutdowns=6,
        media_errors=0,
        available_spare=100,
        available_spare_threshold=10,
        mount_points=["/", "/home"]
    )

    nvme_attrs = [
        SmartAttribute(1, "Critical Warning", None, None, None, 0, "0x00", "OK", "Critical system warnings"),
        SmartAttribute(2, "Composite Temperature", None, None, None, 38, "38 °C", "OK", "Controller and NAND temperature"),
        SmartAttribute(3, "Available Spare", None, None, None, 100, "100%", "OK", "Available spare blocks"),
        SmartAttribute(4, "Available Spare Threshold", None, None, None, 10, "10%", "OK", "Spare threshold"),
        SmartAttribute(5, "Percentage Used", None, None, None, 2, "2%", "OK", "Percentage of life used"),
        SmartAttribute(6, "Data Units Read", None, None, None, 80634610, "37.55 TB", "OK", "Total data read"),
        SmartAttribute(7, "Data Units Written", None, None, None, 64158603, "29.88 TB", "OK", "Total data written"),
        SmartAttribute(8, "Host Read Commands", None, None, None, 452918392, "452,918,392", "OK", "Host read commands"),
        SmartAttribute(9, "Host Write Commands", None, None, None, 381920194, "381,920,194", "OK", "Host write commands"),
        SmartAttribute(10, "Controller Busy Time", None, None, None, 842, "842 min", "OK", "Controller busy time"),
        SmartAttribute(11, "Power Cycles", None, None, None, 412, "412", "OK", "Power cycles count"),
        SmartAttribute(12, "Power On Hours", None, None, None, 2140, "2,140 hrs", "OK", "Total power on hours"),
        SmartAttribute(13, "Unsafe Shutdowns", None, None, None, 6, "6", "OK", "Unsafe shutdowns count"),
        SmartAttribute(14, "Media and Data Errors", None, None, None, 0, "0", "OK", "Media integrity errors"),
        SmartAttribute(15, "Error Log Entries", None, None, None, 0, "0", "OK", "Error log entries count"),
    ]
    nvme.attributes = nvme_attrs

    sata_ssd = DiskInfo(
        device_path="/dev/sda",
        model_name="Crucial MX500 1TB 3D NAND",
        serial_number="2149E5D9183A",
        firmware="M3CR046",
        interface_type="SATA 6.0 Gb/s (SATA III)",
        protocol="SATA",
        capacity_bytes=1000204886016,
        capacity_str="931.51 GB (1000 GB)",
        is_ssd=True,
        rotation_rate="SSD (Solid State Drive)",
        form_factor="2.5 inch",
        smart_passed=True,
        remaining_life_percent=76,
        health_status="Buono",
        health_color="#3B82F6",
        health_details="SSD SATA in ottimo stato. 76% di vita utile rimanente, nessun blocco riallocato.",
        temperature_c=31,
        power_on_hours=14820,
        power_on_hours_str="1.7 anni (617 giorni - 14.820 ore)",
        power_cycles=1280,
        total_bytes_written=85928192847120,
        total_written_str="78.15 TB",
        total_bytes_read=94819201948210,
        total_read_str="86.23 TB",
        reallocated_sectors=0,
        pending_sectors=0,
        uncorrectable_sectors=0,
        mount_points=["/mnt/storage"]
    )

    sata_attrs = [
        SmartAttribute(1, "Raw Read Error Rate", 100, 100, 0, 0, "0x000000000000", "OK", "Errori di lettura hardware"),
        SmartAttribute(5, "Reallocated Sectors Count", 100, 100, 10, 0, "0", "OK", "Settori danneggiati riallocati"),
        SmartAttribute(9, "Power-On Hours", 85, 85, 0, 14820, "14820 ore", "OK", "Tempo totale di funzionamento"),
        SmartAttribute(12, "Power Cycle Count", 98, 98, 0, 1280, "1280", "OK", "Cicli di accensione"),
        SmartAttribute(173, "Media Wearout Indicator", 76, 76, 0, 24, "76% rimanente", "OK", "Livello di usura delle celle NAND (Vita residua)"),
        SmartAttribute(177, "Wear Range Delta", 95, 95, 0, 5, "5", "OK", "Differenza usura tra blocchi"),
        SmartAttribute(180, "Unused Reserved Block Count", 100, 100, 0, 894, "894", "OK", "Blocchi di riserva disponibili"),
        SmartAttribute(183, "Runtime Bad Block Total", 100, 100, 0, 0, "0", "OK", "Blocchi difettosi rilevati a runtime"),
        SmartAttribute(187, "Reported Uncorrectable Errors", 100, 100, 0, 0, "0", "OK", "Errori non correggibili"),
        SmartAttribute(194, "Temperature", 69, 58, 0, 31, "31 °C", "OK", "Temperatura del disco"),
        SmartAttribute(196, "Reallocation Event Count", 100, 100, 0, 0, "0", "OK", "Eventi di riallocazione"),
        SmartAttribute(197, "Current Pending Sector Count", 100, 100, 0, 0, "0", "OK", "Settori instabili in attesa"),
        SmartAttribute(199, "UltraDMA CRC Error Count", 100, 100, 0, 0, "0", "OK", "Errori interfaccia cavo SATA"),
        SmartAttribute(202, "Percent Lifetime Remain", 76, 76, 0, 24, "76%", "OK", "Percentuale di vita residua"),
        SmartAttribute(241, "Total LBAs Written", 100, 100, 0, 167828501654, "78.15 TB", "OK", "Totale scritture host"),
        SmartAttribute(242, "Total LBAs Read", 100, 100, 0, 185193753800, "86.23 TB", "OK", "Totale letture host"),
    ]
    sata_ssd.attributes = sata_attrs

    hdd = DiskInfo(
        device_path="/dev/sdb",
        model_name="Seagate BarraCuda 4TB ST4000DM004",
        serial_number="ZGY149XB",
        firmware="0001",
        interface_type="SATA 6.0 Gb/s (SATA III)",
        protocol="SATA",
        capacity_bytes=4000787030016,
        capacity_str="3.64 TB (4000 GB)",
        is_ssd=False,
        rotation_rate="5425 RPM (HDD Meccanico)",
        form_factor="3.5 inch",
        smart_passed=True,
        remaining_life_percent=58,
        health_status="Attenzione",
        health_color="#F59E0B",
        health_details="Rilevati 8 settori pendenti (instabili). Monitorare e considerare il backup preventivo.",
        temperature_c=41,
        power_on_hours=28450,
        power_on_hours_str="3.2 anni (1.185 giorni - 28.450 ore)",
        power_cycles=3490,
        reallocated_sectors=4,
        pending_sectors=8,
        uncorrectable_sectors=0,
        mount_points=["/mnt/backup"]
    )

    hdd_attrs = [
        SmartAttribute(1, "Raw Read Error Rate", 81, 64, 6, 12849102, "0x000000C4114E", "OK", "Tasso di errori lettura raw"),
        SmartAttribute(3, "Spin-Up Time", 96, 95, 0, 0, "4.2 sec", "OK", "Tempo di accelerazione del motore fino a regime"),
        SmartAttribute(4, "Start/Stop Count", 97, 97, 20, 3512, "3512", "OK", "Avvii e arresti del piatto magnetico"),
        SmartAttribute(5, "Reallocated Sectors Count", 98, 98, 10, 4, "4 settori", "WARN", "Settori danneggiati riallocati"),
        SmartAttribute(7, "Seek Error Rate", 86, 60, 45, 418291048, "0x000018F081E8", "OK", "Tasso di errori durante il posizionamento"),
        SmartAttribute(9, "Power-On Hours", 68, 68, 0, 28450, "28450 ore", "OK", "Ore totali di accensione"),
        SmartAttribute(10, "Spin Retry Count", 100, 100, 97, 0, "0", "OK", "Tentativi di riavvio mandrino falliti"),
        SmartAttribute(12, "Power Cycle Count", 97, 97, 20, 3490, "3490", "OK", "Cicli di accensione"),
        SmartAttribute(187, "Reported Uncorrectable Errors", 100, 100, 0, 0, "0", "OK", "Errori di lettura non correggibili"),
        SmartAttribute(188, "Command Timeout", 100, 99, 0, 1, "1", "OK", "Timeout comandi I/O"),
        SmartAttribute(189, "High Fly Writes", 99, 99, 0, 1, "1", "OK", "Testina oltre l'altezza limite"),
        SmartAttribute(190, "Airflow Temperature", 59, 48, 45, 41, "41 °C", "OK", "Temperatura flusso aria"),
        SmartAttribute(194, "Temperature", 41, 52, 0, 41, "41 °C", "OK", "Temperatura interna"),
        SmartAttribute(197, "Current Pending Sector Count", 96, 96, 0, 8, "8 settori", "WARN", "Settori instabili in attesa di riallocazione"),
        SmartAttribute(198, "Offline Uncorrectable Sector Count", 100, 100, 0, 0, "0", "OK", "Settori non correggibili durante test offline"),
        SmartAttribute(199, "UltraDMA CRC Error Count", 200, 200, 0, 0, "0", "OK", "Errori trasmissione bus SATA"),
    ]
    hdd.attributes = hdd_attrs

    return [nvme, sata_ssd, hdd]
