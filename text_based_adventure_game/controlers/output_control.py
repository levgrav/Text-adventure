import resources.things as things
from time import sleep

def output(player):
    try:
        level = player.stats_level
        xp_above_level = player.stats_xp - things.levels_xp[level]
        xp_between_levels = things.levels_xp[level + 1] - things.levels_xp[level]

        total_weight = player.total_weight
        xp_bar = int(20 * xp_above_level / xp_between_levels)
        weight_bar = int(20 * total_weight / player.stats_max_cap)
        health_bar = int(20 * player.stats_hp / player.stats_max_hp)
        hunger_bar = int(20 * player.stats_hunger / 100)
        stat1_bar = 7
        stat2_bar = 16 
        
        if player.currentroom == None:
            currentroom = player.currentarea
        else:
            currentroom = player.currentroom
        
        if currentroom != None:
            with open("output.txt", 'w') as o:
                quests = []
                
                lines = [
                    f"name: {player.name}\n\n",
                    '\n\n'.join([quest.__repr__() for quest in player.player_quests]),
                    f"\n\ncurrent room: {currentroom.name}\n",
                    f"\"{currentroom.description}\"\n",
                    f"\nTo Win: Get 600 XP \n\n",
                    f"stats:\n",
                    f"level    {level} | {xp_bar * '-' + (20 - xp_bar) * ' '} | {level + 1}       |     weight   0 | {weight_bar * '-' + (20 - weight_bar) * ' '} | {player.stats_max_cap}\n",
                    f"health   0 | {health_bar * '-' + (20 - health_bar) * ' '} | 100     |     hunger   0 | {hunger_bar * '-' + (20 - hunger_bar) * ' '} | 100\n",
                    f"stat1    0 | {stat1_bar * '-' + (20 - stat1_bar) * ' '} | 100     |     stat2    0 | {stat2_bar * '-' + (20 - stat2_bar) * ' '} | 100\n",
                    f"\n",
                    f"inventory:   total weight (including equipped items): {total_weight}"]

                for i, item in enumerate(player.inventory):
                    if i % 3 == 0:
                        lines.append(f"\nItem: {item.name}{(11 - len(item.name)) * ' '}Weight: {item.weight}")
                    elif i % 3 == 1:
                        lines.append(f"  |  Item: {item.name}{(11 - len(item.name)) * ' '}Weight: {item.weight}")
                    elif i % 3 == 2:
                        lines.append(f"  |  Item: {item.name}{(11 - len(item.name)) * ' '}Weight: {item.weight}")
                
                # display equipped inventory
                lines.append(f"\n\nequipped: \n")
                for place in player.equipped:
                    thing = player.equipped[place]

                    if thing:
                        name = thing.name
                        thing_type = thing.__repr__().split('(')[0]

                        if thing_type == "Ranged_Weapon" or thing_type == "Melee_Weapon":
                            damage = thing.base_damage
                        else:
                            damage = 0

                        if thing_type == "Armor" or thing_type == "Melee_Weapon":
                            defense = thing.defense_bonus
                        else:
                            defense = 0
                    else:
                        damage = 0
                        defense = 0
                        name = "None"
                        ability = ''

                    lines.append(f"Place: {place}{(12 - len(place)) * ' '}Item: {name}{(12 - len(name)) * ' '}Base Damamge: {damage}{(8 - len(str(damage))) * ' '}Defense Bonus: {defense}\n")
                
                o.writelines(lines)
                o.close()
                
    except PermissionError:
        sleep(0.1)
        output(player)

def clear_output():
    with open("output.txt", 'w') as o:
        o.write('')