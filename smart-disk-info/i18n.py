LANGUAGES = {
    "en": "English",
    "it": "Italiano",
    "ru": "Русский"
}

current_language = "en"


def get_current_lang() -> str:
    return current_language


def set_current_lang(lang: str):
    global current_language
    if lang in LANGUAGES:
        current_language = lang


TRANSLATIONS = {
    "en": {
        "app_title": "smart disk controller by gianni234",
        "ready": "Ready",
        "scanning": "Scanning SMART disk devices...",
        "disks_loaded": "Loaded {count} disk(s).",

        "menu_file": "&File",
        "menu_tools": "&Tools",
        "menu_language": "&Language",
        "menu_help": "&Help",
        "action_refresh": "&Refresh",
        "action_refresh_tooltip": "Refresh disk SMART data (F5)",
        "action_export": "&Export Report...",
        "action_export_tooltip": "Save a text or JSON SMART health report",
        "action_quit": "&Quit",
        "action_demo": "Simulation Mode (Demo)",
        "action_root": "Run as Root (pkexec)...",
        "action_about": "&About...",

        "toolbar_refresh": "Refresh",
        "toolbar_export": "Export Report",
        "toolbar_auto_refresh": " Refresh: ",
        "toolbar_root_request": "Request Root Privileges",
        "toolbar_root_tooltip": "Run as root to enable direct SMART access to all controllers",
        "interval_manual": "Manual",
        "interval_30s": "30 seconds",
        "interval_1m": "1 minute",
        "interval_5m": "5 minutes",
        "interval_10m": "10 minutes",
        "auto_refresh_set": "Auto-refresh set to {interval}.",
        "auto_refresh_disabled": "Auto-refresh disabled.",

        "group_health": "Health Status",
        "life_remaining": "Remaining Life: {percent}%",
        "health_status": "Status: {status}",
        "temperature": "Temperature: {temp}",
        "status_excellent": "Excellent",
        "status_good": "Good",
        "status_warning": "Warning",
        "status_critical": "Critical",
        "status_unknown": "Unknown",

        "group_info": "Device Information",
        "label_model": "Model:",
        "label_serial": "Serial Number:",
        "label_firmware": "Firmware:",
        "label_interface": "Interface:",
        "label_capacity": "Capacity:",
        "type_ssd": "SSD (Solid State Drive)",
        "type_hdd": "{rpm} RPM (Mechanical HDD)",

        "group_usage": "Usage Statistics",
        "label_writes": "Host Writes (TBW):",
        "label_reads": "Host Reads:",
        "label_poh": "Power-On Hours:",
        "label_cycles": "Power Cycles:",
        "label_errors": "Errors / Sectors:",
        "nvme_errors_format": "{errors} media errors, {unsafe} unsafe shutdowns",
        "sata_errors_format": "{realloc} reallocated, {pending} pending",

        "group_table": "S.M.A.R.T. Attributes",
        "btn_raw_dec": "Raw Values: Decimal",
        "btn_raw_hex": "Raw Values: Hexadecimal",
        "search_label": "Filter:",
        "search_placeholder": "Search attribute or ID...",
        "col_id": "ID",
        "col_name": "Attribute Name",
        "col_current": "Current",
        "col_worst": "Worst",
        "col_threshold": "Threshold",
        "col_raw": "Raw Value",
        "col_status": "Status",
        "col_desc": "Description",

        "root_required_title": "Root Privileges Required",
        "root_required_text": "Direct disk access required.\n\nsmartctl requires administrator privileges to read SMART data from physical drives.",
        "btn_run_root": "Run as Root (pkexec)",
        "btn_use_demo": "Simulation Mode (Demo)",
        "btn_cancel": "Cancel",
        "pkexec_not_found": "pkexec not found. Run the application from terminal with: sudo python3 smart_disk_info.py",
        "elevate_error_title": "Elevation Error",
        "no_disk_selected": "No disk selected.",
        "export_title": "Export SMART Report",
        "export_file_filter": "Text Document (*.txt);;JSON File (*.json);;All Files (*.*)",
        "export_success_title": "Export Successful",
        "export_success_text": "Report saved to:\n{path}",
        "export_error_title": "Error",
        "export_error_text": "Failed to save report:\n{error}",
        "about_title": "About",
        "about_text": "<b>smart disk controller by gianni234</b><br><br>Native Qt interface for smartctl with health monitoring and remaining life calculation.",

        "hours_short": "{hours} hours",
        "days_hours_short": "{days} days, {hours} hours ({total:,} hours)",
        "years_days_short": "{years:.1f} years ({days:,} days - {total:,} hours)",
    },

    "it": {
        "app_title": "smart disk controller by gianni234",
        "ready": "Pronto",
        "scanning": "Scansione dischi SMART in corso...",
        "disks_loaded": "Caricati {count} dischi.",

        "menu_file": "&File",
        "menu_tools": "&Strumenti",
        "menu_language": "&Lingua",
        "menu_help": "&Aiuto",
        "action_refresh": "&Ricarica",
        "action_refresh_tooltip": "Ricarica i dati SMART dei dischi (F5)",
        "action_export": "&Esporta Report...",
        "action_export_tooltip": "Salva un report testuale o JSON dello stato SMART",
        "action_quit": "&Esci",
        "action_demo": "Modalità Simulazione (Demo)",
        "action_root": "Esegui come Root (pkexec)...",
        "action_about": "&Informazioni...",

        "toolbar_refresh": "Ricarica",
        "toolbar_export": "Esporta Report",
        "toolbar_auto_refresh": " Aggiornamento: ",
        "toolbar_root_request": "Richiedi Permessi Root",
        "toolbar_root_tooltip": "Esegui come root per consentire l'accesso diretto ai dispositivi disco",
        "interval_manual": "Manuale",
        "interval_30s": "30 secondi",
        "interval_1m": "1 minuto",
        "interval_5m": "5 minuti",
        "interval_10m": "10 minuti",
        "auto_refresh_set": "Aggiornamento impostato a {interval}.",
        "auto_refresh_disabled": "Aggiornamento automatico disattivato.",

        "group_health": "Stato di Salute",
        "life_remaining": "Vita residua: {percent}%",
        "health_status": "Stato: {status}",
        "temperature": "Temperatura: {temp}",
        "status_excellent": "Ottimo",
        "status_good": "Buono",
        "status_warning": "Attenzione",
        "status_critical": "Critico",
        "status_unknown": "Sconosciuto",

        "group_info": "Informazioni Dispositivo",
        "label_model": "Modello:",
        "label_serial": "Numero di serie:",
        "label_firmware": "Firmware:",
        "label_interface": "Interfaccia:",
        "label_capacity": "Capacità:",
        "type_ssd": "SSD (Disco a stato solido)",
        "type_hdd": "{rpm} RPM (HDD Meccanico)",

        "group_usage": "Statistiche di Utilizzo",
        "label_writes": "Scritture host (TBW):",
        "label_reads": "Letture host:",
        "label_poh": "Ore di attività:",
        "label_cycles": "Cicli di accensione:",
        "label_errors": "Errori / Settori:",
        "nvme_errors_format": "{errors} errori media, {unsafe} spegnimenti non sicuri",
        "sata_errors_format": "{realloc} riallocati, {pending} pendenti",

        "group_table": "Attributi S.M.A.R.T.",
        "btn_raw_dec": "Valori Raw: Decimale",
        "btn_raw_hex": "Valori Raw: Esadecimale",
        "search_label": "Filtra:",
        "search_placeholder": "Cerca attributo o ID...",
        "col_id": "ID",
        "col_name": "Nome Attributo",
        "col_current": "Attuale",
        "col_worst": "Peggiore",
        "col_threshold": "Soglia",
        "col_raw": "Valore Raw",
        "col_status": "Stato",
        "col_desc": "Descrizione",

        "root_required_title": "Privilegi di Root Richiesti",
        "root_required_text": "Accesso ai dispositivi disco richiesto.\n\nsmartctl necessita dei privilegi di amministratore per leggere i dati SMART dei dispositivi fisici.",
        "btn_run_root": "Esegui con Root (pkexec)",
        "btn_use_demo": "Modalità Simulazione (Demo)",
        "btn_cancel": "Annulla",
        "pkexec_not_found": "pkexec non trovato. Avvia l'applicazione da terminale con: sudo python3 smart_disk_info.py",
        "elevate_error_title": "Errore Elevazione",
        "no_disk_selected": "Nessun disco selezionato.",
        "export_title": "Esporta Report SMART",
        "export_file_filter": "Documento di Testo (*.txt);;File JSON (*.json);;Tutti i file (*.*)",
        "export_success_title": "Esportazione Riuscita",
        "export_success_text": "Report salvato in:\n{path}",
        "export_error_title": "Errore",
        "export_error_text": "Impossibile salvare il report:\n{error}",
        "about_title": "Informazioni",
        "about_text": "<b>smart disk controller by gianni234</b><br><br>Interfaccia grafica per smartctl con monitoraggio della salute e percentuale di vita residua del disco.",

        "hours_short": "{hours} ore",
        "days_hours_short": "{days} giorni, {hours} ore ({total:,} ore)",
        "years_days_short": "{years:.1f} anni ({days:,} giorni - {total:,} ore)",
    },

    "ru": {
        "app_title": "smart disk controller by gianni234",
        "ready": "Готово",
        "scanning": "Сканирование SMART устройств...",
        "disks_loaded": "Загружено дисков: {count}.",

        "menu_file": "&Файл",
        "menu_tools": "&Инструменты",
        "menu_language": "&Язык",
        "menu_help": "&Справка",
        "action_refresh": "&Обновить",
        "action_refresh_tooltip": "Обновить данные SMART (F5)",
        "action_export": "&Экспорт отчёта...",
        "action_export_tooltip": "Сохранить текстовый или JSON отчёт SMART",
        "action_quit": "&Выход",
        "action_demo": "Демо режим (Симуляция)",
        "action_root": "Запустить с правами Root (pkexec)...",
        "action_about": "&О программе...",

        "toolbar_refresh": "Обновить",
        "toolbar_export": "Экспорт отчёта",
        "toolbar_auto_refresh": " Автообновление: ",
        "toolbar_root_request": "Запросить права Root",
        "toolbar_root_tooltip": "Запуск от root для прямого доступа к контроллерам дисков",
        "interval_manual": "Вручную",
        "interval_30s": "30 секунд",
        "interval_1m": "1 минута",
        "interval_5m": "5 минут",
        "interval_10m": "10 минут",
        "auto_refresh_set": "Интервал автообновления: {interval}.",
        "auto_refresh_disabled": "Автообновление отключено.",

        "group_health": "Состояние диска",
        "life_remaining": "Остаточный ресурс: {percent}%",
        "health_status": "Состояние: {status}",
        "temperature": "Температура: {temp}",
        "status_excellent": "Отлично",
        "status_good": "Хорошо",
        "status_warning": "Внимание",
        "status_critical": "Критическое",
        "status_unknown": "Неизвестно",

        "group_info": "Информация об устройстве",
        "label_model": "Модель:",
        "label_serial": "Серийный номер:",
        "label_firmware": "Прошивка:",
        "label_interface": "Интерфейс:",
        "label_capacity": "Ёмкость:",
        "type_ssd": "SSD (Твердотельный накопитель)",
        "type_hdd": "{rpm} RPM (Механический HDD)",

        "group_usage": "Статистика использования",
        "label_writes": "Всего записано (TBW):",
        "label_reads": "Всего прочитано:",
        "label_poh": "Время работы:",
        "label_cycles": "Число включений:",
        "label_errors": "Ошибки / Секторы:",
        "nvme_errors_format": "{errors} ошибок носителя, {unsafe} небезопасных отключений",
        "sata_errors_format": "{realloc} переназначено, {pending} нестабильно",

        "group_table": "Атрибуты S.M.A.R.T.",
        "btn_raw_dec": "Raw значения: Десятичные",
        "btn_raw_hex": "Raw значения: Шестнадцатеричные",
        "search_label": "Поиск:",
        "search_placeholder": "Поиск атрибута или ID...",
        "col_id": "ID",
        "col_name": "Атрибут",
        "col_current": "Текущее",
        "col_worst": "Худшее",
        "col_threshold": "Порог",
        "col_raw": "Raw значение",
        "col_status": "Статус",
        "col_desc": "Описание",

        "root_required_title": "Требуются права Root",
        "root_required_text": "Требуется прямой доступ к дискам.\n\nsmartctl требует прав администратора для чтения данных SMART с физических накопителей.",
        "btn_run_root": "Запустить от Root (pkexec)",
        "btn_use_demo": "Демо режим (Симуляция)",
        "btn_cancel": "Отмена",
        "pkexec_not_found": "pkexec не найден. Запустите приложение из терминала: sudo python3 smart_disk_info.py",
        "elevate_error_title": "Ошибка повышения прав",
        "no_disk_selected": "Диск не выбран.",
        "export_title": "Экспорт отчёта SMART",
        "export_file_filter": "Текстовый документ (*.txt);;JSON файл (*.json);;Все файлы (*.*)",
        "export_success_title": "Экспорт выполнен",
        "export_success_text": "Отчёт сохранён в:\n{path}",
        "export_error_title": "Ошибка",
        "export_error_text": "Не удалось сохранить отчёт:\n{error}",
        "about_title": "О программе",
        "about_text": "<b>smart disk controller by gianni234</b><br><br>Графический интерфейс для smartctl с мониторингом состояния и остаточного ресурса дисков.",

        "hours_short": "{hours} ч.",
        "days_hours_short": "{days} дн., {hours} ч. ({total:,} ч.)",
        "years_days_short": "{years:.1f} г. ({days:,} дн. - {total:,} ч.)",
    }
}


SMART_DESCRIPTIONS = {
    1: {
        "name": {"en": "Raw Read Error Rate", "it": "Errori di Lettura Hardware (Raw)", "ru": "Ошибки чтения (Raw Read Error)"},
        "desc": {
            "en": "Rate of hardware read errors occurring when reading from disk surface.",
            "it": "Frequenza di errori hardware durante la lettura da disco.",
            "ru": "Частота аппаратных ошибок при чтении данных с поверхности накопителя."
        }
    },
    3: {
        "name": {"en": "Spin-Up Time", "it": "Tempo di Avvio Mandrino", "ru": "Время раскрутки шпинделя"},
        "desc": {
            "en": "Average time of spindle motor spin-up to operational RPM.",
            "it": "Tempo medio di accelerazione del motore fino a regime operativo.",
            "ru": "Среднее время раскрутки шпинделя до рабочей скорости."
        }
    },
    4: {
        "name": {"en": "Start/Stop Count", "it": "Conteggio Avvii e Arresti", "ru": "Количество запусков/остановок"},
        "desc": {
            "en": "Total count of spindle motor start/stop cycles.",
            "it": "Numero complessivo di avvii e arresti del piatto magnetico.",
            "ru": "Общее количество циклов старта и остановки шпинделя."
        }
    },
    5: {
        "name": {"en": "Reallocated Sectors Count", "it": "Settori Danneggiati Riallocati", "ru": "Переназначенные секторы"},
        "desc": {
            "en": "Count of damaged sectors moved to reserve spare area.",
            "it": "Numero di settori danneggiati spostati nell'area di riserva.",
            "ru": "Количество повреждённых секторов, перемещённых в резервную область."
        }
    },
    7: {
        "name": {"en": "Seek Error Rate", "it": "Errori di Posizionamento Testine", "ru": "Ошибки позиционирования головок"},
        "desc": {
            "en": "Rate of head positioning errors during magnetic seek operations.",
            "it": "Tasso di errori durante il posizionamento delle testine magnetiche.",
            "ru": "Частота ошибок позиционирования магнитных головок."
        }
    },
    9: {
        "name": {"en": "Power-On Hours", "it": "Ore Totali di Funzionamento", "ru": "Время работы (часы)"},
        "desc": {
            "en": "Total time spent in active operational power-on state.",
            "it": "Tempo totale di funzionamento attivo del disco.",
            "ru": "Общее количество часов работы накопителя во включенном состоянии."
        }
    },
    10: {
        "name": {"en": "Spin Retry Count", "it": "Tentativi Riavvio Motore Falliti", "ru": "Повторы раскрутки шпинделя"},
        "desc": {
            "en": "Count of failed spindle spin-up attempts. Warning sign of mechanical failure.",
            "it": "Tentativi falliti di avvio del motore di rotazione.",
            "ru": "Количество неудачных попыток раскрутки двигателя шпинделя."
        }
    },
    12: {
        "name": {"en": "Power Cycle Count", "it": "Cicli di Accensione", "ru": "Число циклов включения"},
        "desc": {
            "en": "Count of full power on/off cycles.",
            "it": "Numero di cicli completi di accensione e spegnimento.",
            "ru": "Количество полных циклов включения и выключения накопителя."
        }
    },
    169: {
        "name": {"en": "Remaining Lifetime Perc", "it": "Percentuale Vita Residua Flash", "ru": "Остаточный ресурс SSD (%)"},
        "desc": {
            "en": "Estimated remaining flash memory life percentage.",
            "it": "Percentuale stimata di vita residua del chip flash.",
            "ru": "Оценочный процент оставшегося ресурса флеш-памяти."
        }
    },
    170: {
        "name": {"en": "Available Reserved Space", "it": "Blocchi di Riserva Disponibili", "ru": "Доступный резервный объем"},
        "desc": {
            "en": "Remaining reserved blocks available to replace defective flash memory.",
            "it": "Blocchi di riserva disponibili per sostituire blocchi difettosi.",
            "ru": "Количество резервных блоков для замены сбойных ячеек памяти."
        }
    },
    173: {
        "name": {"en": "Media Wearout Indicator", "it": "Indicatore di Usura Celle Flash", "ru": "Индикатор износа ячеек"},
        "desc": {
            "en": "Wearout indicator of NAND flash memory blocks.",
            "it": "Livello di usura delle celle NAND flash (100 = nuovo, 0 = esaurito).",
            "ru": "Индикатор степени износа ячеек памяти NAND."
        }
    },
    177: {
        "name": {"en": "Wear Range Delta", "it": "Differenza Usura Blocchi Flash", "ru": "Разброс износа блоков"},
        "desc": {
            "en": "Delta between highest and lowest wear erase cycles.",
            "it": "Differenza di usura tra i blocchi flash più e meno consumati.",
            "ru": "Разница циклов стирания между наиболее и наименее изношенными блоками."
        }
    },
    180: {
        "name": {"en": "Unused Reserved Block Count", "it": "Blocchi di Riserva Inutilizzati", "ru": "Неиспользованные резервные блоки"},
        "desc": {
            "en": "Count of spare flash blocks still unused.",
            "it": "Numero di blocchi di riserva flash ancora inutilizzati.",
            "ru": "Количество неиспользованных резервных блоков памяти."
        }
    },
    181: {
        "name": {"en": "Program Fail Count", "it": "Errori di Scrittura Flash", "ru": "Ошибки программирования (записи)"},
        "desc": {
            "en": "Count of flash write/program failures.",
            "it": "Numero di errori di scrittura nei chip di memoria flash.",
            "ru": "Количество ошибок записи в ячейки флеш-памяти."
        }
    },
    182: {
        "name": {"en": "Erase Fail Count", "it": "Errori di Cancellazione Flash", "ru": "Ошибки стирания блоков"},
        "desc": {
            "en": "Count of flash erase failures.",
            "it": "Numero di errori di cancellazione dei blocchi flash.",
            "ru": "Количество ошибок стирания блоков флеш-памяти."
        }
    },
    183: {
        "name": {"en": "Runtime Bad Block Total", "it": "Blocchi Difettosi a Runtime", "ru": "Сбойные блоки во время работы"},
        "desc": {
            "en": "Total defective blocks encountered during operation.",
            "it": "Numero totale di blocchi difettosi rilevati durante il funzionamento.",
            "ru": "Общее количество сбойных блоков, выявленных в процессе работы."
        }
    },
    184: {
        "name": {"en": "End-to-End Error", "it": "Errori di Trasmissione Host-NAND", "ru": "Ошибки сквозной передачи данных"},
        "desc": {
            "en": "Count of data transmission parity errors between controller and memory.",
            "it": "Errori nei dati di passaggio tra controller e memoria flash.",
            "ru": "Ошибки четности при передаче данных между контроллером и памятью."
        }
    },
    187: {
        "name": {"en": "Reported Uncorrectable Errors", "it": "Errori Non Correggibili da ECC", "ru": "Неисправимые ошибки чтения"},
        "desc": {
            "en": "Count of errors that could not be recovered using hardware ECC.",
            "it": "Errori di lettura non corretti dal codice ECC hardware.",
            "ru": "Количество ошибок чтения, которые не удалось восстановить кодом ECC."
        }
    },
    188: {
        "name": {"en": "Command Timeout", "it": "Timeout dei Comandi I/O", "ru": "Таймаут команд I/O"},
        "desc": {
            "en": "Count of aborted operations due to controller communication timeout.",
            "it": "Comandi I/O interrotti a causa di timeout del controller.",
            "ru": "Количество операций, прерванных из-за таймаута контроллера."
        }
    },
    189: {
        "name": {"en": "High Fly Writes", "it": "Scritture con Testina Fuori Quota", "ru": "Запись при смещении головки"},
        "desc": {
            "en": "Count of writes attempted while head flying height was out of bounds.",
            "it": "Tentativi di scrittura con testina non ad altezza ideale.",
            "ru": "Попытки записи при нахождении головки вне допустимой высоты."
        }
    },
    190: {
        "name": {"en": "Airflow Temperature", "it": "Temperatura Flusso d'Aria", "ru": "Температура воздушного потока"},
        "desc": {
            "en": "Internal drive chassis airflow temperature.",
            "it": "Temperatura del flusso d'aria all'interno dell'alloggiamento.",
            "ru": "Температура воздуха внутри корпуса накопителя."
        }
    },
    194: {
        "name": {"en": "Temperature", "it": "Temperatura Operativa", "ru": "Температура"},
        "desc": {
            "en": "Internal sensor operating temperature.",
            "it": "Temperatura operativa rilevata dal sensore interno del disco.",
            "ru": "Рабочая температура, зафиксированная внутренним датчиком."
        }
    },
    195: {
        "name": {"en": "Hardware ECC Recovered", "it": "Errori Corretti tramite ECC", "ru": "Ошибки, исправленные ECC"},
        "desc": {
            "en": "Count of read errors corrected on-the-fly using hardware ECC.",
            "it": "Errori corretti al volo tramite ECC durante la lettura.",
            "ru": "Количество ошибок чтения, успешно исправленных алгоритмом ECC."
        }
    },
    196: {
        "name": {"en": "Reallocation Event Count", "it": "Eventi di Riallocazione Settori", "ru": "События переназначения секторов"},
        "desc": {
            "en": "Count of sector remapping attempts (successful and failed).",
            "it": "Numero di tentativi di riallocazione dei settori difettosi.",
            "ru": "Количество попыток переназначения дефектных секторов."
        }
    },
    197: {
        "name": {"en": "Current Pending Sector Count", "it": "Settori Instabili (Pending)", "ru": "Нестабильные секторы (Pending)"},
        "desc": {
            "en": "Unstable sectors waiting to be remapped upon next write operation.",
            "it": "Settori instabili in attesa di essere riallocati in scrittura.",
            "ru": "Количество нестабильных секторов, ожидающих переназначения."
        }
    },
    198: {
        "name": {"en": "Offline Uncorrectable Sector Count", "it": "Settori Non Correggibili Offline", "ru": "Неисправимые секторы"},
        "desc": {
            "en": "Uncorrectable sectors found during offline SMART scan.",
            "it": "Settori irrecuperabili rilevati durante la scansione offline.",
            "ru": "Неисправимые секторы, обнаруженные при автономном сканировании."
        }
    },
    199: {
        "name": {"en": "UltraDMA CRC Error Count", "it": "Errori di Trasmissione CRC Cavo", "ru": "Ошибки передачи UltraDMA CRC"},
        "desc": {
            "en": "Count of data transmission CRC parity errors on interface cable.",
            "it": "Errori di trasmissione dati sul cavo SATA/interfaccia host.",
            "ru": "Ошибки передачи данных по интерфейсному кабелю SATA."
        }
    },
    202: {
        "name": {"en": "Percent Lifetime Remain", "it": "Percentuale di Vita Residua SSD", "ru": "Остаточный процент жизни SSD"},
        "desc": {
            "en": "Remaining useful lifetime percentage of SSD NAND flash.",
            "it": "Percentuale di vita utile residua dell'SSD.",
            "ru": "Процент оставшегося срока службы твердотельного накопителя."
        }
    },
    231: {
        "name": {"en": "SSD Life Left", "it": "Percentuale Vita Residua SSD", "ru": "Оставшийся ресурс SSD"},
        "desc": {
            "en": "Remaining SSD life percentage reported by vendor.",
            "it": "Percentuale di vita residua stimata dal produttore dell'SSD.",
            "ru": "Процент оставшегося ресурса SSD по данным производителя."
        }
    },
    232: {
        "name": {"en": "Available Reserved Space", "it": "Spazio di Riserva Disponibile", "ru": "Резервное пространство"},
        "desc": {
            "en": "Remaining reserve flash memory space relative to original capacity.",
            "it": "Spazio di riserva SSD ancora disponibile rispetto all'inizio.",
            "ru": "Оставшийся резервный объем флеш-памяти."
        }
    },
    233: {
        "name": {"en": "Media Wearout Indicator", "it": "Indicatore di Usura Supporto Flash", "ru": "Износ носителя (Media Wearout)"},
        "desc": {
            "en": "Wearout indicator of NAND flash memory blocks.",
            "it": "Indicatore di usura del supporto flash NAND.",
            "ru": "Индикатор износа ячеек флеш-памяти."
        }
    },
    240: {
        "name": {"en": "Head Flying Hours", "it": "Ore Posizionamento Testine", "ru": "Время позиционирования головок"},
        "desc": {
            "en": "Total hours spent with magnetic head in active positioning state.",
            "it": "Ore di posizionamento attivo delle testine magnetiche.",
            "ru": "Количество часов активного перемещения магнитных головок."
        }
    },
    241: {
        "name": {"en": "Total LBAs Written", "it": "Totale Settori Scritti (LBAs)", "ru": "Всего секторов записано (LBAs)"},
        "desc": {
            "en": "Total number of LBAs written by host (Host Writes).",
            "it": "Quantità totale di settori scritti dall'host (Host Writes).",
            "ru": "Общий объем секторов, записанных хостом."
        }
    },
    242: {
        "name": {"en": "Total LBAs Read", "it": "Totale Settori Letti (LBAs)", "ru": "Всего секторов прочитано (LBAs)"},
        "desc": {
            "en": "Total number of LBAs read by host (Host Reads).",
            "it": "Quantità totale di settori letti dall'host (Host Reads).",
            "ru": "Общий объем секторов, прочитанных хостом."
        }
    }
}

NVME_DESCRIPTIONS = {
    "Critical Warning": {
        "name": {"en": "Critical Warning", "it": "Avvisi Critici di Sistema", "ru": "Критические предупреждения"},
        "desc": {
            "en": "Critical system warnings (temperature, spare degradation, NVM subsystem errors).",
            "it": "Avvisi di sistema critici (temperatura, usura riserva, errori controller).",
            "ru": "Критические предупреждения контроллера (температура, деградация резерва, сбои)."
        }
    },
    "Composite Temperature": {
        "name": {"en": "Composite Temperature", "it": "Temperatura Composta", "ru": "Составная температура"},
        "desc": {
            "en": "Current overall controller and flash memory temperature.",
            "it": "Temperatura operativa complessiva di controller e memoria.",
            "ru": "Текущая общая температура контроллера и чипов памяти."
        }
    },
    "Available Spare": {
        "name": {"en": "Available Spare", "it": "Blocchi di Riserva Disponibili", "ru": "Доступный резервный объем"},
        "desc": {
            "en": "Percentage of remaining spare flash capacity available for wear leveling and defects.",
            "it": "Percentuale di blocchi di riserva disponibili per rimpiazzo celle usurate.",
            "ru": "Процент оставшегося резервного объема памяти для замены изношенных ячеек."
        }
    },
    "Available Spare Threshold": {
        "name": {"en": "Available Spare Threshold", "it": "Soglia Minima Riserva", "ru": "Порог резервного объема"},
        "desc": {
            "en": "Low-spare alert threshold configured by drive vendor.",
            "it": "Soglia minima di sicurezza per i blocchi di riserva.",
            "ru": "Минимальный порог резервного объема, установленный производителем."
        }
    },
    "Percentage Used": {
        "name": {"en": "Percentage Used", "it": "Percentuale di Vita Consumata", "ru": "Процент износа (Percentage Used)"},
        "desc": {
            "en": "Estimated percentage of NVM subsystem life consumed based on vendor endurance rating.",
            "it": "Percentuale stimata di vita utile del disco consumata in base alle specifiche di durata.",
            "ru": "Оценочный процент износа накопителя на основе заявленного ресурса перезаписи."
        }
    },
    "Data Units Read": {
        "name": {"en": "Data Units Read", "it": "Unità Dati Lette", "ru": "Прочитано единиц данных"},
        "desc": {
            "en": "Total volume of data read by host (1 unit = 512,000 bytes).",
            "it": "Volume totale di dati letti dall'host (1 unità = 512.000 byte).",
            "ru": "Общий объем данных, прочитанных хостом (1 единица = 512 000 байт)."
        }
    },
    "Data Units Written": {
        "name": {"en": "Data Units Written", "it": "Unità Dati Scritte", "ru": "Записано единиц данных"},
        "desc": {
            "en": "Total volume of data written by host (1 unit = 512,000 bytes).",
            "it": "Volume totale di dati scritti dall'host (1 unità = 512.000 byte).",
            "ru": "Общий объем данных, записанных хостом (1 единица = 512 000 байт)."
        }
    },
    "Host Read Commands": {
        "name": {"en": "Host Read Commands", "it": "Comandi di Lettura Host", "ru": "Команды чтения хоста"},
        "desc": {
            "en": "Total count of read I/O commands processed by the controller.",
            "it": "Numero totale di comandi di lettura elaborati dal controller.",
            "ru": "Общее количество команд чтения, обработанных контроллером."
        }
    },
    "Host Write Commands": {
        "name": {"en": "Host Write Commands", "it": "Comandi di Scrittura Host", "ru": "Команды записи хоста"},
        "desc": {
            "en": "Total count of write I/O commands processed by the controller.",
            "it": "Numero totale di comandi di scrittura elaborati dal controller.",
            "ru": "Общее количество команд записи, обработанных контроллером."
        }
    },
    "Controller Busy Time": {
        "name": {"en": "Controller Busy Time", "it": "Tempo di Attività Controller", "ru": "Время занятости контроллера"},
        "desc": {
            "en": "Total duration in minutes where the controller was actively processing I/O commands.",
            "it": "Minuti complessivi in cui il controller era attivamente impegnato in comandi I/O.",
            "ru": "Общее время в минутах, в течение которого контроллер обрабатывал команды."
        }
    },
    "Power Cycles": {
        "name": {"en": "Power Cycles", "it": "Cicli di Alimentazione", "ru": "Циклы включения"},
        "desc": {
            "en": "Total count of power on/off cycles.",
            "it": "Numero di cicli di accensione e spegnimento del dispositivo.",
            "ru": "Общее число циклов включения и выключения накопителя."
        }
    },
    "Power On Hours": {
        "name": {"en": "Power On Hours", "it": "Ore di Accensione", "ru": "Время во включенном состоянии"},
        "desc": {
            "en": "Total active power-on hours.",
            "it": "Ore totali di attività e alimentazione del disco.",
            "ru": "Общее количество часов работы накопителя."
        }
    },
    "Unsafe Shutdowns": {
        "name": {"en": "Unsafe Shutdowns", "it": "Spegnimenti Non Sicuri", "ru": "Небезопасные отключения"},
        "desc": {
            "en": "Count of power loss events without prior shutdown notification to controller.",
            "it": "Numero di spegnimenti improvvisi senza preventiva notifica di arresto.",
            "ru": "Количество внезапных отключений питания без предварительного уведомления."
        }
    },
    "Media and Data Errors": {
        "name": {"en": "Media and Data Errors", "it": "Errori di Integrità Media Flash", "ru": "Ошибки носителя и данных"},
        "desc": {
            "en": "Count of unrecoverable flash integrity errors and uncorrected ECC failures.",
            "it": "Errori di integrità del supporto flash e recupero ECC non riuscito.",
            "ru": "Количество неисправимых ошибок целостности флеш-памяти и ECC."
        }
    },
    "Error Log Entries": {
        "name": {"en": "Error Log Entries", "it": "Voci nel Registro Errori", "ru": "Записи в журнале ошибок"},
        "desc": {
            "en": "Total number of error information log entries recorded by the controller.",
            "it": "Numero di voci registrate nel registro errori interno del controller.",
            "ru": "Общее количество записей в журнале ошибок контроллера."
        }
    }
}


def tr(key: str, **kwargs) -> str:
    lang_dict = TRANSLATIONS.get(current_language, TRANSLATIONS["en"])
    text = lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text


def get_translated_attribute(attr_id: int, original_name: str, original_desc: str = "") -> tuple[str, str]:
    for nvme_key, entry in NVME_DESCRIPTIONS.items():
        if nvme_key.lower() in original_name.lower() or original_name.lower() in nvme_key.lower():
            name = entry["name"].get(current_language, original_name)
            desc = entry["desc"].get(current_language, original_desc)
            return name, desc

    if attr_id in SMART_DESCRIPTIONS:
        entry = SMART_DESCRIPTIONS[attr_id]
        name = entry["name"].get(current_language, original_name)
        desc = entry["desc"].get(current_language, original_desc)
        return name, desc

    for s_id, entry in SMART_DESCRIPTIONS.items():
        en_name = entry["name"].get("en", "")
        if en_name and (en_name.lower() in original_name.lower() or original_name.lower() in en_name.lower()):
            name = entry["name"].get(current_language, original_name)
            desc = entry["desc"].get(current_language, original_desc)
            return name, desc

    return original_name, original_desc
