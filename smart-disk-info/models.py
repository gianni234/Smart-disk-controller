from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class SmartAttribute:
    id: int
    name: str
    value: Optional[int] = None
    worst: Optional[int] = None
    threshold: Optional[int] = None
    raw_value: int = 0
    raw_string: str = ""
    status: str = "OK"
    description: str = ""
    flags: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DiskInfo:
    device_path: str
    model_name: str = "Dispositivo Sconosciuto"
    serial_number: str = "N/D"
    firmware: str = "N/D"
    interface_type: str = "SATA"
    protocol: str = "SATA"
    capacity_bytes: int = 0
    capacity_str: str = "N/D"
    is_ssd: bool = True
    rotation_rate: str = "SSD (Solid State)"
    form_factor: str = "N/D"

    smart_passed: bool = True
    remaining_life_percent: Optional[int] = None
    health_status: str = "Buono"
    health_details: str = ""
    health_color: str = "#10B981"

    temperature_c: Optional[int] = None
    temperature_max_c: Optional[int] = None
    power_on_hours: Optional[int] = None
    power_on_hours_str: str = "N/D"
    power_cycles: Optional[int] = None

    total_bytes_written: Optional[int] = None
    total_written_str: str = "N/D"
    total_bytes_read: Optional[int] = None
    total_read_str: str = "N/D"
    unsafe_shutdowns: Optional[int] = None
    media_errors: Optional[int] = None
    available_spare: Optional[int] = None
    available_spare_threshold: Optional[int] = None

    reallocated_sectors: Optional[int] = None
    pending_sectors: Optional[int] = None
    uncorrectable_sectors: Optional[int] = None

    attributes: List[SmartAttribute] = field(default_factory=list)
    raw_json: Dict[str, Any] = field(default_factory=dict)

    mount_points: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
