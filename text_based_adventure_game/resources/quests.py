from dataclasses import dataclass, field
import resources.things as things
import controlers.gamestate_control as gsc


@dataclass()
class Quest:
    q_id: int
    description: str = ''
    from_npc: str = None
    reward: dict = field(default_factory={
        'xp': 0,
        'items': []
    })

    def get_completion(self):
        pass

    def __repr__(self):
        return f"Quest: {self.description} \nreward:\txp: {self.reward['xp']}\titems: {[item_name for item_name in self.reward['items']]}"

    
@dataclass()
class Inventory_Quest(Quest):
    item_name: str = ''
    number: int = 0

    def get_completion(self, player):
        count = 0
        for item in player.inventory:
            if item.name == self.item_name:
                count += 1
        
        if count >= self.number:
            return True
        else: 
            return False

    def __repr__(self):
        return super().__repr__()

@dataclass()
class Stat_Quest(Quest):
    stat: str = ''
    number: int = 0
    
    def get_completion(self, player):
        if player.__getattribute__(f"stats_{stat}") >= self.number:
            return True
        else: 
            return False

    def __repr__(self):
        return super().__repr__()
 
@dataclass()
class Kill_Quest(Quest):
    enemy: str = ''
    number: int = 0
    
    def get_completion(self, player):
        enemies = gsc.count('kill', self.enemy)
        if enemies >= self.number:
            return True
        else: 
            return False

    def __repr__(self):
        return super().__repr__()
        
global_quests = [
    Inventory_Quest(
        q_id = 0, 
        description='get a helmet for 20 xp and a chestplate',
        reward = {
            'xp': 100,
            'items': ['chestplate']
        },
        item_name = 'helmet',
        number = 1
    ),
    Kill_Quest(
        q_id = 1, 
        description='Kill 3 gahblins: 100 xp, recurve bow',
        reward = {
            'xp': 100,
            'items': ['recurve_bow']
        },
        enemy = 'gahblin',
        number = 3
    ),
    Inventory_Quest(
        q_id = 2, 
        description='Collect 3 apples for 100 xp',
        reward = {
            'xp': 100,
            'items': []
        },
        item_name = 'apple',
        number = 3
    ),
    Kill_Quest(
        q_id = 3, 
        description='Hunt the "Brogre": 250 xp, club',
        reward = {
            'xp': 250,
            'items': ['recurve_bow']
        },
        enemy = 'ogre',
        number = 1
    )
]


def getQuest(q_id):
    for quest in global_quests:
        if quest.q_id == q_id:
            print(quest)
            return quest
    
    print("Not an available quest")
    return