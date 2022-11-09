""" A Text-Based Adventure Game! """
# ---Imports---
import os

import resources.commands as cmd  # Commands.py
import resources.things as things  # things.py
import resources.database.db as db
from controlers.output_control import clear_output, output  # output_control.py
from controlers.save_control import load_game, new_game, save # output_control.py
from resources.entities import Player


# ---Functions---
def calculate_stuff(obj) -> None:
    for quest in obj.player_quests:
        if quest:
            for i, item in enumerate(quest.reward['items']):
                if isinstance(item, str):
                    quest.reward['items'][i] = db.item(quest.reward['items'][i])
            if quest.from_npc == None:
                if quest.get_completion(obj):
                    obj.on_completion_quest(quest)

    for level, level_xp in enumerate(things.levels_xp):
        if obj.stats_xp >= level_xp:
            obj.stats_level = level
    
    if obj.stats_xp >= 600:
        output(obj)
        os.system('cls')
        print("You Win")
        input("Press enter to continue")
        save(obj)
        clear_output()
        exit()

    obj.total_weight = 0
    # sums up weight of inventory
    for inventory_item in obj.inventory: 
        obj.total_weight += inventory_item.weight
                
    # adds to that weight of equipped items
    for place in obj.equipped:
        if obj.equipped[place] != None:
            obj.total_weight += obj.equipped[place].weight

    player.update_hunger()
    player.update_health()

def main_menu() -> Player:
    print("welcome to the text based adventure game!")
    ui = input("| new game | load game |\n> ").lower()
    if ui == 'new game':
        player, world, npcs = new_game()
    elif ui == 'load game':
        player, world, npcs = load_game()
    else:
        os.system('cls')
        player, world, npcs = main_menu()

    os.system('cls')
    return player, world, npcs

# ---Main Loop---
class Game(object):
    def main(self, player: Player, world, npcs) -> None:
        os.system('cls')
        


        done = False
        while not done:
            
            try:
                calculate_stuff(player)
                output(player) # Updates output.txt based on player stats

                ui = input("> ").lower() # command prompt, looks like, "> <command> <args>"
                ui_split = ui.split(" ") # splits command into command and args. separated by space
                os.system('cls')
                if ui_split[0] in cmd.commands: # checks if first word in available commands
                    returner = cmd.commands[ui_split[0]](player, world, npcs, ui_split[1:]) # calls function that matches first word of UI
                    
                    # if player entered "exit", sets done variable (which controls main loop) to the 
                    # output of the previously called function
                    if ui_split[0] == 'exit':
                        done = returner
                
                else: # If first word in UI does not match a known command
                    print("invalid command") 
            
            # KeyboardInterrupt is treated the same as "> exit"
            except KeyboardInterrupt:
                print("exit")
                done = cmd.exit_sequence(player, world, npcs, [])

        save(player)
        clear_output()

# ---Game commands---
if __name__ == "__main__":
    os.system('cls') # clear screen
    player, world, npcs = main_menu()
    os.system('cls')
    print('The Kingdom of Malus was located on the south western region of the continent Rosacea, ruled by a just and righteous king, his health is failing via a curse levied upon him by the accursed demon king of the North, his three sons, one brave, one kind, and one cunning, must each make the journey to the demon lord\'s castle set upon Mt. Thorne and lift the curse placed upon their father. During their journey however, they must prepare to face monsters, demons, and those unfortunate enough to fall under the spell of the demon king, reducing them to little more than mindless brutes. The three princes may choose to handle their journey however they want, but be warned, none are willing to take the lives of those under the curse of the demon king, as it would remove them from succession to the throne.')
    input("\nPress enter to continue")
    Game().main(player, world, npcs)