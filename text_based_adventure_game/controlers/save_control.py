import resources.things as things
from resources.entities import Player
from controlers.gamestate_control import save_gamestate, load_gamestate, clear_gamestate
import resources.database.db as db

def new_game():
    clear_gamestate()
    name = input("what is your character's name? ")
    world = db.generate_world()
    npcs = db.generate_npcs(world)
    
    player = Player(name, 0, 0, 
        inventory=[
            db.item('apple'), 
            db.item('apple')
        ], 
        equipped={
            'head': None,
            'chest': None,
            'boots': None,
            'primary': None,
            'secondary': None
        },
        currentarea = world[0,0],
        currentroom = None)
    return player, world, npcs


def load_game():
    while True:
        name = input("what is your character's name? ")
        try:
            with open(f"saved_games/{name}.txt", 'r') as s:
                lines = s.read()
                lines = lines.split('/')
                name = lines[0]
                x = int(lines[1])
                y = int(lines[2])
                inventory_names = lines[3].split(',')[:-1]
                inventory = []
                for inventory_item in inventory_names:
                    inventory.append(db.item(inventory_item))
                currentarea = things.areas[x, y]
                currentroom = None
                for room in currentarea.rooms:
                    if room.name == lines[4]:
                        currentroom = room
                equipped_raw = lines[5].split(',')[:-1]
                equipped = {
                    'head': None,
                    'chest': None,
                    'boots': None,
                    'primary': None,
                    'secondary': None,
                }
                for datum in equipped_raw:
                    line = datum.split(':')
                    if line[1] == 'None':
                        thing = None
                    else:
                        thing = db.item(line[1])
                    equipped[line[0]] = thing
                    

                player = Player(name, x, y, inventory, equipped=equipped)
                player.currentarea = currentarea
                player.currentroom = currentroom
                player.stats = stats
                player.stats_level = int(lines[6])
                player.stats_xp = int(lines[7])
                player.stats_max_hp = int(lines[8])
                player.stats_hp = int(lines[9])
                player.stats_hunger = int(lines[10])
                player.stats_max_cap = int(lines[11])
                    
            
            load_gamestate(f"saved_games/{name}.txt")
            return player
        
        except FileNotFoundError:
            print("Character Not Found")
    

def save(player):
    with open(f"saved_games/{player.name}.txt", 'w') as s:
        if player.currentroom == None:
            currentroom_name = None
        else: currentroom_name = player.currentroom.name
        lines = [
            f"{player.name}/",
            f"{player.x_pos}/",
            f"{player.y_pos}/"]

        for item in player.inventory:
            lines.append(f"{item.name},")
        lines.append("/")

        lines.append(f"{currentroom_name}/")
        
        for place in player.equipped:
            if player.equipped[place] == None:
                name = None
            else: 
                name = player.equipped[place].name

            lines.append(f"{place}:{name},")
        lines.append("/")

        lines.append(f"stats_level: {player.stats_level}")
        lines.append(f"stats_xp: {player.stats_xp}")
        lines.append(f"stats_max_hp: {player.stats_max_hp}")
        lines.append(f"stats_hp: {player.stats_hp}")
        lines.append(f"stats_hunger: {player.stats_hunger}")
        lines.append(f"stats_max_cap: {player.stats_max_cap}")
        s.writelines(lines)
    save_gamestate(f"saved_games/{player.name}.txt")
    
