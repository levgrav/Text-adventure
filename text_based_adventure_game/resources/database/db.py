from dataclasses import dataclass
from sqlalchemy.orm import (
    declarative_base, 
    sessionmaker, 
    relationship
)
from sqlalchemy import (
    Column, 
    String, 
    Integer,
    Float, 
    Boolean,
    create_engine, 
    Table, 
    ForeignKey
)
import os
import numpy as np
try:
    from resources.things import Item, Tool, Melee_Weapon, Ranged_Weapon, Food, Armor, Area, Room, Container
    from resources.entities import NPC
except ModuleNotFoundError:
    Item = Tool = Melee_Weapon = Ranged_Weapon = Food = Armor = NPC = None

# ---Configuration---
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = 'sqlite:///'+os.path.join(BASE_DIR, 'world.db')
engine = create_engine(connection_string, echo=True)

Base = declarative_base()
Session = sessionmaker()
local_session = Session(bind = engine)
npcs = []

items_associations = Table(
    "item_associations", 
    Base.metadata,
    Column('inventory_id', ForeignKey("inventories.id")),
    Column('item_id', ForeignKey("items.id")),
)

@dataclass()
class Item_Template(Base):
    __tablename__ = "items"
    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String())
    item_type = Column(String())
    description = Column(String())
    weight = Column(Integer())
    base_damage = Column(Integer())
    attack_range = Column(Integer())
    defense_bonus = Column(Integer())
    length = Column(Integer())
    place = Column(String())
    hunger_points = Column(Integer())
    inventories = relationship(
        'Inventory', 
        secondary=items_associations, 
        back_populates='items')

@dataclass()
class Inventory(Base):
    __tablename__ = 'inventories'
    id = Column(Integer(), primary_key=True, nullable=False)
    items = relationship(
        "Item_Template",
        secondary=items_associations,
        back_populates='inventories'
    )
    container_id = Column(Integer(), ForeignKey('containers.id'))
    room_id = Column(Integer(), ForeignKey('rooms.id'))
    area_id = Column(Integer(), ForeignKey('areas.id'))
    npc_id = Column(Integer(), ForeignKey('npcs.id'))

    @property
    def outer(self):
        if self.container_id:
            return container_id
        elif self.room_id:
            return self.room_id
        elif self.area_id:
            return self.area_id
        elif self.npc_id:
            return self.npc_id
        else:
            return None


@dataclass()
class Container_Template(Base):
    __tablename__ = 'containers'
    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String())
    description = Column(String())
    inventory_list = relationship(
        'Inventory',
        backref='containers'
    )
    room_id = Column(Integer(), ForeignKey('rooms.id'))
    area_id = Column(Integer(), ForeignKey('areas.id'))
    @property
    def room(self):
        if self.room_id:
            return self.room_id
        elif self.area_id:
            return self.area_id
        else:
            return None   
    @property 
    def inventory(self):
        return self.inventory_list[0].items

    @inventory.setter
    def inventory_set(self, val):
        self.inventory_list[0].items = val

    def inventory_append(self, item):
        self.inventory_list[0].items.append(item)
 
@dataclass()
class Room_Template(Base):
    __tablename__ = 'rooms'
    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String())
    description = Column(String())
    inventory_list = relationship(
        'Inventory',
        backref='rooms'
    )

    containers = relationship(
        'Container_Template',
        backref='rooms'
    ) 

    npcs = relationship(
        'Npc_Template',
        backref='rooms'
    )

    area_id = Column(Integer(), ForeignKey('areas.id'))
    @property 
    def inventory(self):
        return self.inventory_list[0].items

    @inventory.setter
    def inventory_set(self, val):
        self.inventory_list[0].items = val
    
    def inventory_append(self, item):
        self.inventory_list[0].items.append(item)

@dataclass()
class Area_Template(Base):
    __tablename__ = 'areas'
    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String())
    description = Column(String())
    x_pos = Column(Integer())
    y_pos = Column(Integer())
    inventory_list = relationship(
        'Inventory',
        backref='areas'
    )

    containers = relationship(
        'Container_Template',
        backref='areas'
    )

    rooms = relationship(
        'Room_Template',
        backref='areas'
    )

    npcs = relationship(
        'Npc_Template',
        backref='areas'
    )

    @property 
    def inventory(self):
        return self.inventory_list[0].items

    @inventory.setter
    def inventory_set(self, val):
        self.inventory_list[0].items = val
    
    def inventory_append(self, item):
        self.inventory_list[0].items.append(item)

@dataclass()
class Npc_Template(Base):
    __tablename__ = 'npcs'
    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String())
    referrals = Column(String())
    species = Column(String(), default='Human')
    description = Column(String())
    x_pos = Column(Integer())
    y_pos = Column(Integer())
    dead = Column(Boolean(), default = False)
    room_id = Column(Integer(), ForeignKey('rooms.id'))
    area_id = Column(Integer(), ForeignKey('areas.id'))
    stats_level = Column(Integer(), default=0)
    stats_xp = Column(Integer(), default=0)
    stats_max_hp = Column(Integer(), default=100)
    stats_hp = Column(Integer(), default=100)
    stats_hunger = Column(Integer(), default=100)
    stats_max_cap = Column(Integer(), default=12)

    inventory_list = relationship(
        'Inventory',
        backref='npcs'
    )

    @property 
    def inventory(self):
        return self.inventory_list[0].items

    @inventory.setter
    def inventory_set(self, val):
        self.inventory_list[0].items = val
    
    def inventory_append(self, item):
        self.inventory_list[0].items.append(item)

    def __post_init__(self):
        self.referrals += self.name.split(' ')[0]

def create_container_template(name, description, inventory):
    n = local_session.query(Container_Template).all().__len__()
    num_inventories = local_session.query(Inventory).all().__len__()
    container_template = Container_Template( id = n+1, name = name, description = description, inventory_list = [ Inventory( id = num_inventories + 1 ) ] )
    for item_name in inventory:
        item_template = local_session.query(Item_Template).filter(Item_Template.name == item_name).first()
        container_template.inventory_append(item_template)
    return container_template

def create_room_template(name, description, inventory, containers):
    n = local_session.query(Room_Template).all().__len__()
    num_inventories = local_session.query(Inventory).all().__len__()
    room_template = Room_Template( id = n+1, name = name, description = description, inventory_list = [ Inventory( id = num_inventories + 1 ) ] )
    for item_name in inventory:
        item_template = local_session.query(Item_Template).filter(Item_Template.name == item_name).first()
        room_template.inventory_append(item_template)
    for container_name in containers:
        container_template = local_session.query(Container_Template).filter(Container_Template.name == container_name).first()
        room_template.containers.append(container_template)
    return room_template

def create_area_template(name, description, inventory, containers, rooms):
    n = local_session.query(Area_Template).all().__len__()
    num_inventories = local_session.query(Inventory).all().__len__()
    area_template = Area_Template( id = n+1, name = name, description = description, inventory_list = [ Inventory( id = num_inventories + 1 ) ] )
    for item_name in inventory:
        item_template = local_session.query(Item_Template).filter(Item_Template.name == item_name).first()
        area_template.inventory_append(item_template)
    for container_name in containers:
        container_template = local_session.query(Container_Template).filter(Container_Template.name == container_name).first()
        area_template.containers.append(container_template)
    for room_name in rooms:
        room_template = local_session.query(Room_Template).filter(Room_Template.name == room_name).first()
        area_template.rooms.append(room_template)
    return area_template

def container(name: str = None, container_template: Container_Template = None):
    if name:
        container_template = local_session.query(Container_Template).filter(Container_Template.name == name).first()
    
    if not container_template:
        print("no template")
        return

    kwargs = container_template.__dict__.copy()
    kwargs.pop('_sa_instance_state')
    kwargs.pop("id")
    kwargs.pop("room_id")
    kwargs.pop("area_id")

    container_created = Container(**kwargs)
    for item_template in container_template.inventory:
        container_created.inventory.append(item(item_template=item_template))

    return container_created

def room(name: str = None, room_template: Room_Template = None):
    global npcs
    if name:
        room_template = local_session.query(Room_Template).filter(Room_Template.name == name).first()
    
    if not room_template:
        print("no template")
        return

    kwargs = room_template.__dict__.copy()
    kwargs.pop('_sa_instance_state')
    kwargs.pop("id")
    kwargs.pop("area_id")

    room_created = Room(**kwargs)
    for item_template in room_template.inventory:
        room_created.inventory.append(item(item_template=item_template))
    for container_template in room_template.containers:
        room_created.containers.append(container(container_template=container_template))

    return room_created

def area(name: str = None, area_template: Area_Template = None):
    global npcs
    if name:
        area_template = local_session.query(Area_Template).filter(Area_Template.name == name).first()
    
    if not area_template:
        print("no template")
        return

    kwargs = area_template.__dict__.copy()
    kwargs.pop('_sa_instance_state')
    kwargs.pop("id")

    area_created = Area(**kwargs)
    for item_template in area_template.inventory:
        area_created.inventory.append(item(item_template=item_template))
    for container_template in area_template.containers:
        area_created.containers.append(container(container_template=container_template))
    for room_template in area_template.rooms:
        area_created.rooms.append(room(room_template=room_template))

    return area_created

def item(name: str = None, item_template: Item_Template = None):
    if name:
        item_template = local_session.query(Item_Template).filter(Item_Template.name == name).first()
    
    if not item_template:
        print("no template")
        return

    item_type = item_template.item_type
    kwargs = item_template.__dict__.copy()
    kwargs.pop('_sa_instance_state')
    kwargs.pop('item_type')
    kwargs.pop("id")
    for key, value in item_template.__dict__.items():
        if value == None:
            if key in kwargs.keys():
                kwargs.pop(key)

    return globals()[item_type](**kwargs)

def npc(world, name: str = None, npc_template: Npc_Template = None):
    if name:
        npc_template = local_session.query(Npc_Template).filter(Npc_Template.name == name).first()
    
    if not npc_template:
        print("no template")
        return

    kwargs = npc_template.__dict__.copy()

    currentarea = world[kwargs['x_pos'], kwargs['y_pos']]

    currentroom = None
    if kwargs['room_id']:
        for room in currentarea.rooms:
            if room.name == local_session.query(Room_Template).filter(Room_Template.id == kwargs['room_id']).first().name:
                currentroom = room

    kwargs.pop('_sa_instance_state')
    kwargs.pop("id")
    kwargs.pop("room_id")
    kwargs.pop("area_id")


    kwargs['referrals'] = kwargs['referrals'].split(", ")
    npc_created = NPC(currentarea = currentarea, currentroom= currentroom, **kwargs)
    npc_created.update_rooms("append")
    for item_template in npc_template.inventory:
        npc_created.inventory.append(item(item_template=item_template))

    available_places = list(npc_created.equipped.keys())

    for inventory_item in npc_created.inventory:
        if isinstance(inventory_item, Melee_Weapon) or isinstance(inventory_item, Ranged_Weapon):
            if 'primary' in available_places:
                npc_created.equipped['primary'] = inventory_item
                available_places.remove('primary')
            elif 'secondary' in available_places:
                npc_created.equipped['secondary'] = inventory_item
                available_places.remove('secondary')

        elif isinstance(inventory_item, Armor):
            if inventory_item.place in available_places:
                npc_created.equipped[inventory_item.place] = inventory_item
                available_places.remove(inventory_item.place)
        
    return npc_created

def generate_npcs(world):
    npcs = []
    for npc_template in local_session.query(Npc_Template).all():
        npcs.append(npc(world, npc_template=npc_template))
    return npcs

def find_area_by_pos(x, y):
    template = local_session.query(Area_Template).filter(Area_Template.x_pos == x).filter(Area_Template.y_pos == y).first()
    return area(area_template=template)

def generate_world():
    return np.array([[find_area_by_pos(x, y) for y in range(3)] for x in range(4)])
