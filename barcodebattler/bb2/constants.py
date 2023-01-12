from enum import Enum

EAN_8 = 8
EAN_13 = 13


class Race(Enum):
    MECHANICAL = 0
    ANIMAL = 1
    AQUATIC = 2
    BARD = 3   # バード could be BIRD or BARD, this is an RPG so...
    HUMAN = 4

    ONE_USE_WEAPON = 5
    DURABLE_WEAPON = 6
    ONE_USE_ARMOR = 7
    DURABLE_ARMOR = 8
    POWER = 9


FIGHTERS = [Race.MECHANICAL.value, Race.ANIMAL.value, Race.AQUATIC.value,
            Race.BARD.value, Race.HUMAN.value]
WEAPONS = [Race.ONE_USE_WEAPON.value, Race.DURABLE_WEAPON.value]
ARMORS = [Race.ONE_USE_ARMOR.value, Race.DURABLE_ARMOR.value]


class Job(Enum):
    SOLDIER_0 = 0
    SOLDIER_1 = 1
    SOLDIER_2 = 2
    SOLDIER_3 = 3
    SOLDIER_4 = 4
    SOLDIER_5 = 5
    ST_SOLDIER_6 = 6
    WIZARD_7 = 7
    WIZARD_8 = 8
    WIZARD_9 = 9


SOLDIER_JOBS = [Job.SOLDIER_0, Job.SOLDIER_1, Job.SOLDIER_2, Job.SOLDIER_3, Job.SOLDIER_4, Job.SOLDIER_5]
WIZARD_JOBS = [Job.WIZARD_7, Job.WIZARD_8, Job.WIZARD_9]
ST_SOLDIER_JOBS = [Job.ST_SOLDIER_6]


class BarcodeDigit(Enum):
    HP_TEN_THOUSAND = 0
    HP_THOUSAND = 1
    HP_HUNDRED = 2

    STRENGTH_THOUSAND = 3
    STRENGTH_HUNDRED = 4

    DEFENSE_THOUSAND = 5
    DEFENSE_HUNDRED = 6

    RACE = 7
    JOB = 8

    SPEED = 9

    SPECIAL_TEN = 10
    SPECIAL_UNIT = 11


# TODO WIP
class SpecialAttribute(Enum):
    _01 = (1, '', '職業「1」の相手に対して3倍剣')
    _02 = (2, '', '職業「2」の相手に対して3倍剣')
    _03 = (3, '', '職業「3」の相手に対して3倍剣')
    _04 = (4, '', '職業「4」の相手に対して3倍剣')
    _05 = (5, '', '職業「5」の相手に対して3倍剣')
    _06 = (6, '', '職業「6」の相手に対して3倍剣')
    _07 = (7, '', '職業「7」の相手に対して3倍剣')
    _08 = (8, '', '職業「8」の相手に対して3倍剣')
    _10 = (10, '', '職業「0」の相手に対して3倍剣')
    _11 = (11, '', '種族「1」の相手に対して3倍剣')
    _12 = (12, '', '種族「2」の相手に対して3倍剣')
    _13 = (13, '', '種族「3」の相手に対して3倍剣')
    _14 = (14, '', '種族「4」の相手に対して3倍剣')
    _15 = (15, '', '種族「0」の相手に対して3倍剣')
    _16 = (16, '', '自分の破壊力50％ダウン')
    _17 = (17, '', '自分の破壊力50％アップ')
    _21 = (21, '', '自分の防御力30％アップ')
    _23 = (23, '', '相手のST値30%ダウン')
    _25 = (25, '', '相手のDF値30％ダウン')
    _28 = (28, '', '相手のHP値30％ダウン')
    _30 = (30, '', 'HPアイテムのとき1/2の確率でHP減算')
    _31 = (31, '', 'STアイテムのとき1/2の確率でST減算')
    _32 = (32, '', 'DFアイテムのとき1/2の確率でDF減算')
    _34 = (34, '', '')
    _35 = (35, '', '')
    _37 = (37, '', '自分の先攻率アップ')
    _38 = (38, '', '自分の命中率アップ')
    _39 = (39, '', '相手の命中率アップ')
    _40 = (40, '', '自分の命中率ダウン')
    _41 = (41, '', '相手の命中率ダウン')
    _43 = (43, '', '相手の回復力ダウン')
    _44 = (44, '', '自分の回復力アップ')
    _49 = (49, '', '')
    _50 = (50, '', 'C1/C2 主人公フラグ')
    _57 = (57, '', '')
    _60 = (60, '', '')
    _63 = (63, '', '')
    _65 = (65, '', 'C1/C2 倒すとHP+1000')
    _66 = (66, '', 'C1/C2 倒すとHP+3000')
    _70 = (70, '', 'C1/C2 倒すとST+200')
    _71 = (71, '', 'C1/C2 倒すとST+400')
    _72 = (72, '', 'C1/C2 倒すとST+600')
    _73 = (73, '', 'C1/C2 倒すとST+800')
    _75 = (75, '', 'C1/C2 倒すとDF+200')
    _76 = (76, '', 'C1/C2 倒すとDF+400')
    _77 = (77, '', 'C1/C2 倒すとDF+600')
    _78 = (78, '', 'C1/C2 倒すとDF+800')
    _80 = (80, '', 'C1/C2 倒すとパスコード05')
    _81 = (81, '', 'C1/C2 倒すとパスコード10')
    _82 = (82, '', 'C1/C2 倒すとパスコード15')
    _83 = (83, '', 'C1/C2 倒すとパスコード20')
    _84 = (84, '', 'C1/C2 倒すとパスコード25')
    _85 = (85, '', 'C1/C2 倒すとパスコード35')
    _88 = (88, '', 'C1/C2 倒すとパスコード38')
