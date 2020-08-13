hauptaggregate = [
    "Gesamtenergiebilanz",
    "ERNEUERBARE",
    "Elektrische Energie",
    "Brennbare Abfälle",
    "KOHLE",
    "ÖL",
    "GAS",
    "Fernwärme",
]

erneuerbare = [
    "ERNEUERBARE",
    "Wasserkraft",
    "Wind",
    "Photovoltaik",
    "Wind und Photovoltaik",
    "Geothermie",
    "Solarwärme",
]

fossil_fest = [
    "Steinkohle",
    "Braunkohle",
    "Braunkohlen-Briketts",
    "Brenntorf",
    "Koks",
    "Industrieabfall",
    "Hausmüll nicht erneuerbar",
]

fossil_flüssig = [
    "Erdöl",
    "Sonstiger Raffinerieeinsatz",
    "Benzin",
    "Petroleum",
    "Diesel",
    "Gasöl für Heizzwecke",
    "Heizöl",
    "Flüssiggas",
    "Sonstige Prod. d. Erdölverarb.",
]

fossil_gasförmig = [
    "Raffinerie-Restgas",
    "Mischgas",
    "Erdgas",
    "Gichtgas",
    "Kokereigas",
]

biogen_fest = [
    "Scheitholz",
    "Pellets+Holzbriketts",
    "Holzabfall",
    "Holzkohle",
    "Ablaugen",
    "Hausmüll Bioanteil",
    "Sonst. Biogene fest",
    "Brennbare Abfälle",
]

biogen_flüssig = [
    "Bioethanol",
    "Biodiesel",
    "Sonst. Biogene flüssig",
]

biogen_gasförmig = [
    "Deponiegas",
    "Klärgas",
    "Biogas"
]

umgebungswärme = [
    "Geothermie",
    "Umgebungswärme",
    "Solarwärme",
    "Reaktionswärme",
]

wasserkraft = [
    "WK<=1MW",
    "WK<=10MW",
    "WK>10MW",
]

abfall = [
    "Brennbare Abfälle",
    "Industrieabfall",
    "Hausmüll Bioanteil",
    "Hausmüll nicht erneuerbar",
]


energy_sources_aggregates = {
    "Hauptaggregate": hauptaggregate,
    "Elektrische Energie": ["Elektrische Energie"],
    "Erneuerbare": erneuerbare,
    "Fossil-fest": fossil_fest,
    "Fossil-flüssig": fossil_flüssig,
    "Fossil-gasförmig": fossil_gasförmig,
    "Biogen-fest": biogen_fest,
    "Biogen-flüssig": biogen_flüssig,
    "Biogen-gasförmig": biogen_gasförmig,
    "Umgebungswärme": umgebungswärme,
    "Wasserkraft": wasserkraft,
    "Abfall": abfall,
}

# Deponiegas	Biogen - gasformig
# Klärgas	Biogen - gasformig
# Biogas	Biogen - gasformig
# Bioethanol	Biogen - flüssig
# Biodiesel	Biogen - flüssig
# Sonst. Biogene flüssig	Biogen - flüssig
# Sonst. Biogene fest	Biogen - fest
