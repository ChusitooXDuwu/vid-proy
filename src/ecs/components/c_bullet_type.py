from enum import Enum

class BulletType(Enum):
    NORMAL = 0
    SPECIAL = 1

class CBulletType:
    def __init__(self, bullet_type: BulletType = BulletType.NORMAL):
        self.bullet_type = bullet_type
        pass