USERNAME_MAX_LENGTH = 10

NODE_ID_MAX_LENGTH = 32

SYSTEM_NODE_PAGE_NAME_MAX_LENGTH = 10
SYSTEM_NODE_NOTES_MAX_LENGTH = 1000

SYSTEM_NAME_MAX_LENGTH = 20
SYSTEM_TYPE_MAX_LENGTH = 4
SYSTEM_TYPE_CHOICES = (
    ('high', 'Highsec'),
    ('low', 'Lowsec'),
    ('null', 'Nullsec'),
    ('c1', 'C1'),
    ('c2', 'C2'),
    ('c3', 'C3'),
    ('c4', 'C4'),
    ('c5', 'C5'),
    ('c6', 'C6')
)
SYSTEM_REGION_MAX_LENGTH = 20
SYSTEM_WSPACE_EFFECT_MAX_LENGTH = 1
SYSTEM_WSPACE_EFFECT_CHOICES = (
    ('b', 'Black Hole'),
    ('c', 'Cataclysmic Variable'),
    ('m', 'Magnetar'),
    ('p', 'Pulsar'),
    ('r', 'Red Giant'),
    ('w', 'Wolf-Rayet')
)

WSPACE_EFFECTS_HTML = {SYSTEM_WSPACE_EFFECT_CHOICES[0][0] :
                           '''Ship velocity +%d%%<br/>
                              Inertia +%d%%<br/>
                              Drone control range -%d%%<br/>
                              Missile velocity -%d%%<br/>
                              Lock Range -%d%%<br/>
                              Falloff -%d%%''',
                       SYSTEM_WSPACE_EFFECT_CHOICES[1][0] :
                           '''Shield transfer +%d%%<br/>
                              Remote repair +%d%%<br/>
                              Capacitor capacity +%d%%<br/>
                              Capacitor recharge +%d%%<br/>
                              Repair amount -%d%%<br/>
                              Shield repair amount -%d%%''',
                       SYSTEM_WSPACE_EFFECT_CHOICES[2][0] :
                           '''Damage +%d%%<br/>
                              AOE Velocity -%d%%<br/>
                              Drone Velocity -%d%%<br/>
                              Targeting Range -%d%%<br/>
                              Tracking Speed -%d%%''',
                       SYSTEM_WSPACE_EFFECT_CHOICES[3][0] :
                           '''Shield +%d%%<br/>
                              Targeting Range +%d%%<br/>
                              Signature +%d%%<br/>
                              Armor Resistances -%d%%<br/>
                              Cap recharge -%d%%''',
                       SYSTEM_WSPACE_EFFECT_CHOICES[4][0] :
                           '''Heat Damage +%d%%<br/>
                              Overload Bonus +%d%%<br/>
                              Smart Bomb Range +%d%%<br/>
                              Smart Bomb Damage +%d%%''',
                       SYSTEM_WSPACE_EFFECT_CHOICES[5][0] :
                           '''Armor Resistances +%d%%<br/>
                              Small Weapon Damage +%d%%<br/>
                              Signature Size -%d%%<br/>
                              Shield Resistances -%d%%'''}

WSPACE_EFFECT_CLASSES = {SYSTEM_WSPACE_EFFECT_CHOICES[0][0] :
                            {SYSTEM_TYPE_CHOICES[3][0] : (25, 25, 10, 10, 10, 10),
                             SYSTEM_TYPE_CHOICES[4][0] : (44, 44, 19, 19, 19, 19),
                             SYSTEM_TYPE_CHOICES[5][0] : (55, 55, 27, 27, 27, 27),
                             SYSTEM_TYPE_CHOICES[6][0] : (68, 68, 34, 34, 34, 34),
                             SYSTEM_TYPE_CHOICES[7][0] : (85, 85, 41, 41, 41, 41),
                             SYSTEM_TYPE_CHOICES[8][0] : (100, 100, 50, 50, 50, 50)},
                        SYSTEM_WSPACE_EFFECT_CHOICES[1][0] :
                            {SYSTEM_TYPE_CHOICES[3][0] : (25, 25, 25, 25, 10, 10),
                             SYSTEM_TYPE_CHOICES[4][0] : (44, 44, 44, 44, 19, 19),
                             SYSTEM_TYPE_CHOICES[5][0] : (55, 55, 55, 55, 27, 27),
                             SYSTEM_TYPE_CHOICES[6][0] : (68, 68, 68, 68, 34, 34),
                             SYSTEM_TYPE_CHOICES[7][0] : (85, 85, 85, 85, 41, 41),
                             SYSTEM_TYPE_CHOICES[8][0] : (100, 100, 100, 100, 50, 50)},
                        SYSTEM_WSPACE_EFFECT_CHOICES[2][0] :
                            {SYSTEM_TYPE_CHOICES[3][0] : (25, 10, 10, 10, 10),
                             SYSTEM_TYPE_CHOICES[4][0] : (44, 19, 19, 19, 19),
                             SYSTEM_TYPE_CHOICES[5][0] : (55, 27, 27, 27, 27),
                             SYSTEM_TYPE_CHOICES[6][0] : (68, 34, 34, 34, 34),
                             SYSTEM_TYPE_CHOICES[7][0] : (85, 41, 41, 41, 41),
                             SYSTEM_TYPE_CHOICES[8][0] : (100, 50, 50, 50, 50)},
                        SYSTEM_WSPACE_EFFECT_CHOICES[3][0] :
                            {SYSTEM_TYPE_CHOICES[3][0] : (25, 25, 25, 10, 10),
                             SYSTEM_TYPE_CHOICES[4][0] : (44, 44, 44, 18, 19),
                             SYSTEM_TYPE_CHOICES[5][0] : (55, 55, 55, 22, 27),
                             SYSTEM_TYPE_CHOICES[6][0] : (68, 68, 68, 27, 34),
                             SYSTEM_TYPE_CHOICES[7][0] : (85, 85, 85, 34, 41),
                             SYSTEM_TYPE_CHOICES[8][0] : (100, 100, 100, 50, 50)},
                        SYSTEM_WSPACE_EFFECT_CHOICES[4][0] :
                            {SYSTEM_TYPE_CHOICES[3][0] : (10, 25, 25, 25),
                             SYSTEM_TYPE_CHOICES[4][0] : (18, 44, 44, 44),
                             SYSTEM_TYPE_CHOICES[5][0] : (22, 55, 55, 55),
                             SYSTEM_TYPE_CHOICES[6][0] : (27, 68, 68, 68),
                             SYSTEM_TYPE_CHOICES[7][0] : (34, 85, 85, 85),
                             SYSTEM_TYPE_CHOICES[8][0] : (50, 100, 100, 100)},
                        SYSTEM_WSPACE_EFFECT_CHOICES[5][0] :
                            {SYSTEM_TYPE_CHOICES[3][0] : (10, 25, 10, 10),
                             SYSTEM_TYPE_CHOICES[4][0] : (18, 44, 19, 18),
                             SYSTEM_TYPE_CHOICES[5][0] : (22, 55, 27, 22),
                             SYSTEM_TYPE_CHOICES[6][0] : (27, 68, 34, 27),
                             SYSTEM_TYPE_CHOICES[7][0] : (34, 85, 41, 34),
                             SYSTEM_TYPE_CHOICES[8][0] : (50, 100, 50, 50)}}

SYSTEM_NAME_AUTOCOMPLETE_MAX_RESULTS = 10

WORMHOLE_SIG_MAX_LENGTH = 4
