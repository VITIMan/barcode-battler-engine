from .constants import EAN_8, EAN_13, Job, Race


class BarcodeData():
    def __init__(self, barcode):
        # barcode (バーコード)
        self.barcode = barcode
        # HP
        self.hp = 0
        # ST
        self.st = 0
        # DF
        self.df = 0
        # Speed, DX, (スピード)
        self.speed = 0
        # Race, Tribe, (種族)
        self.race = 0
        # Job, Occupation, (職業)
        self.job = 0
        # Power Points (薬草)
        self.pp = 0
        # Magic Points (魔法)
        self.mp = 0
        # Special Attribute (特殊能力)
        self.special = 0
        # 生死(C2)
        self.live = True

        # Read Mode
        self.post_read = False

        # TODO how was build -- errors -- with_build_over ...

    def is_ean13(self):
        return len(self.barcode) == EAN_13

    def is_ean8(self):
        return len(self.barcode) == EAN_8

    def __str__(self):
        return (f"barcode: {self.barcode}, hp: {self.hp*100}, st: {self.st*100}, df: {self.df*100}, "
                f"speed: {self.speed}, race: {self.race}, job: {self.job}, pp:{self.pp}, mp:{self.mp}, "
                f"special: {self.special}, post_read: {self.post_read}")

    def dict_repr(self):
        return {'hp': self.hp * 100,
                'st': self.st * 100,
                'df': self.df * 100,
                'speed': self.speed,
                'race': self.race,
                'race_name': Race(self.race).name,
                'job': self.job,
                'job_name': Job(self.job).name,
                'mp': self.mp,
                'pp': self.pp,
                'special': self.special}

    def tabular_print(self):
        return f'''+-----------+-----------------+
| Barcode   | {self.barcode:>15} |
| Race      | {Race(self.race).name:>15} |
| Job       | {Job(self.job).name:>15} |
+-----------+-----------------+
| HP        | {self.hp*100:>15} |
| ST        | {self.st*100:>15} |
| DF        | {self.df*100:>15} |
+-----------+-----------------+
| MP        | {self.mp:>15} |
| PP        | {self.pp:>15} |
| Special   | {self.special:>15} |
+-----------+-----------------+
| Read Mode | {'POST_READ' if self.post_read else 'PRE_READ':>15} |
+-----------+-----------------+'''
