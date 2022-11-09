from db import ( 
    local_session, 
    Item_Template, 
    Inventory, 
    Container_Template, 
    Room_Template, 
    Area_Template, 
    Npc_Template,
    create_container_template, 
    create_room_template,
    create_area_template
)
from random import randint
all_items = { 
    'Melee_Weapon': {
        'sword': {
            'description': 'A simple blade, standard issue to the guards and warriors of Rosacea',
            'base_damage': 10,
            'defense_bonus': 5,
            'length': 3,
            'weight': 4
        },

        'scimitar': {
            'description': 'A curved blade, obtainable only by those of the east via secret techniques',
            'base_damage': 15,
            'defense_bonus': 7,
            'length': 4,
            'weight': 4
        },
        
        'dagger': {
            'description': 'A small blade, favored by thieves, cutthroats and duplicitous individuals,',
            'base_damage': 5,
            'defense_bonus': 1,
            'length': 1,
            'weight': 1
        },

        'shield': {
            'description': 'A simple kite shield, covers the body from attacks',
            'base_damage': 3,
            'defense_bonus': 10,
            'length': 1,
            'weight': 4
        },

        'spear': {
            'description': 'A hardwood staff with a pointed tip, better at a range.',
            'base_damage': 7,
            'defense_bonus': 5,
            'length': 6,
            'weight': 4
        },

        'club': {
            'description': 'A large wooden stick, prized by those who prefer a more percussive method; it’s extremely heavy.',
            'base_damage': 12,
            'defense_bonus': 3,
            'length': 6,
            'weight': 7
        },
    },
    'Ranged_Weapon': {
        'bow': {
            'description': 'A basic bow, hewn and strung to hunt small and medium game.',
            'base_damage': 8,
            'attack_range': 30,
            'weight': 2
        },

        'longbow': {
            'description': 'A large bow, specifically designed to take down big game and puncture armor.',
            'base_damage': 12,
            'attack_range': 60,
            'weight': 4
        },

        'recurve_bow': {
            'description': 'A curved bow, more powerful than a regular bow with fewer drawbacks',
            'base_damage': 10,
            'attack_range': 45,
            'weight': 3
        },
    },
    'Armor': {
        'helmet': {
            'description': 'A standard protective device, enough to stop simple blows',
            'defense_bonus': 8,
            'place': 'head',
            'weight': 1
        },
        
        'chestplate': {
            'description': 'A metal cuirass around the torso, boasts protection at the cost of weight,',
            'defense_bonus': 8,
            'place': 'chest',
            'weight': 4
        },
        
        'leather_boots': {
            'description': 'A basic set of boots, comfortable and capable,',
            'defense_bonus': 3,
            'place': 'boots',
            'weight': 1
        },

        'metal_boots': {
            'description': 'A heavy pair of boots, greatly reduces movement for minor protection',
            'defense_bonus': 4,
            'place': 'boots',
            'weight': 6
        },
    },
    'Tool': {
        'hammer': {
            'description': 'A tool prized by smiths and carpenters, as valuable as the things they build,',
            'weight': 2
        },
        'hoe': {
            'description': 'A tool cherished by farmers, good for moving the earth.',
            'weight': 3
        },
        'fishing_rod': {
            'description': 'A tool used to catch and reel fish ashore.',
            'weight': 2
        },
    },

    'Food': {
        'apple': {
            'description': 'A staple of the Malusian diet, inexpensive and filling',
            'hunger_points': 1,
            'weight': 1
        },

        'fish': {
            'description': 'A prime source of protein for those living along the coast.',
            'hunger_points': 2,
            'weight': 1
        },
    },
    'Key': {
        'silver_key': {
            'description': 'A small, simple key, used to open and lock the door it matches.',
            'weight': 1
        },
    },
}

world = {
    'Village': {
        'x_pos': 0,
        'y_pos': 0,
        'description': '',
        'rooms': {
            'Blacksmith': {
                'description': 'The workplace of a master of steel and iron',
                'containers': {
                    'Display Rack': {
                        'description': 'A rack full of pegs that displays Loui\'s creations',
                        'inventory': ['sword', 'helmet', 'chestplate']
                    }
                },
                'inventory': [],
                'npcs': {
                    'Louie the Blacksmith': {
                        'referrals': '',
                        'description': 'A master of his craft, produces works of metal.',
                        'inventory': ['hammer', 'sword'] # 16 gold
                    }
                }
            },
            'Jimmy\'s Hut': {
                'description': 'The home of a man renowned for his love of one thing.',
                'containers': {
                    'Apple Barrel': {
                        'description': 'A barrel full of free apples. Jimmy\'s gift to humanity',
                        'inventory': ['apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple']}
                },
                'inventory': ['apple', 'apple', 'apple'],
                'npcs': {
                    'Jimmy the Apple Man': {
                        'referrals': '',
                        'description': ' A man known throughout the world, a key political figure in the Malus Kingdom',
                        'inventory': ['apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple', 'apple']
                    }
                }
            },
            'Apothecary': {
                'description': 'Herbal master, brews great concoctions',
                'containers': {},
                'inventory': [],
                'npcs': {
                    'Aerith the Apothecary': {
                        'referrals': '',
                        'description': 'A squat old woman, known for her concoctions and kind demeanor.',
                        'inventory': [] # 13 gold
                    }
                }
            },
            'Market': {
                'description': 'A bustling marketplace, one would do well to watch their coin purse.',
                'containers': {},
                'inventory': [],
                'npcs': {
                    'Vincent the Bowyer': {
                        'referrals': '',
                        'description': 'A hulking figure with the heart of a kitten.',
                        'inventory': ['bow', 'longbow', 'recurve_bow'] # 11 gold
                    },
                    'Carla the Farmer': {
                        'referrals': '',
                        'description': 'An average woman, it ain\'t much but i\'s honest work',
                        'inventory': ['apple', 'apple', 'apple', 'fish', 'hoe'] # 11 gold
                    }
                }
            },
        },
        'containers': {

        },
        'inventory': [

        ],
        'npcs': {

        }
    },
    'Harbor': {
        'x_pos': 0,
        'y_pos': 1,
        'description': 'A seaside port, alive with the work of sailors and dockworkers',
        'rooms': {
            'Fish Market': {
                'description': 'The market of those who live off the sea',
                'containers': {},
                'inventory': [],
                'npcs': {
                    'Charles the Fisherman': {
                        'referrals': '',
                        'description': 'A tan man who catches and sells fish for a living',
                        'inventory': ['fishing_rod', 'fish', 'fish', 'fish', 'fish', 'fish', 'fish'] # 10 gold
                    }
                }
            },
            'Merchant Market': {
                'description': 'An interesting area with all sorts of exotic merchants.',
                'containers': {},
                'inventory': [],
                'npcs': {
                    'Qasim the Traveler': {
                        'referrals': '',
                        'description': ' A man covered in a cloak and mask, speaks little',
                        'inventory': ['leather_boots', 'chestplate', 'scimitar', 'scimitar'] # 29 gold
                    }
                }
            },
            'Docks': {
                'description': 'Travel to a different sector (coming soon!)',
                'containers': {},
                'inventory': [],
                'npcs': {}
            }
        },
        'containers': {

        },
        'inventory': [

        ],
        'npcs': {
            'Ronald the Shipwright': {
                'referrals': '',
                'description': 'A wrinkled old man, days spent sailing the ocean and trading.',
                'inventory': ['fish', 'fish', 'fish', 'sword', 'leather_boots'] # 23 gold
            }
        }
    },
    'Plains South': {
        'x_pos': 1,
        'y_pos': 0,
        'description': 'South of "Plains North" (Duh), it is home to a small encampment of gahblins',
        'rooms': {
            'Gahblin Village': {
                'description': 'A ram-shack town/encampment built and lived in by Gahblins',
                'containers': {
                    'Box O\' Daggers': {
                        'description': 'Exactly what it sounds like. A cardboard box full of daggers. How did they manage to get cardboard? I don\'t know. Maybe they\'re more intelligent then we give them credit for',
                        'inventory': ['dagger', 'dagger', 'dagger', 'dagger', 'dagger', 'dagger', 'dagger', 'dagger', 'dagger', 'dagger', 'dagger', 'dagger', 'dagger', 'dagger', 'dagger', 'dagger']
                    }
                },
                'inventory': [],
                'npcs': {
                    'Grinkle the Gahblin': {
                        'referrals': '',
                        'species': 'Gahblin',
                        'description': 'A little green humanoid monster, not very intelligent. Don\'t ask why he\'s named that.',
                        'inventory': ['dagger'] # 1 gold
                    },
                    'Garry the Gahblin': {
                        'referrals': '',
                        'species': 'Gahblin',
                        'description': 'A little green humanoid monster, very very very unintelligent. ',
                        'inventory': ['dagger'] # 1 gold
                    },
                    'George the Gahblin': {
                        'referrals': '',
                        'species': 'Gahblin',
                        'description': 'A little green humanoid monster, not very intelligent, yet wants to go to school for philosophy in England. I don\'t quite think that\'ll work out',
                        'inventory': ['dagger'] # 3 gold 
                    },
                }
            }
        },
        'containers': {

        },
        'inventory': [

        ],
        'npcs': {
            'Grubby the Gahblin': {
                'referrals': '',
                'species': 'Gahblin',
                'description': 'A little green humanoid monster, not very intelligent, especially hates sunflowers',
                'inventory': ['dagger'] # 1 gold
            },
        }
    },
    'Plains North': {
        'x_pos': 1,
        'y_pos': 1,
        'description': 'Some empty plains with a few Gahblins, a Brogre (Male ogre), and an Ogirl (Female ogre).',
        'rooms': {

        },
        'containers': {

        },
        'inventory': [

        ],
        'npcs': {
            'Boris the Brogre': {
                'referrals': '',
                'species': 'Ogre',
                'description': 'A large green humanoid monster; all brawn, no brain. A lot like Shrek, but less attractive and a bit stupider (also is niether "love" nor "life")',
                'inventory': ['club'] # 5 gold
            }
        }
    },
    'Outpost': {
        'x_pos': 2,
        'y_pos': 1,
        'description': '',
        'rooms': {
            'Market' : {
                'description': '',
                'containers': {},
                'inventory': [],
                'npcs': {}
            },
            'General\'s hut': {
                'description': '',
                'containers': {},
                'inventory': [],
                'npcs': {}
            }
        },
        'containers': {

        },
        'inventory': [

        ],
        'npcs': {

        }
    },
    'Swamp1': {
        'x_pos': 2,
        'y_pos': 0,
        'description': 'Quite similar, in fact, to the village, except no houses, markets or other buildings, no roads, it\'s all wet and muddy, there\'s thick foliage everywhere, and it\'s really not a great place to be.',
        'rooms': {

        },
        'containers': {

        },
        'inventory': [

        ],
        'npcs': {

        }
    },
    'Swamp2': {
        'x_pos': 3,
        'y_pos': 0,
        'description': '',
        'rooms': {
            'Cavern': {
                'description': '',
                'containers': {},
                'inventory': [],
                'npcs': {}
            }
        },
        'containers': {

        },
        'inventory': [

        ],
        'npcs': {

        }
    },
    'Woods1': {
        'x_pos': 0,
        'y_pos': 2,
        'description': '',
        'rooms': {

        },
        'containers': {

        },
        'inventory': [

        ],
        'npcs': {

        }
    },
    'Woods2': {
        'x_pos': 1,
        'y_pos': 2,
        'description': '',
        'rooms': {
            'Witch\'s Hut': {
                'description': '',
                'containers': {},
                'inventory': [],
                'npcs': {}
            }
        },
        'containers': {

        },
        'inventory': [

        ],
        'npcs': {

        }
    },
    'Mountain1': {
        'x_pos': 3,
        'y_pos': 1,
        'description': '',
        'rooms': {

        },
        'containers': {

        },
        'inventory': [

        ],
        'npcs': {

        }
    },
    'Mountain2': {
        'x_pos': 2,
        'y_pos': 2,
        'description': '',
        'rooms': {

        },
        'containers': {

        },
        'inventory': [

        ],
        'npcs': {

        }
    },
    'Demon Castle': {
        'x_pos': 3,
        'y_pos': 2,
        'description': '',
        'rooms': {

        },
        'containers': {

        },
        'inventory': [

        ],
        'npcs': {

        }
    },
}

# itemlist = []
# for item_type, items in all_items.items():
#     for item_name, item_values in items.items():
#         itemlist.append(Item_Template(
#             name = item_name, item_type = item_type, **item_values
#         ))
# local_session.add_all(itemlist)
# local_session.commit()

for area_name, area_data in world.items():
    area_template = Area_Template(
        name = area_name,
        description = area_data['description'],
        inventory_list = [Inventory()],
        x_pos = area_data['x_pos'],
        y_pos = area_data['y_pos']
    )
    for item_name in area_data['inventory']:
        item_template = local_session.query(Item_Template).filter(Item_Template.name == item_name).first()
        area_template.inventory_append(item_template)   

    for container, container_data in area_data['containers'].items():
        container_template = Container_Template(
            name = container,
            description = container_data['description'],
            inventory_list = [Inventory()]
        )
        for item_name in container_data['inventory']:
            item_template = local_session.query(Item_Template).filter(Item_Template.name == item_name).first()
            container_template.inventory_append(item_template)
        
        area_template.containers.append(container_template)  

    for room, room_data in area_data['rooms'].items():
        room_template = Room_Template(
            name = room,
            description = room_data['description'],
            inventory_list = [Inventory()]
        )
        for item_name in room_data['inventory']:
            item_template = local_session.query(Item_Template).filter(Item_Template.name == item_name).first()
            room_template.inventory_append(item_template)  

        for container, container_data in room_data['containers'].items():
            container_template = Container_Template(
                name = container,
                description = container_data['description'],
                inventory_list = [Inventory()]
            )
            for item_name in container_data['inventory']:
                item_template = local_session.query(Item_Template).filter(Item_Template.name == item_name).first()
                container_template.inventory_append(item_template)

            room_template.containers.append(container_template)  

        for npc_name, npc_data in room_data['npcs'].items():
            kwargs = npc_data.copy()
            kwargs.pop('inventory')
            npc_template = Npc_Template(name = npc_name, x_pos = area_data['x_pos'], y_pos = area_data['y_pos'], inventory_list = [Inventory()], **kwargs)
            
            for item_name in npc_data['inventory']:
                item_template = local_session.query(Item_Template).filter(Item_Template.name == item_name).first()
                npc_template.inventory_append(item_template)

            room_template.npcs.append(npc_template) 

        area_template.rooms.append(room_template)
        
    for npc_name, npc_data in area_data['npcs'].items():
        kwargs = npc_data.copy()
        kwargs.pop('inventory')
        npc_template = Npc_Template(name = npc_name, x_pos = area_data['x_pos'], y_pos = area_data['y_pos'], inventory_list = [Inventory()], **kwargs)
        
        for item_name in npc_data['inventory']:
            item_template = local_session.query(Item_Template).filter(Item_Template.name == item_name).first()
            npc_template.inventory_append(item_template)
        
        area_template.npcs.append(npc_template)

    local_session.add(area_template)
    local_session.commit()