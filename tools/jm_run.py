import sys
from jm import *
CFG = {   # model: (legs, mode)
 'Sporeling/SporelingPlayer.m2': ({'L': (7, 16, 23), 'R': (8, 19, 25)}, 'full'),
 'MoguFemale/MoguPlayerFemale.m2': ({'L': (6, 12, 17), 'R': (7, 13, 18)}, 'full'),
 'LostOne/LostOnePlayer.m2': ({'L': (15, 25, 33), 'R': (14, 24, 31)}, 'full'),
 'MoargEngineer/MoargPlayerMale.m2': ({'L': (5, 8, 17), 'R': (6, 10, 19)}, 'full'),
 'MoargMinion2/MoargPlayerFemale.m2': ({'L': (6, 13, 18), 'R': (5, 12, 17)}, 'full'),
 'QuirajBattleguard/QirajiMale.m2': ({'L': (5, 14, 19), 'R': (6, 15, 20)}, 'full'),
 'Lich2/LichPlayerMale.m2': ({}, 'full'),
 'TrollLich/LichPlayerFemale.m2': ({}, 'full'),
 'Nerubian/NerubianPlayerMale.m2': ({}, 'full'),
 'NerubianPriest2/NerubianPlayerFemale.m2': ({}, 'full'),
 'TitanFemale/TitanPlayerFemale.m2': ({'L': (6, 12, 18), 'R': (7, 13, 19)}, 'mount'),
 'Dreadlord/DreadlordPlayerFemale.m2': ({'L': (5, 13, 21), 'R': (6, 14, 22)}, 'mount'),
 'DreadlordShadowlands/DreadlordPlayerMale.m2': ({'L': (17, 23, 31), 'R': (16, 22, 28)}, 'mount'),
}
if __name__ == '__main__':
    import prev
    for n in sys.argv[2:] or CFG:
        lg, mode = CFG[n]; print(n, prev.preview(n, 'jm_%s.png' % os.path.basename(n)[:-3], True, lg) if False else '')
