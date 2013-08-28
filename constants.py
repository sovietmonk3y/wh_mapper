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

WORMHOLE_SIG_MAX_LENGTH = 4
WORMHOLE_TYPE_MAX_LENGTH = 9
WORMHOLE_TYPES = (
    ('unknown', 'C1-3'),
    ('dangerous', 'C4/C5'),
    ('deadly', 'C6'),
    ('null', 'Nullsec'),
    ('low', 'Lowsec'),
    ('high', 'Highsec')
)
WORMHOLE_LIFE_MAX_LENGTH = 2
WORMHOLE_LIFE_CHOICES = (16, 24, 48)
WORMHOLE_TOTAL_MASS_MAX_LENGTH = 10
WORMHOLE_JUMP_MASS_MAX_LENGTH = 10
