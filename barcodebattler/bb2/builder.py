import random
import re
from typing import Literal

from .barcode_data import BarcodeData
from .constants import (ARMORS, EAN_8, EAN_13, FIGHTERS, SOLDIER_JOBS, WEAPONS,
                        WIZARD_JOBS, BarcodeDigit, Job, Race)


class PreReadingMixin():
    def _pre_reading_fighter(self, barcode_data: BarcodeData):
        barcode = barcode_data.barcode
        barcode_data.hp = int(barcode[0:3])
        barcode_data.st = int(barcode[3:5])
        barcode_data.df = int(barcode[5:7])

        # Speed
        # XXX: Barcode Simulator codebase says 11... seems an error
        barcode_data.speed = int(barcode[9])

        # job
        barcode_data.job = int(barcode[8])

        # PP
        barcode_data.pp = 5
        # ST/DF (追加処理)
        if (barcode_data.race == 0 and barcode_data.hp >= 200):
            check_stdf = int(barcode[3:5])
            if check_stdf in [13, 29, 45, 61, 77, 93]:
                barcode_data.st += 100
                barcode_data.df += 100

            barcode_data.st = barcode_data.st + 100

            if barcode_data.st > 256:
                barcode_data.st -= 255
        elif (barcode_data.race == 1 and barcode_data.hp >= 200):
            check_stdf = int(barcode[5:7])
            if check_stdf in [13, 29, 45, 61, 77, 93]:
                barcode_data.st += 100
                barcode_data.df += 100

            barcode_data.df = barcode_data.df + 100

            if barcode_data.df > 256:
                # XXX: Barcode Simulator codebase, sounds strange, should be DF?
                barcode_data.df = barcode_data.st - 255
        elif (barcode_data.race == 2 and barcode_data.hp >= 200):
            barcode_data.st += 100
            barcode_data.df += 100

        # MP
        if (barcode_data.job >= 6):
            barcode_data.mp = 10
        else:
            barcode_data.mp = 0

    def _pre_reading_weapon(self, barcode_data):
        barcode = barcode_data.barcode
        barcode_data.st = int(barcode[3:5])
        if barcode_data.special == 31 and random.randrange(0, 2) == 0:
            barcode_data.st = 0 - barcode_data.st

    def _pre_reading_armor(self, barcode_data):
        barcode = barcode_data.barcode
        barcode_data.df = int(barcode[5:7])
        if barcode_data.special == 32 and random.randrange(0, 2) == 0:
            barcode_data.df = 0 - barcode_data.df

    def _pre_reading_item(self, barcode_data):
        barcode = barcode_data.barcode
        # Get "job/order" for buff items (HPアイテムの種類判別用に職業保存)
        barcode_data.job = int(barcode[8])

        # HP item (HPアイテム)
        if barcode_data.job in list(range(0, 5)):
            barcode_data.hp = int(barcode[0:3])
            if barcode_data.special == 30 and random.randrange(0, 2) == 0:
                barcode_data.hp = 0 - barcode_data.hp

        # info card (情報カード)
        elif barcode_data.job in [5, 6]:
            pass
        # MP/PP items (薬草アップ)
        elif barcode_data.job == 7:
            barcode_data.pp = int(barcode[3:5])
        else:
            barcode_data.mp = int(barcode[5:7])

    def pre_reading(self, barcode_data: BarcodeData):
        '''
        //前読み
        '''
        barcode = barcode_data.barcode
        # Get race from barcode digit / 種族取得
        barcode_data.race = int(barcode[BarcodeDigit.RACE.value])

        # Get special value from barcode digits / 特殊能力
        barcode_data.special = int(barcode[10:12])

        # Characters, fighters cards (キャラクター)
        if barcode_data.race in FIGHTERS:
            self._pre_reading_fighter(barcode_data)
        # ST items (st アイテム)
        elif (barcode_data.race in WEAPONS):
            self._pre_reading_weapon(barcode_data)
        # DF items (DF アイテム)
        elif (barcode_data.race in ARMORS):
            self._pre_reading_armor(barcode_data)
        # HP items, Info cards, MP/PP items HPアイテム/情報カード/薬草アップ/MPアップ
        else:
            self._pre_reading_item(barcode_data)


class PostReadingMixin():
    def _post_reading_fighter(self, barcode_data: BarcodeData, shift=-8):
        '''
        '''
        ean_shift = self.get_ean_shift(barcode_data)
        barcode = barcode_data.barcode
        # HP
        barcode_data.hp = int(str(int(int(barcode[11 + ean_shift + shift]) / 2)) +
                              barcode[10 + ean_shift + shift] + barcode[9 + ean_shift + shift])
        # ST
        tmpst = int(barcode[10 + ean_shift + shift]) + 7
        if tmpst > 11:
            tmpst = tmpst - 10

        tmpst2 = int(barcode[9 + ean_shift + shift]) + 5 % 10
        if tmpst2 >= 10:
            tmpst2 = tmpst2 - 10
        barcode_data.st = int(str(tmpst) + str(tmpst2))

        # DF
        tmpdf = int(barcode[9 + ean_shift + shift]) + 7
        if tmpdf >= 10:
            tmpdf = tmpdf - 10

        tmpdf2 = int(barcode[8 + ean_shift + shift]) + 7
        if tmpdf2 >= 10:
            tmpdf2 = tmpdf2 - 10
        barcode_data.df = int(str(tmpdf) + str(tmpdf2))

        # Speed
        barcode_data.speed = int(barcode[10 + ean_shift])

        # Job
        barcode_data.job = int(barcode[5]) if barcode_data.is_ean13() else 4

        # PP
        barcode_data.pp = 5

        # MP
        # EAN-13
        if barcode_data.is_ean13():
            if barcode_data.job >= 6:
                barcode_data.mp = 10
            else:
                barcode_data.mp = 0
        # EAN-8
        else:
            barcode_data.mp = 0

    def get_ean_shift(self, barcode_data: BarcodeData):
        return 0 if barcode_data.is_ean13() else self.ean8_shift

    def _post_reading_weapon(self, barcode_data: BarcodeData):
        barcode = barcode_data.barcode
        ean_shift = self.get_ean_shift(barcode_data)
        if int(barcode[10 + ean_shift]) in [5, 6, 7, 8]:
            barcode_data.st = int("1" + str((int(barcode[9 + ean_shift]) + 5) % 10))
        elif int(barcode[10 + ean_shift]) in [3, 4]:
            barcode_data.st = int("3" + str((int(barcode[9 + ean_shift]) + 5) % 10))
        else:
            barcode_data.st = int("2" + str((int(barcode[9 + ean_shift]) + 5) % 10))

    def _post_reading_armor(self, barcode_data: BarcodeData):
        barcode = barcode_data.barcode
        ean_shift = self.get_ean_shift(barcode_data)
        if int(barcode[9 + ean_shift]) in [3, 4, 5, 6]:
            barcode_data.df = int(str((int(barcode[8 + ean_shift]) + 7) % 10))
        elif int(barcode[9 + ean_shift]) in [1, 2]:
            barcode_data.df = int("2" + str((int(barcode[8 + ean_shift]) + 7) % 10))
        else:
            barcode_data.df = int("1" + str((int(barcode[8 + ean_shift]) + 7) % 10))

    def _post_reading_item(self, barcode_data: BarcodeData):
        barcode = barcode_data.barcode
        ean_shift = self.get_ean_shift(barcode_data)
        barcode_data.job = 0
        barcode_data.hp = int(str(int(int(barcode[11 + ean_shift]) / 8)) +
                              barcode[10 + ean_shift] + barcode[9 + ean_shift])

    def _post_reading_special(self, barcode_data: BarcodeData):
        ''' Get Special Attribute # 特殊能力
        '''
        barcode = barcode_data.barcode
        ean_shift = self.get_ean_shift(barcode_data)
        tmpspecial = barcode[8 + ean_shift]
        if tmpspecial in [0, 1, 2, 3]:
            barcode_data.special = int(barcode[10 + ean_shift])
        elif tmpspecial in [8, 9]:
            barcode_data.special = int("2" + barcode[10 + ean_shift])
        else:
            barcode_data.special = int("1" + barcode[10 + ean_shift])

    def post_reading(self, barcode_data: BarcodeData, shift=2):
        '''
        Post reading phase
        '''
        barcode = barcode_data.barcode
        ean_shift = self.get_ean_shift(barcode_data)

        # 先頭へのズレの場合
        if shift == 2:
            shift = -8 + ean_shift

        # 種族取得
        barcode_data.race = int(barcode[12 + ean_shift])
        # Characters (キャラクター)
        if barcode_data.race in FIGHTERS:
            self._post_reading_fighter(barcode_data, shift=shift)
        # ST item アイテム
        elif barcode_data.race in WEAPONS:
            self._post_reading_weapon(barcode_data)
        # DF item アイテム
        elif barcode_data.race in ARMORS:
            self._post_reading_armor(barcode_data)
        # HP item アイテム
        else:
            self._post_reading_item(barcode_data)
        # Special Attribute (特殊能力)
        self._post_reading_special(barcode_data)


SOLDIER = 'SOLDIER'
WIZARD = 'WIZARD'


class BarcodeBattler2Builder(PreReadingMixin, PostReadingMixin):

    def __init__(self, shift: int = 0, c1_flag: bool = False, hero_flag: bool = False, item_flag: bool = False,
                 expected_job: Literal[SOLDIER, WIZARD] = ''):
        '''
        - shift:

        Flags for `build_over` mode
        - c1_flag:
        - hero_flag:
        - item_flag:
        - expected_job:
        '''
        self.shift = shift
        self.c1_flag = c1_flag
        self.hero_flag = hero_flag
        self.item_flag = item_flag
        self.expected_job = expected_job

        # post reading helper functions shares the same code but the barcode positions are different
        self.ean8_shift = -5

    def build(self, barcode: str) -> BarcodeData:
        self.check_barcode_length(barcode)
        self.check_digits(barcode)

        barcode_data = BarcodeData(barcode)

        if self.prepost_check(barcode):
            self.pre_reading(barcode_data)
        else:
            barcode_data.post_read = True
            self.post_reading(barcode_data, shift=self.shift)
        return barcode_data

    def _calc_c1_reading(self, barcode_data: BarcodeData):
        # TODO Needs review, not enterily correct
        # HP,ST,DFを元に再計算
        barcode_data.hp = int(barcode_data.hp / 10)
        barcode_data.st = int(barcode_data.st / 10) + 1
        barcode_data.df = int(barcode_data.df / 10) + 3

    def _check_previous_barcode_data(self, barcode_data: BarcodeData):
        ''' Check barcode data information from initial build to be valid for the
        second barcode data
        '''
        # 1枚目はアイテム不可
        # First read cannot be an item, READ_ERROR_FIRST_ITEM
        if barcode_data.race > 4:
            raise ValueError('First card cannot be an item.')

        # 主人公フラグ
        if (self.hero_flag and barcode_data.special not in [18, 50] and not barcode_data.post_read):
            raise ValueError('First card is not a hero')

        # 主人公でHP6000、ST2000、DF2000以上ははじく
        if barcode_data.special == 50 and (barcode_data.hp >= 60 or
                                           barcode_data.st >= 20 or
                                           barcode_data.df >= 20):
            raise ValueError('Hero exceed the valid stats')

        # heroフラグたっている（＝C1、C2モードのときはHP、ST、DFを再計算）
        # if (hero and post_read_flag and barcode_data.race <= 4):
        if (self.hero_flag and barcode_data.post_read and barcode_data.race in FIGHTERS):
            self._calc_c1_reading(barcode_data)
        if self.expected_job == SOLDIER:
            # 戦士のみ受け付けで魔法使いだった場合
            # if barcode_data.job > 6:
            if barcode_data.job in WIZARD_JOBS:
                raise ValueError('Expected WIZARD first card')
        elif self.expected_job == WIZARD:
            # 魔法使いのみ受け付けで戦士だった場合
            # if barcode_data.job <= 6:
            if barcode_data.job in SOLDIER_JOBS + [Job.ST_SOLDIER_6]:
                raise ValueError('Expected SOLDIER first card')

    def _chack_similar_barcode(self, previous_barcode_data: BarcodeData,
                               barcode_data: BarcodeData):
        ''' Check if barcodes are similar. (同じバーコードは合体不可)
        '''
        barcode_check = previous_barcode_check = ""
        barcode = barcode_data.barcode
        if len(barcode) >= 13:
            barcode_check = barcode[6:13]
        else:
            barcode_check = barcode[1:8]

        previous_barcode = previous_barcode_data.barcode
        if len(previous_barcode) >= 13:
            previous_barcode_check = previous_barcode[6:13]
        else:
            previous_barcode_check = previous_barcode[1:8]

        if barcode_check == previous_barcode_check:
            raise ValueError('Very similar barcode. Invalid')

    def _validate_both_barcode_data(self, previous_barcode_data: BarcodeData,
                                    barcode_data: BarcodeData):
        ''' Checks for previous_barcode_data
        '''
        # C2アイテム固定チェック
        if previous_barcode_data is not None and self.item_flag:
            if barcode_data.race <= 4:
                # 合体できないバーコードであることを確認
                if (barcode_data.race != previous_barcode_data.race or
                        barcode_data.job != previous_barcode_data.job):
                    raise ValueError('')  # TODO

        # Check if barcodes are similar. (同じバーコードは合体不可)
        self._check_similar_barcode(previous_barcode_data, barcode_data)

        # HPアイテム系チェック
        if barcode_data.race == Race.POWER.value:
            # 情報カードは入力不可
            if barcode_data.job in [5, 6] and not self.c1_flag:
                raise ValueError('Info card only valid for C1 Mode.')
            # TODO Seems not to be in this conditional. It is in BarcodeBattler2Simulator codebase
            # SOLDIER JOBS cannot increase MP. (戦士はMPアップ不可)
            if previous_barcode_data.job <= 6 and barcode_data.job >= 8:
                raise ValueError('Soldier jobs cannot increase MP.')

        # Wizards cannot use weapons and armors. (魔法使いは武器・防具は不可)
        # if barcode_data.job >= 7 and barcode_data.race in [5, 6, 7, 8]:
        # TODO Should be previous_barcode_data.job seems an error in BarcodeBattler2Simulator codebase
        if previous_barcode_data.job >= 7 and barcode_data.race in WEAPONS + ARMORS:
            raise ValueError('Weapons and armos are note allowed for Wizards.')

    def build_over(self, previous_barcode_data: BarcodeData, barcode: str) -> BarcodeData:
        ''' Build a second barcode data, based on previous barcode data. to be compatible
        or not
        '''
        barcode_data = self.build(barcode)
        self._check_previous_barcode_data(previous_barcode_data)
        self._validate_both_barcode_data(previous_barcode_data, barcode_data)
        return barcode_data

    def check_barcode_length(self, barcode: str) -> bool:
        ''' Barcodes EAN_13 & EAN_8 only allowed
        '''
        if not re.match(r'[0-9]+', barcode):
            raise ValueError('Only digits 0-9 allowed')
        if len(barcode) != EAN_13 and len(barcode) != EAN_8:
            raise ValueError('Invalid barcode length')
        return True

    def check_digits(self, barcode: str) -> bool:
        ''' Hashing validator for barcode string
        '''
        if len(barcode) == EAN_8:
            barcode = barcode.zfill(EAN_13)

        sum_odds = sum([int(_) for _ in barcode[0:len(barcode) - 2:2]])
        sum_evens = sum([int(_) for _ in barcode[1:len(barcode) - 1:2]])

        hash_barcode = 10 - ((sum_odds + sum_evens * 3) % 10)
        if hash_barcode == 10:
            hash_barcode = 0

        last_digit = int(barcode[-1])
        if hash_barcode != last_digit:
            raise ValueError('Hash invalid for this barcode.')
        return True

    def prepost_check(self, barcode: str) -> bool:
        '''
        Read mode selection, returns bool
        if True will be pre_reading mode, else post_reading mode
        前読みか後読みか判別 true:前読み　false:後読み
        '''
        if len(barcode) == EAN_8:
            return False
        first_digit = int(barcode[0])
        if first_digit in [0, 1]:
            if int(barcode[7]) >= 0 and int(barcode[7]) <= 4:
                return True
            else:
                # 前読みとして読んだ場合HP5000、ST1900、DF1900以下の場合は5-9でも前読みに
                hp = int(barcode[0:3])
                st = int(barcode[3:5])
                df = int(barcode[5:7])
                if hp <= 50 and st <= 19 and df <= 19:
                    return True
                else:
                    return False
        else:
            return True if int(barcode[2]) == 9 and int(barcode[9]) == 5 else False
