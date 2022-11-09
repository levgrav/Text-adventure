import os
import resources.entities as entities
import resources.quests as quests
import resources.things as things
import resources.database.db as db
import controlers.gamestate_control as gsc
find = things.find_item_in
find_room = things.find_room
# ---Functions---

# increments X and Y based on direction. changes area.
def move(player, world, npcs, args):
    direction = args[0] # "> move <direction>"

    # self explanatory
    if direction == "north":
        player.y_pos += 1
    elif direction == "south":
        player.y_pos -= 1
    elif direction == "east":
        player.x_pos += 1
    elif direction == "west":
        player.x_pos -= 1
    else:
        print("invalid direction")
        return
    
    # if out of bounds, is moved back
    if player.y_pos >= world[0].__len__():
        player.y_pos = world[0].__len__() - 1
        print("nothing there")
        return
    elif player.y_pos < 0:
        player.y_pos = 0
        print("nothing there")
        return
    elif player.x_pos >= world.__len__():
        player.x_pos = world.__len__() - 1
        print("nothing there")
        return
    elif player.x_pos < 0:
        player.x_pos = 0
        return
        print("nothing there")

    if player.currentroom != None:
        leave(player, world, npcs, [])
    # updates areas based on x and y
    player.currentarea = world[player.x_pos, player.y_pos]

    # outputs direction, x, y, and new area
    print(f"moving {direction}... X: {player.x_pos} Y: {player.y_pos} area: {world[player.x_pos, player.y_pos].name}")

# goes to a specific area by name
def go(player, world, npcs, args):
    # checking grammar
    if args[0] != 'to':
        print("Invalid command")
        return

    area_name = ' '.join(args[1:]).lower() # "> go to <area_name>"

    for x, area_row in enumerate(world): # looping through x in areas
        for y, area in enumerate(area_row): # looping through y in areas
            if area.name.lower() == area_name: # if name of defined area == name of desired area
                if player.currentroom != None:
                    leave(player, world, npcs, [])
                # moves the player to that area
                player.currentarea = area 
                player.x_pos = x
                player.y_pos = y
                
                print(f"Went to area {area_name} at x: {x}, y: {y}") # outputs info to the player

# removes item from player inventory, equips in appropriate spot
def equip(player, world, npcs, args):
    item_name = args[0] # "> equip <item> <place>"

    if args.__len__() > 1: # if more than 1 trailing word...
        place = args[1] # the second will be "place"
    else:
        place = None

    item, message = find(player.inventory, item_name, place)
    if item == None: 
        print(message)
        return

    if isinstance(item, things.Melee_Weapon) or isinstance(item, things.Ranged_Weapon):
        available_places = ['primary', 'secondary']
    # setting place for armor
    elif isinstance(item, things.Armor):
        available_places = [item.place] # sets place to be place defined for give playerect
    # if item is niether weapon or armor
    else: 
        print("not an item you can equip")
        return

    if place == None: place = available_places[0]

    if place not in available_places:
        print("you can't equip that there")
        return
    
    # checks if there is already something in the spot item is replacing
    if player.equipped[place] != None:
        unequip(player, world, npcs, [player.equipped[place].name, place]) # unequips that item

    gsc.update_gamestate('equip', item.name)
    player.equipped[place] = item
    player.inventory.remove(item)
    print(f"equipped {item.name} in spot: {place}. {item.name} removed from inventory")

def unequip(player, world, npcs, args):
    item_name = args[0]

    if args.__len__() > 1: # if more than 1 trailing word...
        place = args[1] # the second will be "place"
    else:
        place = None

    place, message = find(player.equipped, item_name, place)
    if place == None: 
        print(message)
        return


    gsc.update_gamestate('unequip', item.name)
    player.inventory.append(player.equipped[place]) # add thing to inventory 
    player.equipped[place] = None # remove thing from equipped
    print(f"unequipped {item} from {place}. {item} added to inventory") # output information

def enter(player, world, npcs, args):
    
    if player.currentroom != None:
        print("you must exit the current room befor entering a new one")
        return

    room_name = ' '.join(args)
    for room in player.currentarea.rooms:
        if room.name.lower() == room_name.lower():
            player.currentroom = room
            print(f"entering {room.name}")
            break


def leave(player, world, npcs, args):
    if player.currentroom == None:
        print("you must enter a room befor exiting one")
        return

    print(f"exiting {player.currentroom.name}")
    player.currentroom = None

# will continue to work on it. for right now it gives a description of the area along with 
# it's inventory and all containers inside it
def look(player, world, npcs, args):
    room = find_room(player)
    
    if args[0] == 'around':
        print(room.describe())

    elif args[0] == 'at':
        for container in room.containers:
            if container.name.lower() == ' '.join(args[1:]):
                print(container.describe())
                return
        
        npc_name = ' '.join(args[1:])
        for npc in npcs:
            if npc_name == npc.name.lower() or npc_name in [referral.lower() for referral in npc.referrals]:
                if npc.currentarea == player.currentarea and npc.currentroom == player.currentroom:
                    print(npc.describe())
                    break
                else: print("they're not here")
        

# transfers item from area inventory to player inventory
def pick_up(player, world, npcs, args):
    
    if args[0] != 'up':
        print('Invalid Command')
        return

    item_name = args[1] # "pick up <item>"
    room = find_room(player)

    item, message = find(room.inventory, item_name)
    if item == None: 
        if message == "item not in inventory":
            print("item not here")
        else:
            print(message)
        return

    # adds to that weight of desired item
    w = item.weight + player.total_weight

    if w <= player.stats_max_cap: # checks if total weight is within player max capacity
        gsc.update_gamestate("pick up", item_name)
        player.inventory.append(item) # adds iem to player inventory
        room.inventory.remove(item) # removes item from area inventory 
        print(f'picked up {item.name}') # sends message to player confirming success
                
    else: print("too heavy!")

def take(player, world, npcs, args):

    if args.__len__() < 3 or args[1] != 'from':
        print('Invalid Command')
        return

    item_name = args[0] # "take <item> from <container>"
    container_name = ' '.join(args[2:]).lower()
    room = find_room(player)

    for container in room.containers:
        if container.name.lower() == container_name:
            break
    else: 
        for npc in npcs:
            if container_name == npc.name.lower() or container_name in [referral.lower() for referral in npc.referrals]:
                if npc.currentarea == player.currentarea and npc.currentroom == player.currentroom:
                    if npc.dead or npc.follows_orders:
                        container = npc
                        break
                    else: print("you can't take stuff from them")
                else: print("they're not here")
        else:
            print("container not in area")
            return

    item, message = find(container.inventory, item_name)
    if item == None: 
        if message == "item not in inventory":
            print("item not there")
        else:
            print(message)
        return

    # adds to that weight of desired item
    w = item.weight + player.total_weight

    if w <= player.stats_max_cap: # checks if total weight is within player max capacity
        gsc.update_gamestate("take", item_name)
        player.inventory.append(item) # adds iem to player inventory
        container.inventory.remove(item) # removes item from area inventory 
        print(f'took {item.name} from {container_name}') # sends message to player confirming success
    else: print("too heavy!") # if total weight 


def drop(player, world, npcs, args):
    item_name = args[0]
    room = find_room(player)
    
    item, message = find(player.inventory, item_name)
    if item == None: 
        print(message)
        return

    gsc.update_gamestate("drop", item_name)
    print(f"Dropped {item.name}")
    room.inventory.append(item)
    player.inventory.remove(item)
    
def eat(player, world, npcs, args):
    item_name = args[0]
    
    item, message = find(player.inventory, item_name)
    if item == None: 
        print(message)
        return

    gsc.update_gamestate("eat", item_name)

    print(f"Yum! {item.name}!")
    player.inventory.remove(item)
    player.stats_hunger += item.hunger_points
    if player.stats_hunger >= 100:
        player.stats_hunger = 100
    player.stats_xp += 3

def talk(player, world, npcs, args):
    try:
        if args[0] != 'to':
            print("Invalid Command")
            return
        
        npc_name = ' '.join(args[1:])
        for npc in npcs:
            if npc_name == npc.name.lower() or npc_name in [referral.lower() for referral in npc.referrals]:
                if npc.currentarea == player.currentarea and npc.currentroom == player.currentroom:
                    if not npc.dead: player.talk(npc)
                    else: print("he's dead")
                else: 
                    print("npc not here")
    except:
        return 'error'

def fight(player, world, npcs, args):
    npc_name = ' '.join(args)
    for npc in npcs:
        if npc_name == npc.name.lower() or npc_name in [referral.lower() for referral in npc.referrals]:
            if npc.currentarea == player.currentarea and npc.currentroom == player.currentroom:
                if not npc.dead:
                    done = False
                    while not done:
                        done = player.fight(npc)
                        if done:
                            break
                        done = npc.fight(player)
                    if npc.dead:
                        player.stats_xp += 20
                        gsc.update_gamestate('kill', npc.species)
                    return
                else: print("You can't fight a dead guy")
            else: 
                print("npc not here")
                return
        
def exit_sequence(player, world, npcs, args):
    bad_answer = True
    while bad_answer:
        os.system('cls')
        done = input("Are you sure you want to go? (y/n) ")
        bad_answer = False
        if done == 'y':
            done = True
        elif done == 'n':
            done = False
        else:
            bad_answer = True
            print("Invalid respose.")
    return done


# ---Main controller---
commands = {
    'move': move,
    'go': go, 
    'equip': equip,
    'unequip': unequip,
    'enter': enter,
    'leave': leave,
    'look': look,
    'pick': pick_up,
    'take': take,
    'drop': drop,
    'eat': eat,
    'talk': talk,
    'fight': fight,
    'exit': exit_sequence,
}