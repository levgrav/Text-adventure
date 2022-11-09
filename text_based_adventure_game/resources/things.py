from dataclasses import dataclass, field, asdict, astuple, InitVar
import numpy as np

@dataclass()
class Item:
    name: str
    description: str
    weight: str

    def __repr__(self):
        return self.name

@dataclass()
class Tool(Item):
    pass

@dataclass()
class Ranged_Weapon(Tool):
    base_damage: str
    attack_range: str

@dataclass()
class Melee_Weapon(Tool):
    base_damage: str
    defense_bonus: str
    length: str

@dataclass()
class Armor(Tool):
    defense_bonus: str
    place: str
    
@dataclass()
class Food(Item):
    hunger_points: float        

@dataclass()
class Container:
    name: str
    description: str
    inventory: list = field(default_factory=list)
    def describe(self):
        return f"Container name: {self.name}\n Container description: {self.description}\nItems in container: {[item.name for item in self.inventory]}"

@dataclass()
class Room(Container):
    containers: list = field(default_factory=list)
    npcs: list = field(default_factory=list, init=False)

    def describe(self):
        return f"Room name: {self.name}\n Room description: {self.description}\nItems in room: {[item.name for item in self.inventory]} Containers in room: {[container.name for container in self.containers]} NPCs in room: {self.npcs}"

@dataclass()
class Area(Room):
    x_pos: int = 0
    y_pos: int = 0
    rooms: list = field(default_factory=list)

    def describe(self):
        return f"Area name: {self.name}\n Area description: {self.description}\nItems in area: {[item.name for item in self.inventory]} Containers in area: {[container.name for container in self.containers]} Rooms in area: {[room.name for room in self.rooms]} NPCs in area: {self.npcs}"

num_containers = 0
def default_container():
    global num_containers
    num_containers += 1
    return Container(name = f'container{num_containers}', 
                     description ='a default containrer', 
                     inventory = [Tool('hammer'), Food('apple')])

num_rooms = 0
def default_room():
    global num_rooms
    num_rooms += 1
    return Room(name = f"room{num_rooms}", 
                description = "a default room", 
                containers = [default_container()], 
                inventory = [Melee_Weapon('sword'), Armor('helmet')])

num_areas = 0
def default_area(x, y):
    global num_areas
    num_areas += 1
    return Area(x = x,
                y = y,
                name = f"area{num_areas}", 
                description = "a default area",
                rooms = [default_room()], 
                containers = [default_container()], 
                inventory = [Melee_Weapon('sword'), Armor('helmet')])

levels_xp = [0, 20, 50, 100, 200, 500, 1000] #, 2000, 5000, 10000, 200000]

def find_item_in(inventory, name: str, place = None):
    if isinstance(inventory, list):
        for inventory_item in inventory: # loops through items in inventory 
            if inventory_item.name == name:
                return inventory_item, None
        return None, "item not in inventory"
    elif isinstance(inventory, dict):
        if place == None:
            for place, item in inventory.items():
                if item.name == name:
                    return place, None
        return None, "item not equipped"

def find_room(obj):
    if obj.currentroom == None:
        return obj.currentarea
    else: 
        return obj.currentroom

if __name__ == "__main__":
    pass