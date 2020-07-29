def rgb2hex(rgb: tuple) -> str:
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


# ______________________________________________ Allgemein

# AEA Rot

AEA_red_rgb = (206, 50, 26)  # ce321a
# Kontrastfarbe Grün
AEA_green_rgb = (20, 140, 50)  # 148C32
# Schriftfarbe
AEA_font_color_rgb = (50, 50, 50)  # 323232
# Hintergrundlinien
AEA_background_lines_rgb = (191, 191, 191)  # BFBFBF

# ______________________________________________ Energieträger

# CO2-Emissionen
AEA_CO2_emissions_rgb = (101, 101, 101)
# Fossile Energie
AEA_fossile_energy_rgb = (50, 32, 24)
# Kohle
AEA_coal_rgb = (101, 101, 101)
# Erdöl
AEA_oil_rgb = (88, 7, 79)
# Erdgas
AEA_gas_rgb = (255, 192, 0)
# Nuklear
AEA_nuclear_rgb = (0, 61, 94)
# Heizöl
AEA_fuel_oil_rgb = (100, 65, 50)
# Erneuerbare Energien
AEA_VRES_rgb = (20, 140, 50)
# Photovoltaik
AEA_photovoltaic_rgb = (190, 200, 0)
# Wasser
AEA_hydro_rgb_ = (0, 125, 190)
# Wind
AEA_wind_rgb = (125, 209, 255)
# Biomasse
AEA_biomass_rgb = (10, 69, 24)
# Biogas
AEA_biogas_rgb = (133, 237, 159)
# Abfall
AEA_waste_rgb = (230, 100, 0)
# Umgebungswärme
AEA_ambient_heat_rgb = (236, 122, 106)
# Fernwärme
AEA_district_heating_rgb = (183, 132, 111)
# Strom
AEA_electricity_rgb = (165, 0, 0)
# Sonstiges
AEA_misc_rgb = (128, 128, 128)

# ______________________________________________ Verkehr
# Benzin
AEA_petrol_rgb = (58, 5, 52)
# Diesel
AEA_diesel_rgb = (255, 157, 85)
# Strom
AEA_electricity_rgb = (165, 0, 0)

# ______________________________________________ Sektoren
# Industrie
AEA_industry_rgb = (230, 100, 0)
# Haushalte
AEA_households_rgb = (206, 50, 26)
# Dienstleistungen
AEA_services_rgb = (255, 192, 0)
# Landwirtschaft
AEA_agriculture_rgb = (20, 140, 50)
# Verkehr
AEA_transportation_rgb = (0, 125, 190)

# ______________________________________________ Bundesländer
provinces_color_table = {
    "AT": rgb2hex(rgb=(0, 0, 0)),
    "Bgd": rgb2hex(rgb=(255, 165, 0)),
    "Ktn": rgb2hex(rgb=(192, 0, 0)),
    "Noe": rgb2hex(rgb=(0, 176, 240)),
    "Ooe": rgb2hex(rgb=(191, 143, 0)),
    "Sbg": rgb2hex(rgb=(112, 48, 160)),
    "Stk": rgb2hex(rgb=(84, 130, 53)),
    "Tir": rgb2hex(rgb=(31, 76, 120)),
    "Vbg": rgb2hex(rgb=(123, 123, 123)),
    "Wie": rgb2hex(rgb=(144, 183, 107)),
}

provinces_color_table_rgba = {
    "AT": (0, 0, 0, 0.5),
    "Bgd": (255, 165, 0, 0.5),
    "Ktn": (192, 0, 0, 0.5),
    "Noe": (0, 176, 240, 0.5),
    "Ooe": (191, 143, 0, 0.5),
    "Sbg": (112, 48, 160, 0.5),
    "Stk": (84, 130, 53, 0.5),
    "Tir": (31, 76, 120, 0.5),
    "Vbg": (123, 123, 123, 0.5),
    "Wie": (144, 183, 107, 0.5)
}

provinces_color_table_rgb = {
    "AT": (0, 0, 0),
    "Bgd": (0, 125, 190),  # hellblau
    "Ktn": (82, 0, 0),  # dunkelrot
    "Noe": (165, 0, 0),  # rot
    "Ooe": (230, 100, 0),  # orange
    "Sbg": (190, 200, 0),  # limette
    "Stk": (84, 130, 53),  # grün
    "Tir": (10, 70, 25),  # dunkelgrün
    "Vbg": (100, 65, 50),  # braun
    "Wie": (205, 16, 118),  # deeppink
}
