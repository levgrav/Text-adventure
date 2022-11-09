import os
import resources.commands as cmd  # Commands.py
import resources.things as things  # things.py
from controlers.output_control import clear_output, output  # output_control.py
from controlers.save_control import load_game, new_game, save # output_control.py
from resources.entities import Player

import resources.database.db as db

world = db.generate_world()
npcs = db.generate_npcs(world)

print('')