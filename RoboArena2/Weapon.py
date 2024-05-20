import math
from enum import Enum


class WeaponTyp(Enum):
    hitscan = "hitscan"
    projectile = "projectile"


class WeaponName(Enum):
    basicHitscan = "basicHitscan"
    basicLaser = "basicLaser"
    strongLaser = "strongLaser"
    sniper = "sniper"
    basicProjectile = "basicProjectile"
    minigun = "minigun"
    bigBullet = "bigBullet"
    curveBall = "curveBall"


class Weapon:
    def __init__(self, name: WeaponName) -> None:
        self.damage = 0
        self.size = 0
        self.ticksToNextShoot = 10
        self.typ = WeaponTyp.hitscan
        self.name = name
        self.projectileSpeed = 10
        self.extraTurnig = 0
        self.listOfPositionForProjectils = []
        self.listOfVectorsForProjectils = []
        self.listOfDirections = []
        self.getWeaponStats(name)

    def addProjectilePosition(self, x: int, y: int) -> None:
        self.listOfPositionForProjectils.append([x, y])

    def addProjectileVector(self, direction: int) -> None:
        xVelocity = (math.cos(math.radians(direction))) * self.projectileSpeed
        xVelocity = int(xVelocity)
        yVelocity = (math.sin(math.radians(direction))) * self.projectileSpeed
        yVelocity = int(yVelocity)
        self.listOfVectorsForProjectils.append([xVelocity, yVelocity])
        self.listOfDirections.append(direction + self.extraTurnig)

    def newXVelocity(self, posInList: int) -> int:
        xVelocity = (
            math.cos(math.radians(self.listOfDirections[posInList]))
        ) * self.projectileSpeed
        xVelocity = int(xVelocity)
        self.listOfDirections[posInList] += self.extraTurnig
        return xVelocity

    def newYVelocity(self, posInList: int) -> int:
        yVelocity = (
            math.sin(math.radians(self.listOfDirections[posInList]))
        ) * self.projectileSpeed
        yVelocity = int(yVelocity)
        self.listOfDirections[posInList] += self.extraTurnig
        return yVelocity

    def moveProjectils(self) -> None:
        if len(self.listOfPositionForProjectils) == len(
            self.listOfVectorsForProjectils
        ):
            for i in range(len(self.listOfPositionForProjectils)):
                self.listOfPositionForProjectils[i][
                    0
                ] += self.listOfVectorsForProjectils[i][0]
                self.listOfPositionForProjectils[i][
                    1
                ] += self.listOfVectorsForProjectils[i][1]
                if self.extraTurnig > 0:
                    self.listOfVectorsForProjectils[i][0] = self.newXVelocity(
                        i
                    )
                    self.listOfVectorsForProjectils[i][1] = self.newYVelocity(
                        i
                    )

    def deleatProjectile(self, PosInList: int) -> None:
        try:
            del self.listOfPositionForProjectils[PosInList]
        except Exception:
            pass
        try:
            del self.listOfVectorsForProjectils[PosInList]
        except Exception:
            pass
        try:
            del self.listOfDirections[PosInList]
        except Exception:
            pass

    def getWeaponStats(self, name: WeaponName) -> None:
        match (name):
            case WeaponName.basicHitscan:
                self.damage = 10
                self.size = 1000
                self.ticksToNextShoot = 8
                self.typ = WeaponTyp.hitscan
            case WeaponName.basicLaser:
                self.damage = 3
                self.size = 400
                self.ticksToNextShoot = 0
                self.typ = WeaponTyp.hitscan
            case WeaponName.strongLaser:
                self.damage = 7
                self.size = 200
                self.ticksToNextShoot = 0
                self.typ = WeaponTyp.hitscan
            case WeaponName.sniper:
                self.damage = 50
                self.size = 2000
                self.ticksToNextShoot = 20
                self.typ = WeaponTyp.hitscan
            case WeaponName.basicProjectile:
                self.damage = 10
                self.size = 5
                self.ticksToNextShoot = 4
                self.projectileSpeed = 40
                self.typ = WeaponTyp.projectile
            case WeaponName.minigun:
                self.damage = 7
                self.size = 5
                self.ticksToNextShoot = 10
                self.projectileSpeed = 40
                self.typ = WeaponTyp.projectile
            case WeaponName.bigBullet:
                self.damage = 20
                self.size = 40
                self.ticksToNextShoot = 14
                self.projectileSpeed = 30
                self.typ = WeaponTyp.projectile
            case WeaponName.curveBall:
                self.damage = 40
                self.size = 20
                self.ticksToNextShoot = 10
                self.projectileSpeed = 30
                self.extraTurnig = 5
                self.typ = WeaponTyp.projectile
