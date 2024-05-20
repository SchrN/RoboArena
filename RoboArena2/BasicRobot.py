import configparser
import math
from enum import Enum

from PyQt5.QtCore import Qt
from Terrain import boost, fire, normal, spikes, wall, water
from Weapon import Weapon, WeaponName

config = configparser.ConfigParser()
config.read("config.txt")
selected_map = config.get("Map", "selected_map")
arena_size_width = config.getint("Arena", "arena_size_width")
arena_size_height = config.getint("Arena", "arena_size_height")
tile_size = config.getint("Tiles", "tile_size")
tile_amount = config.getint("Tiles", "tile_amount")


class MovementTyp(Enum):
    Line = "Line"
    Circle = "Circle"
    Wave = "Wave"
    Player1Control = "Player1Control"
    Player2Control = "Player2Control"


class BasicRobot:
    MAX_SPEED = 20
    MAX_TURNSPEED = 10
    MAX_HEALTH = 100

    def __init__(
        self,
        xPos,
        yPos,
        movementtype,
    ):
        self.x = xPos
        self.y = yPos
        self.movementtype = movementtype
        self.tiles = [
            [None for i in range(tile_amount)] for j in range(tile_amount)
        ]
        self.color = Qt.black
        self.turnAccel = 20
        self.acceleration = 10
        self.alpha = 180
        self.radius = 20
        self.speed = 10
        self.turnSpeed = 10
        self.robots = []
        self.moveMultiplier = 1
        self.health = self.MAX_HEALTH
        self.weapon = Weapon(WeaponName.minigun)
        self.weaponsCurrentlyShoot = False
        self.weaponsCurrentlyShootforSound = False
        self.type = "Basic"
        list_with_tiles = []
        config.read("config.txt")
        selected_map = config.get("Map", "selected_map")
        with open(selected_map, "r") as file:  # Opens the textfile
            content = file.read()
            content = content.replace(" ", "").replace("\n", "")
        for letter in content:  # saves every letter in a list
            list_with_tiles.append(letter)
        for y in range(0, tile_amount):  # Iterates through every possible tile
            for x in range(0, tile_amount):
                next_tile = list_with_tiles.pop(
                    0
                )  # first element is deleted and returned from the list
                if next_tile == "w":
                    self.tiles[y][x] = wall()  # The coordinate is marked with
                    # the designated terrain_type
                    # Depending on the type of the tile, different
                    # colors are used
                if next_tile == "a":
                    self.tiles[y][x] = water()
                if next_tile == "f":
                    self.tiles[y][x] = fire()
                if next_tile == "s":
                    self.tiles[y][x] = spikes()
                if next_tile == "b":
                    self.tiles[y][x] = boost()
                if next_tile == "n":
                    self.tiles[y][x] = normal()

    def getMovementType(self):
        return self.movementtype

    # called every game-tick
    def tick(self, moveInputVec, rotationInputVec, deltaTime):
        self.tileLogic()
        self.rotate(rotationInputVec, deltaTime)
        self.move(moveInputVec, deltaTime)

    def tileLogic(self):
        currTile = self.tiles[round(self.y / tile_size)][
            round(self.x / tile_size)
        ]

        self.moveMultiplier = 1
        damage = 0

        self.moveMultiplier = currTile.movement
        damage += currTile.damage

        self.takeDamage(damage)

    # cos(a)^2+sin(a)^2=1 that is why we use this for movement
    def move(self, vec, deltaTime):
        self.calculateSpeed(deltaTime)

        xVelocity = (
            (math.cos(math.radians(self.alpha)))
            * self.speed
            * self.moveMultiplier
        )
        yVelocity = (
            (math.sin(math.radians(self.alpha)))
            * self.speed
            * self.moveMultiplier
        )
        colls = self.collisionDetection(
            self.x + (vec * xVelocity), self.y + (vec * yVelocity)
        )

        self.x = int(colls[0])
        self.y = int(colls[1])

    def rotate(self, vec, deltaTime):
        self.calculateTurnSpeed(deltaTime)
        self.alpha += self.turnSpeed * vec

    def calculateSpeed(self, deltaTime):
        self.speed = min(
            self.speed + self.acceleration * deltaTime, self.MAX_SPEED
        )

    def calculateTurnSpeed(self, deltaTime):
        self.turnSpeed = min(
            self.turnSpeed + self.turnAccel * deltaTime, self.MAX_TURNSPEED
        )

    def collisionDetection(self, endX, endY):
        currX = self.x
        currY = self.y

        endX = round(endX)
        endY = round(endY)

        freeX = self.x
        freeY = self.y

        while (currY != endY) | (currX != endX):
            xDir = endX - currX
            yDir = endY - currY

            if xDir != 0:
                xDir = math.copysign(1, xDir)

            if yDir != 0:
                yDir = math.copysign(1, yDir)

            currX += xDir
            currY += yDir

            for robot in self.robots:
                if robot != self:
                    dist = (currX - robot.x) ** 2 + abs(currY - robot.y) ** 2
                    if dist <= (self.radius + robot.radius) ** 2:
                        return freeX, freeY

            for y in range(
                math.ceil(currX - (self.radius)),
                math.ceil(currX + (self.radius) + 0.1),
                self.radius,
            ):
                for x in range(
                    math.ceil(currY - math.ceil(self.radius)),
                    math.ceil(currY + math.ceil(self.radius) + 0.1),
                    self.radius,
                ):
                    if (
                        self.tiles[math.floor(x / 50)][
                            math.floor(y / 50)
                        ].getCollision()
                        != 0
                    ):
                        return freeX, freeY

            freeX = currX
            freeY = currY

        return endX, endY

    # taking damage function
    def takeDamage(self, Damage: int) -> None:
        if Damage < self.health:
            self.health -= Damage
        else:
            self.health = 0

    # healing funktion
    # no overhealth
    def heal(self, healingAmount: int) -> None:
        if self.health + healingAmount < self.MAX_HEALTH:
            self.health += healingAmount
        else:
            self.health = self.MAX_HEALTH
