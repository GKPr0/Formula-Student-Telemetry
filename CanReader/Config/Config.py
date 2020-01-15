from configparser import ConfigParser
import os

# TODO Předělat na object Config
CONFIGFILE_NAME = "config_file.ini"

# Vytvoří config file, pokud  neexistuje
if not os.path.isfile(CONFIGFILE_NAME):
    configfile = open(CONFIGFILE_NAME,"w")
    configfile.close()

config = ConfigParser()
config.read(CONFIGFILE_NAME)

def save_config():  # Přepíše config se všemi změny
    with open(CONFIGFILE_NAME, "w") as configfile:
        config.write(configfile)

def update_section_in_config(ID): # Aktualizuje parametry v už existující sekci
    # TODO Doplnit možnost updatu v případě potřeby podle ID
    save_config()

def load_from_config_file(): # do objekt proměnné načte všechny parametry podle
    # TODO Načítení celého configu do objektů
    pass