import os
import sys
import json
import time
import shutil
import subprocess

try:
    from PyQt6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
        QLabel, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
        QHeaderView, QFrame, QScrollArea, QFileDialog, QMessageBox,
        QLineEdit, QAbstractItemView, QToolBar, QProgressBar, QGroupBox,
        QFormLayout, QMenuBar, QMenu, QTabWidget, QSizePolicy
    )
    from PyQt6.QtCore import Qt, QTimer, pyqtSlot
    from PyQt6.QtGui import QIcon, QColor, QFont, QAction, QFontDatabase, QActionGroup
except ImportError:
    from PySide6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
        QLabel, QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
        QHeaderView, QFrame, QScrollArea, QFileDialog, QMessageBox,
        QLineEdit, QAbstractItemView, QToolBar, QProgressBar, QGroupBox,
        QFormLayout, QMenuBar, QMenu, QTabWidget, QSizePolicy
    )
    from PySide6.QtCore import Qt, QTimer, Slot as pyqtSlot
    from PySide6.QtGui import QIcon, QColor, QFont, QAction, QFontDatabase, QActionGroup

from models import DiskInfo, SmartAttribute
from disk_scanner import DiskScanner, get_mock_disks
from i18n import tr, set_current_lang, get_current_lang, LANGUAGES, get_translated_attribute


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("app_title"))
        self.setWindowIcon(QIcon.fromTheme("drive-harddisk"))
        self.resize(1024, 720)
        self.setMinimumSize(850, 550)

        self.mono_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)

        self.scanner = DiskScanner()
        self.disks: list[DiskInfo] = []
        self.current_disk: DiskInfo | None = None
        self.is_demo_mode = False
        self.show_raw_hex = False

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_disks)

        self.init_ui()
        self.load_initial_data()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.setup_menu_bar()
        self.setup_toolbar()

        self.disk_tabs = QTabWidget()
        self.disk_tabs.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.disk_tabs.currentChanged.connect(self.on_disk_tab_changed)
        self.main_layout.addWidget(self.disk_tabs)

        self.setup_disk_overview()

        self.setup_attributes_table()

        self.statusBar().showMessage(tr("ready"))

    def setup_menu_bar(self):
        menubar = self.menuBar()

        self.menu_file = menubar.addMenu(tr("menu_file"))
        self.act_refresh = self.menu_file.addAction(QIcon.fromTheme("view-refresh"), tr("action_refresh"))
        self.act_refresh.setShortcut("F5")
        self.act_refresh.triggered.connect(self.refresh_disks)

        self.act_export = self.menu_file.addAction(QIcon.fromTheme("document-save"), tr("action_export"))
        self.act_export.setShortcut("Ctrl+S")
        self.act_export.triggered.connect(self.export_report)

        self.menu_file.addSeparator()
        self.act_quit = self.menu_file.addAction(QIcon.fromTheme("application-exit"), tr("action_quit"))
        self.act_quit.setShortcut("Ctrl+Q")
        self.act_quit.triggered.connect(self.close)

        self.menu_tools = menubar.addMenu(tr("menu_tools"))
        self.act_demo = QAction(tr("action_demo"), self)
        self.act_demo.setCheckable(True)
        self.act_demo.triggered.connect(self.toggle_demo_mode)
        self.menu_tools.addAction(self.act_demo)

        if os.geteuid() != 0:
            self.act_root_menu = self.menu_tools.addAction(QIcon.fromTheme("security-high"), tr("action_root"))
            self.act_root_menu.triggered.connect(self.elevate_with_root)

        self.menu_lang = menubar.addMenu(tr("menu_language"))
        self.lang_action_group = QActionGroup(self)
        self.lang_action_group.setExclusive(True)

        for code, label in [("it", "Italiano"), ("en", "English"), ("ru", "Русский")]:
            act = QAction(label, self)
            act.setCheckable(True)
            if code == get_current_lang():
                act.setChecked(True)
            act.triggered.connect(lambda checked=False, c=code: self.change_language(c))
            self.lang_action_group.addAction(act)
            self.menu_lang.addAction(act)

        self.menu_help = menubar.addMenu(tr("menu_help"))
        self.act_about = self.menu_help.addAction(QIcon.fromTheme("help-about"), tr("action_about"))
        self.act_about.triggered.connect(self.show_about_dialog)

    def setup_toolbar(self):
        self.toolbar = QToolBar("Barra Principale")
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        self.tb_act_refresh = self.toolbar.addAction(QIcon.fromTheme("view-refresh"), tr("toolbar_refresh"))
        self.tb_act_refresh.setToolTip(tr("action_refresh_tooltip"))
        self.tb_act_refresh.triggered.connect(self.refresh_disks)

        self.tb_act_export = self.toolbar.addAction(QIcon.fromTheme("document-save"), tr("toolbar_export"))
        self.tb_act_export.setToolTip(tr("action_export_tooltip"))
        self.tb_act_export.triggered.connect(self.export_report)

        self.toolbar.addSeparator()

        self.lbl_auto_toolbar = QLabel(tr("toolbar_auto_refresh"))
        self.toolbar.addWidget(self.lbl_auto_toolbar)

        self.combo_auto = QComboBox()
        self.populate_auto_refresh_combo()
        self.combo_auto.currentIndexChanged.connect(self.on_auto_refresh_changed)
        self.toolbar.addWidget(self.combo_auto)

        self.toolbar.addSeparator()

        if os.geteuid() != 0:
            self.act_elevate_tb = self.toolbar.addAction(QIcon.fromTheme("dialog-password"), tr("toolbar_root_request"))
            self.act_elevate_tb.setToolTip(tr("toolbar_root_tooltip"))
            self.act_elevate_tb.triggered.connect(self.elevate_with_root)

    def populate_auto_refresh_combo(self):
        cur_idx = self.combo_auto.currentIndex() if self.combo_auto.count() > 0 else 0
        self.combo_auto.blockSignals(True)
        self.combo_auto.clear()
        self.combo_auto.addItems([
            tr("interval_manual"),
            tr("interval_30s"),
            tr("interval_1m"),
            tr("interval_5m"),
            tr("interval_10m")
        ])
        self.combo_auto.setCurrentIndex(max(0, cur_idx))
        self.combo_auto.blockSignals(False)

    def setup_disk_overview(self):
        overview_widget = QWidget()
        overview_layout = QHBoxLayout(overview_widget)
        overview_layout.setContentsMargins(0, 0, 0, 0)
        overview_layout.setSpacing(12)

        self.group_health = QGroupBox(tr("group_health"))
        health_layout = QVBoxLayout(self.group_health)
        health_layout.setSpacing(6)

        self.lbl_life_title = QLabel(tr("life_remaining", percent=100))
        self.lbl_life_title.setStyleSheet("font-weight: bold;")
        health_layout.addWidget(self.lbl_life_title)

        self.progress_life = QProgressBar()
        self.progress_life.setRange(0, 100)
        self.progress_life.setValue(100)
        self.progress_life.setTextVisible(True)
        self.progress_life.setFormat("%v%")
        health_layout.addWidget(self.progress_life)

        self.lbl_health_status = QLabel(tr("health_status", status=tr("status_good")))
        health_layout.addWidget(self.lbl_health_status)

        self.lbl_temp = QLabel(tr("temperature", temp="N/D"))
        health_layout.addWidget(self.lbl_temp)

        health_layout.addStretch()
        overview_layout.addWidget(self.group_health, stretch=1)

        self.group_info = QGroupBox(tr("group_info"))
        self.form_info = QFormLayout(self.group_info)
        self.form_info.setContentsMargins(10, 8, 10, 8)
        self.form_info.setSpacing(6)

        self.lbl_hdr_model = QLabel(tr("label_model"))
        self.lbl_hdr_serial = QLabel(tr("label_serial"))
        self.lbl_hdr_firmware = QLabel(tr("label_firmware"))
        self.lbl_hdr_interface = QLabel(tr("label_interface"))
        self.lbl_hdr_capacity = QLabel(tr("label_capacity"))

        self.lbl_model = QLabel("-")
        self.lbl_serial = QLabel("-")
        self.lbl_firmware = QLabel("-")
        self.lbl_interface = QLabel("-")
        self.lbl_capacity = QLabel("-")

        self.form_info.addRow(self.lbl_hdr_model, self.lbl_model)
        self.form_info.addRow(self.lbl_hdr_serial, self.lbl_serial)
        self.form_info.addRow(self.lbl_hdr_firmware, self.lbl_firmware)
        self.form_info.addRow(self.lbl_hdr_interface, self.lbl_interface)
        self.form_info.addRow(self.lbl_hdr_capacity, self.lbl_capacity)

        overview_layout.addWidget(self.group_info, stretch=2)

        self.group_metrics = QGroupBox(tr("group_usage"))
        self.form_metrics = QFormLayout(self.group_metrics)
        self.form_metrics.setContentsMargins(10, 8, 10, 8)
        self.form_metrics.setSpacing(6)

        self.lbl_hdr_writes = QLabel(tr("label_writes"))
        self.lbl_hdr_reads = QLabel(tr("label_reads"))
        self.lbl_hdr_poh = QLabel(tr("label_poh"))
        self.lbl_hdr_cycles = QLabel(tr("label_cycles"))
        self.lbl_hdr_errors = QLabel(tr("label_errors"))

        self.lbl_writes = QLabel("-")
        self.lbl_reads = QLabel("-")
        self.lbl_poh = QLabel("-")
        self.lbl_cycles = QLabel("-")
        self.lbl_errors = QLabel("-")

        self.form_metrics.addRow(self.lbl_hdr_writes, self.lbl_writes)
        self.form_metrics.addRow(self.lbl_hdr_reads, self.lbl_reads)
        self.form_metrics.addRow(self.lbl_hdr_poh, self.lbl_poh)
        self.form_metrics.addRow(self.lbl_hdr_cycles, self.lbl_cycles)
        self.form_metrics.addRow(self.lbl_hdr_errors, self.lbl_errors)

        overview_layout.addWidget(self.group_metrics, stretch=2)
        self.main_layout.addWidget(overview_widget)

    def setup_attributes_table(self):
        self.group_table = QGroupBox(tr("group_table"))
        table_layout = QVBoxLayout(self.group_table)
        table_layout.setContentsMargins(8, 8, 8, 8)
        table_layout.setSpacing(6)

        ctrl_layout = QHBoxLayout()
        self.btn_raw_toggle = QPushButton(tr("btn_raw_dec"))
        self.btn_raw_toggle.clicked.connect(self.toggle_raw_format)
        ctrl_layout.addWidget(self.btn_raw_toggle)

        ctrl_layout.addStretch()

        self.lbl_search = QLabel(tr("search_label"))
        ctrl_layout.addWidget(self.lbl_search)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(tr("search_placeholder"))
        self.search_input.setMaximumWidth(220)
        self.search_input.textChanged.connect(self.filter_table)
        ctrl_layout.addWidget(self.search_input)

        table_layout.addLayout(ctrl_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.update_table_headers()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        table_layout.addWidget(self.table)
        self.main_layout.addWidget(self.group_table)

    def update_table_headers(self):
        self.table.setHorizontalHeaderLabels([
            tr("col_id"),
            tr("col_name"),
            tr("col_current"),
            tr("col_worst"),
            tr("col_threshold"),
            tr("col_raw"),
            tr("col_status"),
            tr("col_desc"),
        ])

    def change_language(self, lang_code: str):
        set_current_lang(lang_code)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(tr("app_title"))

        self.menu_file.setTitle(tr("menu_file"))
        self.act_refresh.setText(tr("action_refresh"))
        self.act_export.setText(tr("action_export"))
        self.act_quit.setText(tr("action_quit"))

        self.menu_tools.setTitle(tr("menu_tools"))
        self.act_demo.setText(tr("action_demo"))
        if hasattr(self, "act_root_menu"):
            self.act_root_menu.setText(tr("action_root"))

        self.menu_lang.setTitle(tr("menu_language"))
        self.menu_help.setTitle(tr("menu_help"))
        self.act_about.setText(tr("action_about"))

        self.tb_act_refresh.setText(tr("toolbar_refresh"))
        self.tb_act_refresh.setToolTip(tr("action_refresh_tooltip"))
        self.tb_act_export.setText(tr("toolbar_export"))
        self.tb_act_export.setToolTip(tr("action_export_tooltip"))
        self.lbl_auto_toolbar.setText(tr("toolbar_auto_refresh"))
        if hasattr(self, "act_elevate_tb"):
            self.act_elevate_tb.setText(tr("toolbar_root_request"))
            self.act_elevate_tb.setToolTip(tr("toolbar_root_tooltip"))
        self.populate_auto_refresh_combo()

        self.group_health.setTitle(tr("group_health"))
        self.group_info.setTitle(tr("group_info"))
        self.group_metrics.setTitle(tr("group_usage"))
        self.group_table.setTitle(tr("group_table"))

        self.lbl_hdr_model.setText(tr("label_model"))
        self.lbl_hdr_serial.setText(tr("label_serial"))
        self.lbl_hdr_firmware.setText(tr("label_firmware"))
        self.lbl_hdr_interface.setText(tr("label_interface"))
        self.lbl_hdr_capacity.setText(tr("label_capacity"))

        self.lbl_hdr_writes.setText(tr("label_writes"))
        self.lbl_hdr_reads.setText(tr("label_reads"))
        self.lbl_hdr_poh.setText(tr("label_poh"))
        self.lbl_hdr_cycles.setText(tr("label_cycles"))
        self.lbl_hdr_errors.setText(tr("label_errors"))

        self.btn_raw_toggle.setText(tr("btn_raw_hex") if self.show_raw_hex else tr("btn_raw_dec"))
        self.lbl_search.setText(tr("search_label"))
        self.search_input.setPlaceholderText(tr("search_placeholder"))
        self.update_table_headers()

        self.render_disk_tabs()
        if self.current_disk:
            self.select_disk(self.current_disk)

        self.statusBar().showMessage(tr("ready"), 2000)

    def load_initial_data(self):
        self.refresh_disks()

    def refresh_disks(self, use_root: bool = False):
        self.statusBar().showMessage(tr("scanning"))

        if self.is_demo_mode:
            self.disks = get_mock_disks()
        else:
            is_root = os.geteuid() == 0 or use_root
            devs = self.scanner.scan_devices(use_root=is_root)
            loaded_disks = []
            for dev in devs:
                info = self.scanner.get_disk_info(dev, use_root=is_root)
                loaded_disks.append(info)

            has_permission_denied = any(d.error_message and "Permesso negato" in d.error_message for d in loaded_disks)
            if (not loaded_disks or has_permission_denied) and os.geteuid() != 0 and not self.disks:
                self.prompt_root_required()
                return

            self.disks = loaded_disks

        self.render_disk_tabs()

        if self.disks:
            current_path = self.current_disk.device_path if self.current_disk else None
            matching = next((d for d in self.disks if d.device_path == current_path), None)
            self.select_disk(matching or self.disks[0])
            self.statusBar().showMessage(tr("disks_loaded", count=len(self.disks)), 3000)

    def prompt_root_required(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(tr("root_required_title"))
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setText(tr("root_required_text"))
        btn_root = msg_box.addButton(tr("btn_run_root"), QMessageBox.ButtonRole.AcceptRole)
        btn_demo = msg_box.addButton(tr("btn_use_demo"), QMessageBox.ButtonRole.RejectRole)
        msg_box.addButton(tr("btn_cancel"), QMessageBox.ButtonRole.DestructiveRole)

        msg_box.exec()
        clicked = msg_box.clickedButton()

        if clicked == btn_root:
            self.elevate_with_root()
        elif clicked == btn_demo:
            self.is_demo_mode = True
            self.act_demo.setChecked(True)
            self.refresh_disks()

    def elevate_with_root(self):
        pkexec = shutil.which("pkexec")
        if not pkexec:
            QMessageBox.critical(self, tr("export_error_title"), tr("pkexec_not_found"))
            return

        display = os.environ.get("DISPLAY", ":0")
        xauth = os.environ.get("XAUTHORITY", os.path.expanduser("~/.Xauthority"))
        wayland_display = os.environ.get("WAYLAND_DISPLAY", "")
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        script_path = os.path.join(script_dir, "smart_disk_info.py")

        env_args = ["env", f"DISPLAY={display}", f"XAUTHORITY={xauth}", f"PYTHONPATH={script_dir}"]
        if wayland_display:
            env_args.append(f"WAYLAND_DISPLAY={wayland_display}")

        cmd = [pkexec] + env_args + [sys.executable, script_path, "--no-root"]
        try:
            self.hide()
            res = subprocess.run(cmd)
            if res.returncode == 0:
                sys.exit(0)
            else:
                self.show()
                self.refresh_disks()
        except Exception as e:
            self.show()
            QMessageBox.critical(self, tr("elevate_error_title"), str(e))

    def render_disk_tabs(self):
        self.disk_tabs.blockSignals(True)
        self.disk_tabs.clear()

        for idx, disk in enumerate(self.disks):
            pct_str = f"{disk.remaining_life_percent}%" if disk.remaining_life_percent is not None else ""
            tab_label = f"{os.path.basename(disk.device_path)}: {disk.model_name}"
            if pct_str:
                tab_label += f" ({pct_str})"
            self.disk_tabs.addTab(QWidget(), QIcon.fromTheme("drive-harddisk"), tab_label)

        self.disk_tabs.blockSignals(False)

    def on_disk_tab_changed(self, index: int):
        if 0 <= index < len(self.disks):
            self.select_disk(self.disks[index])

    def select_disk(self, disk: DiskInfo):
        self.current_disk = disk

        for i in range(self.disk_tabs.count()):
            if i < len(self.disks) and self.disks[i].device_path == disk.device_path:
                self.disk_tabs.setCurrentIndex(i)
                break

        pct = disk.remaining_life_percent if disk.remaining_life_percent is not None else 100
        self.progress_life.setValue(pct)
        self.lbl_life_title.setText(tr("life_remaining", percent=pct))

        status_key = "status_good"
        if disk.health_status == "Ottimo":
            status_key = "status_excellent"
        elif disk.health_status == "Attenzione":
            status_key = "status_warning"
        elif disk.health_status == "Critico":
            status_key = "status_critical"

        localized_status = tr(status_key)

        if pct < 50 or not disk.smart_passed or status_key in ("status_warning", "status_critical"):
            self.lbl_health_status.setText(tr("health_status", status=f"{localized_status}"))
            self.lbl_health_status.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.lbl_health_status.setText(tr("health_status", status=localized_status))
            self.lbl_health_status.setStyleSheet("")

        if disk.temperature_c is not None:
            self.lbl_temp.setText(tr("temperature", temp=f"{disk.temperature_c} °C"))
            if disk.temperature_c >= 65:
                self.lbl_temp.setStyleSheet("color: red; font-weight: bold;")
            elif disk.temperature_c >= 55:
                self.lbl_temp.setStyleSheet("color: orange; font-weight: bold;")
            else:
                self.lbl_temp.setStyleSheet("")
        else:
            self.lbl_temp.setText(tr("temperature", temp="N/D"))
            self.lbl_temp.setStyleSheet("")

        self.lbl_model.setText(disk.model_name or "-")
        self.lbl_serial.setText(disk.serial_number if disk.serial_number != "N/D" else "-")
        self.lbl_firmware.setText(disk.firmware if disk.firmware != "N/D" else "-")

        if disk.is_ssd:
            self.lbl_interface.setText(f"{disk.interface_type} • {tr('type_ssd')}")
        else:
            rpm_val = disk.rotation_rate.split()[0] if disk.rotation_rate and disk.rotation_rate.split()[0].isdigit() else "5400"
            self.lbl_interface.setText(f"{disk.interface_type} • {tr('type_hdd', rpm=rpm_val)}")

        self.lbl_capacity.setText(disk.capacity_str or "-")

        self.lbl_writes.setText(disk.total_written_str if disk.total_written_str != "N/D" else "-")
        self.lbl_reads.setText(disk.total_read_str if disk.total_read_str != "N/D" else "-")

        if disk.power_on_hours is not None:
            hours = disk.power_on_hours
            if hours < 24:
                poh_str = tr("hours_short", hours=hours)
            else:
                days = hours // 24
                rem_hours = hours % 24
                if days < 365:
                    poh_str = tr("days_hours_short", days=days, hours=rem_hours, total=hours)
                else:
                    years = days / 365.25
                    poh_str = tr("years_days_short", years=years, days=days, total=hours)
            self.lbl_poh.setText(poh_str)
        else:
            self.lbl_poh.setText("-")

        self.lbl_cycles.setText(f"{disk.power_cycles:,}" if disk.power_cycles is not None else "-")

        if disk.interface_type == "NVMe":
            errs = disk.media_errors or 0
            unsafe = disk.unsafe_shutdowns or 0
            err_text = tr("nvme_errors_format", errors=errs, unsafe=unsafe)
            self.lbl_errors.setText(err_text)
            if errs > 0:
                self.lbl_errors.setStyleSheet("color: red; font-weight: bold;")
            else:
                self.lbl_errors.setStyleSheet("")
        else:
            realloc = disk.reallocated_sectors or 0
            pending = disk.pending_sectors or 0
            err_text = tr("sata_errors_format", realloc=realloc, pending=pending)
            self.lbl_errors.setText(err_text)
            if realloc > 0 or pending > 0:
                self.lbl_errors.setStyleSheet("color: red; font-weight: bold;")
            else:
                self.lbl_errors.setStyleSheet("")

        self.populate_table(disk.attributes)

    def populate_table(self, attributes: list[SmartAttribute]):
        self.table.setRowCount(0)
        search_query = self.search_input.text().lower().strip()

        has_normalized_values = any(
            (attr.value is not None or attr.worst is not None or attr.threshold is not None)
            for attr in attributes
        )

        self.table.setColumnHidden(2, not has_normalized_values)
        self.table.setColumnHidden(3, not has_normalized_values)
        self.table.setColumnHidden(4, not has_normalized_values)

        for attr in attributes:
            t_name, t_desc = get_translated_attribute(attr.id, attr.name, attr.description)

            if search_query:
                id_match = str(attr.id).startswith(search_query) or hex(attr.id).lower().startswith(search_query)
                name_match = search_query in t_name.lower() or search_query in attr.name.lower()
                if not (id_match or name_match):
                    continue

            row = self.table.rowCount()
            self.table.insertRow(row)

            id_str = f"0x{attr.id:02X} ({attr.id})" if attr.id < 256 else str(attr.id)
            item_id = QTableWidgetItem(id_str)
            item_id.setFont(self.mono_font)
            item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, item_id)

            item_name = QTableWidgetItem(t_name)
            self.table.setItem(row, 1, item_name)

            val_str = str(attr.value) if attr.value is not None else "-"
            item_val = QTableWidgetItem(val_str)
            item_val.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 2, item_val)

            worst_str = str(attr.worst) if attr.worst is not None else "-"
            item_worst = QTableWidgetItem(worst_str)
            item_worst.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, item_worst)

            thresh_str = str(attr.threshold) if attr.threshold is not None else "-"
            item_thresh = QTableWidgetItem(thresh_str)
            item_thresh.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 4, item_thresh)

            if self.show_raw_hex:
                raw_display = f"0x{attr.raw_value:012X}" if isinstance(attr.raw_value, int) else attr.raw_string
            else:
                raw_display = attr.raw_string or f"{attr.raw_value:,}"
            item_raw = QTableWidgetItem(raw_display)
            item_raw.setFont(self.mono_font)
            item_raw.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 5, item_raw)

            status_item = QTableWidgetItem(attr.status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if attr.status == "WARN":
                status_item.setForeground(QColor("orange"))
            elif attr.status == "FAIL":
                status_item.setForeground(QColor("red"))
            self.table.setItem(row, 6, status_item)

            item_desc = QTableWidgetItem(t_desc)
            self.table.setItem(row, 7, item_desc)

        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)

    def filter_table(self):
        if self.current_disk:
            self.populate_table(self.current_disk.attributes)

    def toggle_raw_format(self):
        self.show_raw_hex = not self.show_raw_hex
        self.btn_raw_toggle.setText(tr("btn_raw_hex") if self.show_raw_hex else tr("btn_raw_dec"))
        if self.current_disk:
            self.populate_table(self.current_disk.attributes)

    def toggle_demo_mode(self, checked: bool):
        self.is_demo_mode = checked
        self.refresh_disks()

    def on_auto_refresh_changed(self, index: int):
        intervals = {0: 0, 1: 30000, 2: 60000, 3: 300000, 4: 600000}
        ms = intervals.get(index, 0)
        if ms > 0:
            self.refresh_timer.start(ms)
            self.statusBar().showMessage(tr("auto_refresh_set", interval=self.combo_auto.currentText()), 3000)
        else:
            self.refresh_timer.stop()
            self.statusBar().showMessage(tr("auto_refresh_disabled"), 3000)

    def export_report(self):
        if not self.current_disk:
            QMessageBox.warning(self, tr("export_error_title"), tr("no_disk_selected"))
            return

        disk = self.current_disk
        default_filename = f"smart_report_{os.path.basename(disk.device_path)}_{int(time.time())}.txt"

        filepath, _ = QFileDialog.getSaveFileName(
            self, tr("export_title"), default_filename, tr("export_file_filter")
        )
        if not filepath:
            return

        try:
            if filepath.endswith(".json"):
                data = {
                    "device": disk.device_path, "model": disk.model_name,
                    "serial": disk.serial_number, "firmware": disk.firmware,
                    "interface": disk.interface_type, "capacity": disk.capacity_str,
                    "remaining_life_percent": disk.remaining_life_percent,
                    "health_status": disk.health_status, "temperature_c": disk.temperature_c,
                    "power_on_hours": disk.power_on_hours, "total_written": disk.total_written_str,
                    "total_read": disk.total_read_str,
                    "attributes": [
                        {"id": a.id, "name": a.name, "value": a.value, "worst": a.worst,
                         "threshold": a.threshold, "raw": a.raw_string or a.raw_value,
                         "status": a.status, "description": a.description}
                        for a in disk.attributes
                    ]
                }
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                lines = [
                    "=" * 60,
                    f"REPORT SMART - {disk.model_name}",
                    "=" * 60,
                    f"Device:                {disk.device_path}",
                    f"Serial Number:         {disk.serial_number}",
                    f"Firmware:              {disk.firmware}",
                    f"Interface:             {disk.interface_type} ({disk.rotation_rate})",
                    f"Capacity:              {disk.capacity_str}",
                    f"Remaining Life:        {disk.remaining_life_percent}% ({disk.health_status})",
                    f"Temperature:           {disk.temperature_c}°C" if disk.temperature_c else "Temperature: N/D",
                    f"Power-On Hours:        {disk.power_on_hours_str}",
                    f"Power Cycles:          {disk.power_cycles}",
                    f"Host Writes:           {disk.total_written_str}",
                    f"Host Reads:            {disk.total_read_str}",
                    "-" * 60,
                    "ATTRIBUTES:",
                    "-" * 60,
                    f"{'ID':<6} {'ATTRIBUTE NAME':<30} {'VALUE':<8} {'WORST':<8} {'THRESH':<8} {'RAW':<16} {'STATUS'}",
                    "-" * 60,
                ]
                for a in disk.attributes:
                    lines.append(
                        f"{a.id:<6} {a.name[:28]:<30} {str(a.value or '-'):<8} {str(a.worst or '-'):<8} "
                        f"{str(a.threshold or '-'):<8} {str(a.raw_string or a.raw_value)[:15]:<16} {a.status}"
                    )
                lines.append("=" * 60)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))

            QMessageBox.information(self, tr("export_success_title"), tr("export_success_text", path=filepath))
        except Exception as e:
            QMessageBox.critical(self, tr("export_error_title"), tr("export_error_text", error=str(e)))

    def show_about_dialog(self):
        QMessageBox.about(
            self,
            tr("about_title"),
            tr("about_text")
        )
