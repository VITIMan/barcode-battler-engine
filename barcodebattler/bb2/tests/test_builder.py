import unittest

from parameterized import parameterized

from barcodebattler.bb2.builder import BarcodeBattler2Builder

# BBOX2_1 extracted from:
# https://wikiwiki.jp/barcode/%E5%A4%96%E4%BC%9D1%20%E7%99%BD%E9%AD%94%E8%A1%93%E7%8E%8B%E3%83%9B%E3%82%AB%E3%83%AD%E3%83%B3%E3%83%80%E3%83%BC%E3%81%AE%E9%99%B0%E8%AC%80%20%E3%82%AB%E3%83%BC%E3%83%89%E3%83%AA%E3%82%B9%E3%83%88  # noqa


class TestBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = BarcodeBattler2Builder()

    @parameterized.expand([
        ('G-SOLDIER-1', '0401207237501', 4000, 1200, 700, 7, 2, 3, 50),
        ('G-SOLDIER-2', '0341011384506', 3400, 1000, 1100, 4, 3, 8, 50),
        ('G-ENEMY-1', '0521209429381', 5200, 1200, 900, 9, 4, 2, 38),
        ('G-ENEMY-2', '0551512179710', 5500, 1500, 1200, 9, 1, 7, 71),
        ('G-ENEMY-3', '0642013418764', 6400, 2000, 1300, 8, 4, 1, 76),
        ('G-ENEMY-4', '0592316368252', 5900, 2300, 1600, 8, 3, 6, 25),
        ('G-ENEMY-5', '0601814354701', 6000, 1800, 1400, 4, 3, 5, 70),
        ('G-ENEMY-6', '0682518275806', 6800, 2500, 1800, 5, 2, 7, 80),
        ('G-ENEMY-7', '0752716104700', 7500, 2700, 1600, 4, 1, 0, 70),
        ('G-ENEMY-8', '0792818344703', 7900, 2800, 1800, 4, 3, 4, 70),
        ('G-ENEMY-9', '0873020325657', 8700, 3000, 2000, 5, 3, 2, 65),
        ('G-ENEMY-10', '0842927378288', 8400, 2900, 2700, 8, 3, 7, 28),
        ('G-ENEMY-11', '0963225309764', 9600, 3200, 2500, 9, 3, 0, 76),
        ('G-ENEMY-12', '1003430079812', 10000, 3400, 3000, 9, 0, 7, 81),
        ('G-ENEMY-13', '1153229269235', 11500, 3200, 2900, 9, 2, 6, 23),
        ('G-ENEMY-14', '1203531475654', 12000, 3500, 3100, 5, 4, 7, 65),
        ('G-ENEMY-15', '1253833055719', 12500, 3800, 3300, 5, 0, 5, 71),
        ('G-ENEMY-16', '1383634085766', 13800, 3600, 3400, 5, 0, 8, 76),
        ('G-ENEMY-17', '1474036245664', 14700, 4000, 3600, 5, 2, 4, 66),
        ('G-ENEMY-18', '1544235125774', 15400, 4200, 3500, 5, 1, 2, 77),
        ('G-ENEMY-19', '1603938185284', 16000, 3900, 3800, 5, 1, 8, 28),
        ('G-ENEMY-20', '1734337205713', 17300, 4300, 3700, 5, 2, 0, 71),
        ('G-BOSS-1', '1954840299829', 19500, 4800, 4000, 9, 2, 9, 82),
        ('G-BOSS-1', '0120000905140', 1200, 0, 0, 0, 9, 0, 14),
        ('G-POWER-1', '0160000903159', 1600, 0, 0, 0, 9, 0, 15),
        ('G-POWER-2', '0120000903115', 1200, 0, 0, 0, 9, 0, 11),
        ('G-WEAPON-1', '0000600602017', 0, 600, 0, 0, 6, 0, 1),
        ('G-WEAPON-2', '0001400500022', 0, 1400, 0, 0, 5, 0, 2),
        ('G-PROTECTOR-1', '0000010802212', 0, 0, 1000, 0, 8, 0, 21),
        ('G-PROTECTOR-2', '0000019700328', 0, 0, 1900, 0, 7, 0, 32)
    ])
    def test_barcodes_bbox2_1_fighters(self, _, barcode, hp, st, df, speed, race, job, special):
        barcode_data = self.builder.build(barcode)

        self.assertEqual(barcode_data.hp, hp / 100)
        self.assertEqual(barcode_data.st, st / 100)
        if special == 32 and barcode_data.df < 0:  # TODO include in Enum
            self.assertEqual(barcode_data.df, -(df / 100))
        else:
            self.assertEqual(barcode_data.df, df / 100)
        self.assertEqual(barcode_data.speed, speed)
        self.assertEqual(barcode_data.race, race)
        self.assertEqual(barcode_data.job, job)
        self.assertEqual(barcode_data.special, special)
        self.assertFalse(barcode_data.post_read)

    @parameterized.expand([
        ('G-M.POINT-1', '0000006990077', 6, 0, 9, 9, 7),
        ('G-P.POINT-1', '0000600970444', 0, 6, 9, 7, 44)
    ])
    def test_barcodes_bbox2_1_power_items(self, _, barcode, mp, pp, race, job, special):
        barcode_data = self.builder.build(barcode)
        self.assertEqual(barcode_data.mp, mp)
        self.assertEqual(barcode_data.pp, pp)
        self.assertEqual(barcode_data.race, race)
        self.assertEqual(barcode_data.job, job)
        self.assertEqual(barcode_data.special, special)
        self.assertFalse(barcode_data.post_read)
