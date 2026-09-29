ATTRIBUTE_DESCRIPTIONS = {
    1: ("Read Error Rate", "Frequenza di errori hardware durante la lettura da disco.", "warning_if_high"),
    5: ("Reallocated Sectors Count", "Numero di settori danneggiati spostati nell'area di riserva. Valori crescenti indicano degrado fisico.", "critical_if_high"),
    9: ("Power-On Hours", "Tempo totale di funzionamento attivo del disco.", "info"),
    10: ("Spin Retry Count", "Tentativi di avvio del motore falliti. Tipico sintomo di guasto meccanico imminente.", "critical_if_high"),
    12: ("Power Cycle Count", "Numero di cicli di accensione e spegnimento del dispositivo.", "info"),
    169: ("Remaining Lifetime Perc", "Percentuale stimata di vita residua del chip di memoria flash.", "life_indicator"),
    170: ("Available Reserved Space", "Quantità di blocchi di riserva rimasti per sostituire blocchi flash guasti.", "life_indicator"),
    173: ("Media Wearout Indicator", "Livello di usura delle celle NAND flash (100 = nuovo, 0 = esaurito).", "life_indicator"),
    177: ("Wear Range Delta", "Differenza tra i blocchi flash più consumati e quelli meno consumati.", "life_indicator"),
    180: ("Unused Reserved Block Count", "Numero di blocchi di riserva inutilizzati.", "life_indicator"),
    181: ("Program Fail Count", "Numero di errori di scrittura nei chip flash.", "warning_if_high"),
    182: ("Erase Fail Count", "Numero di errori di cancellazione dei blocchi flash.", "warning_if_high"),
    183: ("Runtime Bad Block Total", "Numero totale di blocchi difettosi rilevati durante il funzionamento.", "warning_if_high"),
    184: ("End-to-End Error", "Errori nei dati di passaggio tra host e memoria flash.", "critical_if_high"),
    187: ("Reported Uncorrectable Errors", "Errori di lettura che non sono stati corretti dal codice ECC hardware.", "critical_if_high"),
    188: ("Command Timeout", "Comandi I/O interrotti a causa di timeout del controller.", "warning_if_high"),
    189: ("High Fly Writes", "Testina di scrittura non allineata ad altezza ideale (HDD).", "warning_if_high"),
    190: ("Airflow Temperature", "Temperatura del flusso d'aria all'interno dell'alloggiamento.", "temp"),
    194: ("Temperature", "Temperatura operativa rilevata dal sensore interno del disco.", "temp"),
    195: ("Hardware ECC Recovered", "Errori corretti al volo tramite ECC durante la lettura.", "info"),
    196: ("Reallocation Event Count", "Numero di eventi/tentativi di riallocazione dei settori difettosi.", "warning_if_high"),
    197: ("Current Pending Sector Count", "Settori 'instabili' in attesa di essere riallocati in scrittura.", "critical_if_high"),
    198: ("Offline Uncorrectable Sector Count", "Settori irrecuperabili rilevati durante la scansione offline.", "critical_if_high"),
    199: ("UltraDMA CRC Error Count", "Errori di trasmissione dati sul cavo SATA/interfaccia host.", "warning_if_high"),
    202: ("Percent Lifetime Remain", "Percentuale di vita utile residua dell'SSD.", "life_indicator"),
    231: ("SSD Life Left", "Percentuale di vita residua stimata dal produttore dell'SSD.", "life_indicator"),
    232: ("Available Reserved Space", "Spazio di riserva SSD ancora disponibile rispetto all'inizio.", "life_indicator"),
    233: ("Media Wearout Indicator", "Indicatore di usura del supporto flash NAND.", "life_indicator"),
    240: ("Head Flying Hours", "Ore di posizionamento attivo delle testine magnetiche.", "info"),
    241: ("Total LBAs Written", "Quantità totale di settori/dati scritti dall'host (Host Writes).", "info"),
    242: ("Total LBAs Read", "Quantità totale di settori/dati letti dall'host (Host Reads).", "info"),
}


def get_attribute_info(attr_id: int, name: str = ""):
    if attr_id in ATTRIBUTE_DESCRIPTIONS:
        desc_name, desc_text, cat = ATTRIBUTE_DESCRIPTIONS[attr_id]
        return desc_name or name, desc_text, cat
    return name, "Attributo SMART standard.", "info"
