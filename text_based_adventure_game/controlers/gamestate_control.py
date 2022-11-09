
def update_gamestate(action, item):
    action_id = find_action_id(action)
    item_id = find_item_id(item)
    with open('controlers/gamestate.txt', 'a') as gs:
        gs.write(f"{action_id}:{item_id}/")

def save_gamestate(file):
    with open('controlers/gamestate.txt', 'r') as gs:
        with open(file, 'a') as f:
            f.write(f"\n{gs.read()}")

def load_gamestate(file):
    with open('controlers/gamestate.txt', 'w') as gs:
        with open(file, 'r') as f:
            last_line = f.read().split("\n")[-1]
            gs.write(last_line)

def clear_gamestate():
    with open('controlers/gamestate.txt', 'w') as gs:
        gs.write('')

def count(action, item = None):
    action_id = find_action_id(action)
    if item:
        item_id = find_item_id(item)    
    
    with open('controlers/gamestate.txt', 'r') as gs:
        lines = gs.read().split('/')[:-1]
        num = 0
        for line in lines:
            split_line = line.split(":")
            if action_id == int(split_line[0]):
                if item:
                    if item_id == int(split_line[1]):
                        num += 1
                else:
                    num += 1

    return num

# add kill
actions = [
    'equip',
    'unequip',
    'pick up',
    'take',
    'drop',
    'eat',
    'kill'
]

# add enemies
items = [
    'sword',
    'dagger',
    'shield',
    'helmet',
    'chestplate',
    'leather_boots',
    'metal_boots',
    'hammer',
    'bow',
    'apple',
    'silver_key',
    'human',
    'gahblin',
    'ogre'
]

def find_action_id(action):
    for index, option in enumerate(actions):
        if option == action.lower():
            return index

def find_item_id(item):
    for index, option in enumerate(items):
        if option == item.lower():
            return index

if __name__ == "__main__":
    update_gamestate('equip', 'helmet')