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

def save(status, inventar, inventarQa, stats):
    data = {
        "status": status,
        "inventar": inventar,
        "inventarQa": inventarQa,
        "stats": stats
    }
    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Spiel gespeichert.")

def load():
    try:
        with open("save.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        global status, inventar, inventarQa, stats
        status = data["status"]
        inventar = data["inventar"]
        inventarQa = data["inventarQa"]
        stats = data["stats"]
        print("Spielstand geladen.")
    except FileNotFoundError:
        print("Keine Speicherdatei gefunden.")
        return main()


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
        print (temp+"="+RecipesHidden[temp])
        inventarQa[RecipesHidden[temp]] = inventarQa[RecipesHidden[temp]] + 1
        return kombinieren()   
    if f'{temp}' not in RecipesHidden:
        print ("not valid")
        return kombinieren()

inventarui()