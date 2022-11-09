from dataclasses import dataclass, field
import resources.things as things
import resources.commands as cmd
import resources.quests as quests
import random
import os
from controlers.output_control import output  # output_control.py
import numpy as np
from typing import Dict, List


@dataclass
class Entity:
    # Attributes
    name: str = field(default='jerry') # for later referencing, creating story
    x_pos: int = field(default=0) # for storing position for areas
    y_pos: int = field(default=0) # ||
    dead: bool = field(default=False)
    description: str = field(default=str)
    # will be a list of things.Item objects
    inventory: list = field(default_factory=list)
    currentarea: things.Area = field(default=None)
    currentroom: things.Room = field(default=None)
    total_weight: int = field(default = 0, init=False)
    
    # Will also have things.Item objects
    equipped: dict = field(default_factory=lambda:{
        'head': None,
        'chest': None,
        'boots': None,
        'primary': None,
        'secondary': None
    }, init = True)
    
    # list of integers to store stats (will add more)
    stats_level: int = field(default=0) 
    stats_xp: int = field(default=0) 
    stats_max_hp: int = field(default=100) 
    stats_hp: int = field(default=100) 
    stats_hunger: int = field(default=100) 
    stats_max_cap: int = field(default=12) 

    def __post_init__(self):
        self.total_weight = 0
        # sums up weight of inventory
        for inventory_item in self.inventory: 
            self.total_weight += inventory_item.weight
                    
        # adds to that weight of equipped items
        for place in self.equipped:
            if self.equipped[place] != None:
                self.total_weight += self.equipped[place].weight

    def update_hunger(self):
        if self.stats_hunger <= 0:
            self.stats_hunger = 0
        else: self.stats_hunger -= 2

    def update_health(self):
        if self.stats_hunger <= 0:
            self.stats_hp -= 10
        elif self.stats_hunger >= 90:
            self.stats_hp += 10
            if self.stats_hp >= 100:
                self.stats_hp = 100

        if self.stats_hp <= 0:
            self.stats_hp = 0
            self.die()

    def die(self):
        pass

    def describe(self):
        return f"Name: {self.name}\nDescription: {self.description}"

@dataclass
class Player(Entity): # Player class  
    player_quests: list = field(default_factory=list, init=False)

    def __post_init__(self):
        super().__post_init__()
        self.player_quests.append(quests.getQuest(0))

    def talk(self, npc):
        goodbye = False
        while not goodbye:
            output(self)
            message = input(f"You: ")
            
            if message == 'quest':
                if npc.pending_quest == None:
                    self.player_quests.append(npc.available_quests[0])
                    npc.pending_quest = npc.available_quests[0]
                    npc.available_quests.pop(0)
                    response = npc.respond("", "new_quest")
            
                elif npc.pending_quest.get_completion(self):
                    print('quest_completed_a')
                    response = npc.respond("", "quest_completed")
                    print('quest_completed_b')
                    self.on_completion_quest(npc.pending_quest, npc)
                    npc.pending_quest = None
                    print('quest_completed_c')
            
                else:
                    print('pending_quest')
                    response = npc.respond("", "pending_quest")
            else:
                response = npc.respond(message)
                    
            print(f"{npc.name}: {response}")
            if response == 'bye':
                goodbye = True
    
    def on_completion_quest(self, quest, from_npc = None):
        self.stats_xp += quest.reward['xp']
        if self.currentroom == None:
            currentroom = self.currentarea
        else: currentroom = self.currentroom
        currentroom.inventory += quest.reward['items']
        self.player_quests.remove(quest)
        if not from_npc:
            print(f"you completed a quest! reward: \nxp: {quest.reward['xp']}\titems:{[item.name for item in quest.reward['items']]}")
            if quest.q_id == quests.global_quests.__len__() - 1:
                print("You have completed all the quests")
            else:
                self.player_quests.append(quests.getQuest(quest.q_id+1))

    def fight(self, npc):
        # your turn

        output(self)
        if self.stats_hp <= 0:
            self.die()
            return True


        decison = input("Your Turn! pick an equipped weapon to use\n> ")
        if decison.__len__() == 0:
            print("Invalid Command --- Bulunder")
            damage = 0
        else:

            if self.equipped['primary'] == None:
                equipped_primary = None
            else:
                equipped_primary = self.equipped['primary'].name

            if self.equipped['secondary'] == None:
                equipped_secondary = None
            else:
                equipped_secondary = self.equipped['secondary'].name

            if equipped_primary == decison == equipped_secondary:
                damage = int(1.5 * self.equipped['primary'].base_damage)
            elif equipped_primary == decison:
                damage = self.equipped['primary'].base_damage
            elif equipped_secondary == decison:
                damage = int(0.8 * self.equipped['primary'].base_damage)
            elif decison == 'run' or decison == 'retreat':
                print("you run")
                return True
            else:
                print("Invalid Command --- Bulunder")
                damage = 0
            
        npc.stats_hp -= damage
        os.system('cls')
        print(f"You did {damage} damage. NPC has {npc.stats_hp} hp")
        return False

    def die(self):
        output(self)
        os.system('cls')
        print("you died")
        try: os.remove(f'saved_games/{self.name}.txt')
        except FileNotFoundError: pass
        exit()

@dataclass
class NPC(Entity): # Player class
    species: str = field(default='human')
    referrals: list = field(default_factory=list)
    available_quests: list = field(default_factory=list)
    pending_quest: quests.Quest = field(default=None, init=False)
    follows_orders: bool = field(default=False)
    agression: float = field(default=0.5)
    
    responses: dict = field(default_factory=lambda: {
        'hello': 'hi, how can i help?',
        'goodbye': 'bye'
    })

    def __post_init__(self):
        super().__post_init__()
        for quest in self.available_quests:
            quest.from_npc = self.name
    
    def update_rooms(self, fun):
        if self.currentroom == None:
            npc_list = self.currentarea.npcs
        else:
            npc_list = self.currentroom.npcs
        
        if fun == "append":
            npc_list.append(self.name)
        elif fun == 'remove':
            npc_list.remove(self.name)

    def respond(self, message: str, request: str = None):
        if request == None:
            if message in self.responses:
                return self.responses[message]
            elif message.split(' ')[0] in cmd.commands:
                if self.follows_orders:
                    self.update_rooms("remove")
                    returner = cmd.commands[message.split(' ')[0]](self, message.split(' ')[1:]) # calls function that matches first word of UI     
                    self.update_rooms("append")
                    if returner == 'error':
                        return 'I can\'t do that'
                    elif message.split(' ')[0] == 'go' or message.split(' ')[0] == 'move' or message.split(' ')[0] == 'enter' or message.split(' ')[0] == 'leave':
                        return 'bye'
                    else:
                        return 'ok'
                else: return 'no'
            else: # If first word in UI does not match a known command
                return "I don't understand"
        else:
            if request == "pending_quest":
                return f"Come back when you {self.pending_quest.description}"
            elif request == "new_quest":
                return f"Quest: {self.pending_quest.description} \nreward:\txp: {self.pending_quest.reward['xp']}\titems :{[item.name for item in self.pending_quest.reward['items']]}"
            elif request == "quest_completed":
                return f"you completed a quest! reward: \nxp: {self.pending_quest.reward['xp']}\titems:{[item.name for item in self.pending_quest.reward['items']]}"
            else: return "Invalid Request"

    def fight(self, obj):
        if self.equipped['primary']:
            damage = self.equipped['primary'].base_damage
            weapon_name = self.equipped['primary'].name
        elif self.equipped['secondary']:
            damage = int(self.equipped['secondary'].base_damage * 0.8)
            weapon_name = self.equipped['secondary'].name
        else:
            damage = 5
            weapon_name = 'fists'
        
        if self.stats_hp >= 50:
            pass
        elif self.stats_hp > 0:
            rand_num = random.randint(0, 100)
            retreat_chance = (100 - self.stats_hp) * (1 - self.agression) - 1
            if rand_num <= retreat_chance:
                print("enemy ran away")
                return True
        else:
            self.die()
            return True

        obj.stats_hp -= damage
        print(f"The enemy did {damage} damage with his/her/it's {weapon_name}. you have {obj.stats_hp} hp")
        return False

    def die(self):
        self.dead = True
        self.referrals.append(self.name)
        if self.currentroom: self.currentroom.npcs.remove(self.name)
        else: self.currentarea.npcs.remove(self.name)
        self.name = f"{self.name} (dead)"
        if self.currentroom: self.currentroom.npcs.append(self.name)
        else: self.currentarea.npcs.append(self.name)
        
        for place in self.equipped:
            if self.equipped[place] != None:
                self.inventory.append(self.equipped[place]) # add thing to inventory 
                self.equipped[place] = None # remove thing from equipped
        
        print("dead")

print('')


@dataclass
class Animal(Entity): # Player class  
    pass

