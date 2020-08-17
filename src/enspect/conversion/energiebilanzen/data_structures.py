eb_sheet_names = [
    "Kokskohle",
    "Anthrazit",
    "Steinkohlen-Briketts",
    "Sonstige Steinkohle",
    "Steinkohle",
    "Subbituminöse Kohle",
    "Sonstige Braunkohle",
    "Braunkohle",
    "Braunkohlen-Briketts",
    "Brenntorf",
    "Koks",
    "Rohöl",
    "NGL",
    "Erdöl",
    "Steinkohleteer",
    "Benzol",
    "Feedstocks",
    "Sonstiger Raffinerieeinsatz",
    "Motorbenzin",
    "Industriebenzin",
    "Flugbenzin",
    "Benzin",
    "Flugturbinenkraftstoff",
    "Sonstiges Petroleum",
    "Petroleum",
    "Diesel",
    "Gasöl für Heizzwecke",
    "Heizöl<1%S",
    "Heizöl>1%S",
    "Heizöl",
    "Flüssiggas",
    "Naphta",
    "Bitumen",
    "Schmiermittel",
    "Petrolkoks",
    "Sonstige",
    "Sonstige Prod. d. Erdölverarb.",
    "Raffinerie-Restgas",
    "Mischgas",
    "Erdgas",
    "Tiegelgas",
    "Hochofengas",
    "Gichtgas",
    "Kokereigas",
    "Industrieabfall",
    "Hausmüll nicht erneuerbar",
    "Brennbare Abfälle",
    "Scheitholz",
    "Hausmüll Bioanteil",
    "Pellets+Holzbriketts",
    "Holzabfall",
    "Holzkohle",
    "Ablaugen",
    "Deponiegas",
    "Klärgas",
    "Biogas",
    "Bioethanol",
    "Biodiesel",
    "Sonst. Biogene flüssig",
    "Sonst. Biogene fest",
    "Biogene Brenn- u. Treibstoffe",
    "Geothermie",
    "Umgebungswärme",
    "Solarwärme",
    "Reaktionswärme",
    "Umgebungswärme etc.",
    "WK<=1MW",
    "WK<=10MW",
    "WK>10MW",
    "Wasserkraft",
    "Wind",
    "Photovoltaik",
    "Wind und Photovoltaik",
    "Fernwärme",
    "Elektrische Energie",
    "KOHLE",
    "ÖL",
    "GAS",
    "ERNEUERBARE",
    "ABFÄLLE",
    "Gesamtenergiebilanz",
]

# ///////////////////////////////////////////////////// ENERGY SOURCE AGGREGATES

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

biogen_gasförmig = ["Deponiegas", "Klärgas", "Biogas"]

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

# //////////////////////////////////////////////// BALANCE AGGREGATES PER PICKLE
# Includes the first balance aggregates including "Energetischer
# Endverbrauch"
eev_aggregates = [
    "Inländ. Erzeugung v. Rohenergie",
    "Importe",
    "Lager",
    "Recycling/Prod. Trans.",
    "Exporte",
    "Bruttoinlandsverbrauch",
    "Umwandlungseinsatz",
    "Umwandlungsausstoß",
    "Verbrauch des Sektors Energie",
    "Transportverluste",
    "Nichtenergetischer Verbrauch",
    "Energetischer Endverbrauch",
]

# "Energetischer Endverbrauch, Verbrauch der Sektoren"
sectors = [
    "Eisen- und Stahlerzeugung",
    "Chemie und  Petrochemie",
    "Nicht Eisen Metalle",
    "Steine und Erden, Glas",
    "Fahrzeugbau",
    "Maschinenbau",
    "Bergbau",
    "Nahrungs- und Genußmittel, Tabak",
    "Papier und Druck",
    "Holzverarbeitung",
    "Bau",
    "Textil und Leder",
    "Sonst. Produzierender Bereich",
    "Eisenbahn",
    "Sonstiger Landverkehr",
    "Transport in Rohrfernleitungen",
    "Binnenschiffahrt",
    "Flugverkehr",
    "Öffentliche und Private Dienstleistungen",
    "Private Haushalte",
    "Landwirtschaft",
    "Produzierender Bereich",
    "Verkehr",
    "Sonstige",
]
# "Energetischer Endverbrauch, Verbrauch der Sektor Energie"
sector_energy = [
    "Gewinnung von Erdöl und Erdgas",
    "Kohlenbergbau",
    "Mineralölverarbeitung",
    "Kokerei",
    "Hochofen",
    "Energieversorgung (Elektrizität, Erdgas, Fernwärme)",
]
