import time
import math
import re
import shelve
import json

temp = 0

print ("""
  _   __              _     _______     _______     ______  
 / |_[  |            / |_  |_   __ \   |_   __ \  .' ___  | 
`| |-'| |--.   ,--. `| |-'   | |__) |    | |__) |/ .'   \_|
 | |  | .-. | `'_\ : | |     |  __ /     |  ___/ | |   ____ 
 | |, | | | | // | |,| |,   _| |  \ \_  _| |_    \ `.___]  |
 \__/[___]|__]\'-;__/\__/  |____| |___||_____|    `._____.' 
""")


#ITEMS
class gun:
    def __init__(gun, stacksize, magwell, reichweite, damage, hands, accuracy, caliber, rp, descrip):
        gun.stacksize = stacksize
        gun.magwell = magwell
        gun.reichweite = reichweite
        gun.damage = damage
        gun.hands = hands
        gun.accuracy = accuracy
        gun.caliber = caliber
        gun.rp = rp
    
    def __str__(gun):
        return (f'{gun.magwell}+{gun.damage}+{gun.caliber}')

ar15 = gun(1, "ar", 200, 500, 2, 100, 5.56, 500, "default")

class NotGun:
    def __init__(NotGun, stacksize, speed, atk, block, hands, rp, descrip):
        NotGun.stacksize = stacksize
        NotGun.speed = speed
        NotGun.atk = atk
        NotGun.block = block
        NotGun.hands = hands
        NotGun.rp = rp
        NotGun.descrip = descrip
        
    def __str__(NotGun):
        return (f'stacksize: {NotGun.stacksize}   speed: {NotGun.speed}   atk: {NotGun.atk}    rp: {NotGun.rp}   {NotGun.descrip}')
    
club = NotGun(2, 10, 10, 5, 2, 33, "stück holz")
        
class mag:
    def __init__(mag, stacksize, capacity, magwell, caliber):
        mag.stacksize = stacksize
        mag.capacity = capacity
        mag.magwell = magwell
        mag.caliber = caliber
    def __str__(mag):
        return (f'{mag.stacksize}+{mag.capacity}+{mag.magwell}+{mag.caliber}')
    
class consumables:
    def __init__(consumables, stacksize, heal, saturation, poison, descrip):
        consumables.heal = heal
        consumables.saturation = saturation
        consumables.poison = poison
    
    def __str__(consumables):
        return (f'{consumables.saturation}')
    
class armor:
    def __init__(armor, stacksize, rp, protGun, protSharp, protBlunt, descrip):
        armor.stacksize = stacksize
        armor.rp = rp
        armor.protGun = protGun
        armor.protSharp = protSharp
        armor.protBlunt = protBlunt
        
    def __str__(armor):
        return (f'{armor.protGun}+{armor.protBlunt}+{armor.protSharp}+{armor.rp}')
    
class crafting:
    def __init__(craft, stacksize, descrip):
        craft.stacksize = stacksize

#    def __str__()

stick = crafting(20, "kleines stück holz")

apfelTX = str("""                                                  
                                                  
                                                  
                                                  
                                                  
                                                  
                    @                             
                    %@                            
                     @                            
                   .  @ .+%#*:  .  .              
                 -*#@#=-=*.:=+%#%@                
            . =*#*.+ .@@=....  --##@   .          
             *+. .:..-...=*%=*=%@+#%@  .          
         . *:...:....+-#.=*-*#=@-*#@#@            
         . =.:-.... ..  : :*#:**=+-+%#@           
         . -=-........ -:.*-+%=%%@-%%%@           
         . ==:.:::::::..:*-.@+=-*.+##%%           
         . #=-::=..:...-.+-*:-*%%@#%@%@           
         . -++..:-::=:.+-=-+:+:-#:@%#@            
         .  :*+=*-=.:.:#.+.#@=%%#%%%%  .          
            . @=++=**###=*#%#%%@@#%% . .          
               +@++-=%*:+@+#%%@@@#@               
                 @@@@%@%#@%@@@@@@                 
                     @@@@@@@@                     
                              . .                 
                                                  
                                                  
                                                  
                                                  
                                                  """)

eimerTX = str()


status = {
    "gesundheit" : 100,
    "movementkram" : 100,
    "hunger" : 0
}

stats = {
    "strength" : 0,
    "speed" : 0,
    "endurance" : 0,
    "intelligence" : 0,
    "charisma" : 0,
    "maxHP" : 100
}

inventar = {
    "ar15" : (1, "ar", 200, 500, 2, 100, 5.56, 500),
    "stick" : (20)
}

inventarQa = {
    "ar15" : 1,
    "stick" : 2,
    "club" : 0
}

RecipesHidden = {
    "stick+stick" : ("club")
}

class NPC:
    def __init__(NPC, HP, aggro, like, power):
        NPC.HP = HP
        NPC.aggro = aggro
        NPC.like = like
        NPC.power = power

name = input('Name:')

def load():
    try:
        with open("save.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        status = data["status"]
        inventar = data["inventar"]
        inventarQa = data["inventaQa"]
        stats = data["stats"]
        print ("geladen")
        return status, inventar, inventarQa, stats, main()
    except FileNotFoundError:
        print("keine File")
        return main()

import json
import os

def save(status, inventar, inventarQa, stats):
    """
    Speichert die Spieldaten sicher in save.json
    """
    try:
        # Daten vorbereiten
        data = {
            "status": status,
            "inventar": inventar,
            "inventarQa": inventarQa,
            "stats": stats,
        }
        
        # Backup der alten Datei falls vorhanden
        if os.path.exists("save.json"):
            try:
                os.rename("save.json", "save_backup.json")
            except:
                pass  # Backup fehlgeschlagen, aber weitermachen
        
        # Speichern mit absoluten Pfad für Sicherheit
        save_path = os.path.join(os.getcwd(), "save.json")
        
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        # Erfolgreich gespeichert - Backup löschen
        if os.path.exists("save_backup.json"):
            try:
                os.remove("save_backup.json")
            except:
                pass
        
        print("✓ Erfolgreich gespeichert!")
        print(f"Datei: {save_path}")
        
        # Verifikation
        if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
            print(f"✓ Datei erstellt ({os.path.getsize(save_path)} Bytes)")
        else:
            print("⚠ Warnung: Datei scheint leer oder nicht erstellt zu sein")
            
    except PermissionError:
        print("❌ Fehler: Keine Berechtigung zum Schreiben in diesem Ordner")
        print(f"Aktueller Ordner: {os.getcwd()}")
        
        # Alternativer Speicherort versuchen
        try:
            alt_path = os.path.join(os.path.expanduser("~"), "save.json")
            with open(alt_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"✓ Alternative gespeichert in: {alt_path}")
        except:
            print("❌ Auch alternativer Speicherort fehlgeschlagen")
            
    except json.JSONEncoder.JSONError as e:
        print(f"❌ JSON-Fehler: Die Daten können nicht als JSON gespeichert werden")
        print(f"Fehler: {e}")
        print("Prüfe ob alle Variablen JSON-serialisierbar sind (keine Funktionen, Klassen etc.)")
        
    except Exception as e:
        print(f"❌ Unerwarteter Fehler beim Speichern: {e}")
        
        # Backup wiederherstellen falls vorhanden
        if os.path.exists("save_backup.json"):
            try:
                os.rename("save_backup.json", "save.json")
                print("Backup wiederhergestellt")
            except:
                print("Backup konnte nicht wiederhergestellt werden")


def load_save():
    """
    Lädt die gespeicherten Daten
    """
    try:
        if os.path.exists("save.json"):
            with open("save.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            print("✓ Spieldaten geladen")
            return data
        else:
            print("Keine Speicherdatei gefunden")
            return None
            
    except json.JSONDecodeError:
        print("❌ Speicherdatei ist beschädigt")
        
        # Backup versuchen
        if os.path.exists("save_backup.json"):
            try:
                with open("save_backup.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                print("✓ Backup-Datei geladen")
                return data
            except:
                print("❌ Auch Backup ist beschädigt")
        
        return None
        
    except Exception as e:
        print(f"❌ Fehler beim Laden: {e}")
        return None


# Beispiel für saubere Programmstruktur ohne Rekursion:
def main():
    """
    Hauptprogramm - Beispiel wie es strukturiert werden könnte
    """
    # Initialisierung
    status = {"level": 1, "health": 100}
    inventar = ["schwert", "schild"]
    inventarQa = {"schwert": 1, "schild": 1}
    stats = {"kills": 0, "deaths": 0}
    
    # Gespeicherte Daten laden falls vorhanden
    saved_data = load_save()
    if saved_data:
        status = saved_data.get("status", status)
        inventar = saved_data.get("inventar", inventar)
        inventarQa = saved_data.get("inventarQa", inventarQa)
        stats = saved_data.get("stats", stats)
    
    # Hauptspiel-Loop
    while True:
        print("\n=== SPIEL MENÜ ===")
        print("1. Spielen")
        print("2. Speichern")
        print("3. Beenden")
        
        choice = input("Wähle: ")
        
        if choice == "1":
            print("Spiel läuft...")
            # Hier würde dein Spielcode stehen
            
        elif choice == "2":
            save(status, inventar, inventarQa, stats)
            
        elif choice == "3":
            # Vor dem Beenden speichern?
            save_before_exit = input("Vor dem Beenden speichern? (j/n): ")
            if save_before_exit.lower() == 'j':
                save(status, inventar, inventarQa, stats)
            break
            
        else:
            print("Ungültige Eingabe")


if __name__ == "__main__":
    main()

def main():
    T = input("mainmenu:")
    if (T == 'i'):
        T = None
        return inventarui()
    if (T == 'm'):
        T = None
        return MAP()    #niy
    if (T == 'c'):
        T = None
        return combat() #niy
    if (T == 'w'):
        T = None
        return world()  #niy
    if (T == 's'):
        T = None
        return save(status, inventar, inventarQa, stats)
    if (T == 'l'):
        T = None
        return load()

def inventarui():
    print (inventar.keys())
    T = input("c oder q:")
    if (T == 'c'):
        T = 0
        return crafting()
    if (T == 'e'):
        T = 0
        return equipment()  #niy
    if (T == 'q'):
        T = 0
        return main()
    
def crafting():
    T = input("t, k oder q")
    if (T == 't'):
        T = 0
        return kombinieren()
    if (T == 'k'):
        T = 0
        return rezepte()    #niy
    if (T == 'q'):
        T = 0
        return inventarui()
        
def kombinieren():
    T = input("zutaten oder q:")
    if (T == ('q')):
        T = 0
        return crafting()
    print (inventarQa)
    Z1 = input("erste Zutat: ")
    templist = inventarQa[Z1]
    if inventarQa[Z1] < 1:
        print ("fehler")
        return kombinieren()
    templist = templist - 1
    Z2 = input("zweite Zutat: ")
    if templist < 1:
        print ("fehler")
        templist = 0
        return kombinieren
    temp = (f'{Z1}+{Z2}')
    templist = 0
    if f'{temp}' in RecipesHidden:
        inventarQa[Z1] = inventarQa[Z1] - 1
        inventarQa[Z2] = inventarQa[Z2] - 1
        print (RecipesHidden[temp]+{RecipesHidden[temp]})
        inventarQa[RecipesHidden[temp]] = inventarQa[RecipesHidden[temp]] + 1
        return kombinieren()   
    if f'{temp}' not in RecipesHidden:
        print ("not valid")
        return kombinieren()

inventarui()