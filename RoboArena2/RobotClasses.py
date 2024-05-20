from BasicRobot import BasicRobot
from Weapon import Weapon, WeaponName


class Destroyer(BasicRobot):
    def __init__(self, xPos, yPos, movementtype):
        super().__init__(xPos, yPos, movementtype)
        self.health = 50
        self.speed = 10
        self.type = "Destroyer"
        self.weapon = Weapon(WeaponName.bigBullet)


class Tank(BasicRobot):
    def __init__(self, xPos, yPos, movementtype):
        super().__init__(xPos, yPos, movementtype)
        self.health = 100
        self.speed = 5
        self.type = "Tank"
        self.weapon = Weapon(WeaponName.minigun)


class Velocity(BasicRobot):
    def __init__(self, xPos, yPos, movementtype):
        super().__init__(xPos, yPos, movementtype)
        self.health = 75
        self.speed = 15
        self.type = "Velocity"
        self.weapon = Weapon(WeaponName.curveBall)
