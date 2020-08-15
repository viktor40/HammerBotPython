from typing_extensions import Final

stages: Final[list] = [  # final state: head, torso, both arms, and both legs
                        """
                ```
                   -------------
                   |           |
                   |           O
                   |          \\|/
                   |           | 
                   |          / \\ 
                   ----```
                        """,
                        # head, torso, both arms, and one leg
                        """
                ```
                   ------------- 
                   |           | 
                   |           O 
                   |          \\|/ 
                   |           | 
                   |          / 
                   ----```
                        """,
                        # head, torso, and both arms
                        """
                ```
                   ------------- 
                   |           | 
                   |           O 
                   |          \\|/ 
                   |           | 
                   |      
                   ----```
                        """,
                        # head, torso, and one arm
                        """
                ```
                   -------------
                   |           |
                   |           O
                   |          \\|
                   |           | 
                   |      
                   ----```
                        """,
                        # head and torso
                        """
                ```
                   ------------- 
                   |           | 
                   |           O 
                   |           | 
                   |           | 
                   |     
                   ----```
                        """,
                        # head
                        """
                ```
                   ------------- 
                   |           | 
                   |           O 
                   |     
                   |     
                   |     
                   ----```
                        """,
                        # pole and rope only
                        """
                ```
                   ------------- 
                   |           | 
                   |      
                   |      
                   |      
                   |      
                   ----```
                        """,
                        # pole only
                        """
                ```
                   ------------- 
                   |      
                   |      
                   |      
                   |      
                   |      
                   ----```
                        """,
                        # pole without vertical part
                        """
                ```
                   -
                   |      
                   |      
                   |      
                   |      
                   |      
                   ----```
                        """
                    ]

word_list: Final[list] = [
                            'wares',
                            'soup',
                            'mount',
                            'extend',
                            'brown',
                            'expert',
                            'tired',
                            'humidity',
                            'backpack',
                            'crust',
                            'dent',
                            'market',
                            'knock',
                            'smite',
                            'windy',
                            'coin',
                            'throw',
                            'silence',
                            'bluff',
                            'downfall',
                            'climb',
                            'lying',
                            'weaver',
                            'snob',
                            'kickoff',
                            'match',
                            'quaker',
                            'foreman',
                            'excite',
                            'thinking',
                            'mend',
                            'allergen',
                            'pruning',
                            'coat',
                            'emerald',
                            'coherent',
                            'manic',
                            'multiple',
                            'square',
                            'funded',
                            'funnel',
                            'sailing',
                            'dream',
                            'mutation',
                            'strict',
                            'mystic',
                            'film',
                            'guide',
                            'strain',
                            'bishop',
                            'settle',
                            'plateau',
                            'emigrate',
                            'marching',
                            'optimal',
                            'medley',
                            'endanger',
                            'wick',
                            'condone',
                            'schema',
                            'rage',
                            'figure',
                            'plague',
                            'aloof',
                            'there',
                            'reusable',
                            'refinery',
                            'suffer',
                            'affirm',
                            'captive',
                            'flipping',
                            'prolong',
                            'main',
                            'coral',
                            'dinner',
                            'rabbit',
                            'chill',
                            'seed',
                            'born',
                            'shampoo',
                            'italian',
                            'giggle',
                            'roost',
                            'palm',
                            'globe',
                            'wise',
                            'grandson',
                            'running',
                            'sunlight',
                            'spending',
                            'crunch',
                            'tangle',
                            'forego',
                            'tailor',
                            'divinity',
                            'probe',
                            'bearded',
                            'premium',
                            'featured',
                            'serve',
                            'borrower',
                            'examine',
                            'legal',
                            'outlive',
                            'unnamed',
                            'unending',
                            'snow',
                            'whisper',
                            'bundle',
                            'bracket',
                            'deny',
                            'blurred',
                            'pentagon',
                            'reformed',
                            'polarity',
                            'jumping',
                            'gain',
                            'laundry',
                            'hobble',
                            'culture',
                            'whittle',
                            'docket',
                            'mayhem',
                            'build',
                            'peel',
                            'board',
                            'keen',
                            'glorious',
                            'singular',
                            'cavalry',
                            'present',
                            'cold',
                            'hook',
                            'salted',
                            'just',
                            'dumpling',
                            'glimmer',
                            'drowning',
                            'admiral',
                            'sketch',
                            'subject',
                            'upright',
                            'sunshine',
                            'slide',
                            'calamity',
                            'gurney',
                            'adult',
                            'adore',
                            'weld',
                            'masking',
                            'print',
                            'wishful',
                            'foyer',
                            'tofu',
                            'machete',
                            'diced',
                            'behemoth',
                            'rout',
                            'midwife',
                            'neglect',
                            'mass',
                            'game',
                            'stocking',
                            'folly',
                            'action',
                            'bubbling',
                            'scented',
                            'sprinter',
                            'bingo',
                            'egyptian',
                            'comedy',
                            'rung',
                            'outdated',
                            'radical',
                            'escalate',
                            'mutter',
                            'desert',
                            'memento',
                            'kayak',
                            'talon',
                            'portion',
                            'affirm',
                            'dashing',
                            'fare',
                            'battle',
                            'pupil',
                            'rite',
                            'smash',
                            'true',
                            'entrance',
                            'counting',
                            'peruse',
                            'dioxide',
                            'hermit',
                            'carving',
                            'backyard',
                            'homeless',
                            'medley',
                            'packet',
                            'tickle',
                            'coming',
                            'leave',
                            'swing',
                            'thicket',
                            'reserve',
                            'murder',
                            'costly',
                            'corduroy',
                            'bump',
                            'oncology',
                            'swatch',
                            'rundown',
                            'steal',
                            'teller',
                            'cable',
                            'oily',
                            'official',
                            'abyss',
                            'schism',
                            'failing',
                            'guru',
                            'trim',
                            'alfalfa',
                            'doubt',
                            'booming',
                            'bruised',
                            'playful',
                            'kicker',
                            'jockey',
                            'handmade',
                            'landfall',
                            'rhythm',
                            'keep',
                            'reassure',
                            'garland',
                            'sauna',
                            'idiom',
                            'fluent',
                            'lope',
                            'gland',
                            'amend',
                            'fashion',
                            'treaty',
                            'standing',
                            'current',
                            'sharpen',
                            'cinder',
                            'idealist',
                            'festive',
                            'frame',
                            'molten',
                            'sill',
                            'glisten',
                            'fearful',
                            'basement',
                            'minutia',
                            'coin',
                            'stick',
                            'featured',
                            'soot',
                            'static',
                            'crazed',
                            'upset',
                            'robotics',
                            'dwarf',
                            'shield',
                            'butler',
                            'stitch',
                            'stub',
                            'sabotage',
                            'parlor',
                            'prompt',
                            'heady',
                            'horn',
                            'bygone',
                            'rework',
                            'painful',
                            'composer',
                            'glance',
                            'acquit',
                            'eagle',
                            'solvent',
                            'backbone',
                            'smart',
                            'atlas',
                            'leap',
                            'danger',
                            'bruise',
                            'seminar',
                            'tinge',
                            'trip',
                            'narrow',
                            'while',
                            'jaguar',
                            'seminary',
                            'command',
                            'cassette',
                            'draw',
                            'anchovy',
                            'scream',
                            'blush',
                            'organic',
                            'applause',
                            'parallel',
                            'trolley',
                            'pathos',
                            'origin',
                            'hang',
                            'pungent',
                            'angular',
                            'stubble',
                            'painted',
                            'forward',
                            'saddle',
                            'muddy',
                            'orchid',
                            'prudence',
                            'disprove',
                            'yiddish',
                            'lobbying',
                            'neuron',
                            'tumor',
                            'haitian',
                            'swift',
                            'mantel',
                            'wardrobe',
                            'consist',
                            'storied',
                            'extreme',
                            'payback',
                            'control',
                            'dummy',
                            'influx',
                            'realtor',
                            'detach',
                            'flake',
                            'consign',
                            'adjunct',
                            'stylized',
                            'weep',
                            'prepare',
                            'pioneer',
                            'tail',
                            'platoon',
                            'exercise',
                            'dummy',
                            'clap',
                            'actor',
                            'spark',
                            'dope',
                            'phrase',
                            'welsh',
                            'wall',
                            'whine',
                            'fickle',
                            'wrong',
                            'stamina',
                            'dazed',
                            'cramp',
                            'filet',
                            'foresee',
                            'seller',
                            'award',
                            'mare',
                            'uncover',
                            'drowning',
                            'ease',
                            'buttery',
                            'luxury',
                            'bigotry',
                            'muddy',
                            'photon',
                            'snow',
                            'oppress',
                            'blessed',
                            'call',
                            'stain',
                            'amber',
                            'rental',
                            'nominee',
                            'township',
                            'adhesive',
                            'lengthy',
                            'swarm',
                            'court',
                            'baguette',
                            'leper',
                            'vital',
                            'push',
                            'digger',
                            'setback',
                            'accused',
                            'taker',
                            'genie',
                            'reverse',
                            'fake',
                            'widowed',
                            'renewed',
                            'goodness',
                            'featured',
                            'curse',
                            'shocked',
                            'shove',
                            'marked',
                            'interact',
                            'mane',
                            'hawk',
                            'kidnap',
                            'noble',
                            'proton',
                            'effort',
                            'patriot',
                            'showcase',
                            'parish',
                            'mosaic',
                            'coil',
                            'aide',
                            'breeder',
                            'concoct',
                            'pathway',
                            'hearing',
                            'bayou',
                            'regimen',
                            'drain',
                            'bereft',
                            'matte',
                            'bill',
                            'medal',
                            'prickly',
                            'sarcasm',
                            'stuffy',
                            'allege',
                            'monopoly',
                            'lighter',
                            'repair',
                            'worship',
                            'vent',
                            'hybrid',
                            'buffet',
                            'lively',
                            'abruptly',
                            'absurd',
                            'askew',
                            'avenue',
                            'awkward',
                            'axiom',
                            'azure',
                            'bagpipes',
                            'bandwagon',
                            'banjo',
                            'beekeeper',
                            'bikini',
                            'blitz',
                            'blizzard',
                            'boggle',
                            'bookworm',
                            'boxcar',
                            'buffalo',
                            'buffoon',
                            'buzzwords',
                            'cobweb',
                            'cockiness',
                            'croquet',
                            'crypt',
                            'curacao',
                            'cycle',
                            'dizzying',
                            'duplex',
                            'dwarves',
                            'embezzle',
                            'equip',
                            'espionage',
                            'exodus',
                            'faking',
                            'fishhook',
                            'fixable',
                            'fjord',
                            'fluffiness',
                            'flyby',
                            'funny',
                            'gabby',
                            'galaxy',
                            'galvanize',
                            'gazebo',
                            'gnarly',
                            'gossip',
                            'haiku',
                            'icebox',
                            'injury',
                            'ivory',
                            'ivy',
                            'jackpot',
                            'jaywalk',
                            'jazzy',
                            'jelly',
                            'jigsaw',
                            'jiujitsu',
                            'jogging',
                            'joking',
                            'joyful',
                            'juicy',
                            'jukebox',
                            'jumbo',
                            'kazoo',
                            'kiwifruit',
                            'knapsack',
                            'lengths',
                            'matrix',
                            'megahertz',
                            'microwave',
                            'mnemonic',
                            'mystify',
                            'nightclub'
                            'nowadays',
                            'nymph',
                            'onyx',
                            'ovary',
                            'oxidize',
                            'oxygen',
                            'peekaboo',
                            'pixel',
                            'pizazz',
                            'pneumonia',
                            'polka',
                            'psyche',
                            'puppy',
                            'puzzling',
                            'quartz',
                            'queue',
                            'quips',
                            'quiz',
                            'quizzes',
                            'rickshaw',
                            'schnapps',
                            'scratch',
                            'shiv',
                            'snazzy',
                            'sphinx',
                            'spritz',
                            'squawk',
                            'staff',
                            'strength',
                            'stretch',
                            'stronghold',
                            'subway',
                            'swivel',
                            'syndrome',
                            'thriftless',
                            'thumbscrew',
                            'topaz',
                            'transcript',
                            'transgress',
                            'unknown',
                            'unworthy',
                            'unzip',
                            'uptown',
                            'vaporize',
                            'vixen',
                            'vodka',
                            'voodoo',
                            'vortex',
                            'voyeurism',
                            'walkway',
                            'waltz',
                            'wellspring',
                            'whiskey',
                            'whizzing',
                            'whomever',
                            'witchcraft',
                            'wizard',
                            'wristwatch',
                            'xylophone',
                            'youthful',
                            'yummy',
                            'zephyr'
                            ]
