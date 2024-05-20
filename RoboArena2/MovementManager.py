import configparser
import itertools

from BasicRobot import BasicRobot, MovementTyp
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from Weapon import WeaponTyp


class SoundPlayer:
    def __init__(self):
        self.media_player = QMediaPlayer()
        self.sounds = [0, 1]
        self.sounds[0] = QMediaContent(
            QUrl.fromLocalFile("Sounds\\Pistol.mp3")
        )
        self.sounds[1] = QMediaContent(QUrl.fromLocalFile("Sounds\\Dash.mp3"))

        # Get Volume from config file
        config = configparser.ConfigParser()
        config.read("config.txt")  # Path to config file
        self.sound_volume = config.getint("Settings", "game_sounds")

        # Adjust volume
        self.media_player.setVolume(self.sound_volume)

    def play_sound(self, index):
        self.media_player.stop()
        self.media_player.setMedia(self.sounds[index])
        self.media_player.play()

    def stop(self):
        self.media_player.stop()

    def update_sound_volume(self):
        config = configparser.ConfigParser()
        config.read("config.txt")  # Path to config file
        self.sound_volume = config.getint("Settings", "game_sounds")
        self.media_player.setVolume(self.sound_volume)


class MovementManager_:
    waveConter = 0
    weaponsCurrentlyShoot = False
    weaponsCurrentlyShootforSound = False
    ticksToNextShoot = 0
    dashcooldown = 0

    def __init__(self, robot: BasicRobot):
        self.robot = robot
        self.sound_player = SoundPlayer()

    def handleInput(self, keys: dict):
        Movementtyp_ = self.robot.getMovementType()

        match (Movementtyp_):
            case MovementTyp.Line:
                self.moveInLine()
            case MovementTyp.Circle:
                self.moveInCircle()
            case MovementTyp.Wave:
                self.moveInWave()
            case MovementTyp.Player1Control:
                self.handleInputPlayer1(keys)
            case MovementTyp.Player2Control:
                self.handleInputPlayer2(keys)

    def moveInLine(self):
        self.robot.tick(1, 0, (1 / 30))

    def moveInCircle(self):
        self.robot.tick(1, 1, (1 / 30))

    def moveInWave(self):
        if self.waveConter < 50:
            self.robot.tick(1, 1, (1 / 30))
            self.waveConter += 1
        else:
            self.robot.tick(1, -1, (1 / 30))
            self.waveConter += 1
            self.waveConter = self.waveConter % 100

    def handleInputPlayer1(self, keys: dict):
        dashDistance = 8
        dashcooldowntime = 30
        self.reduceTimerToShoot()
        self.reduceAbilityCooldown()
        self.robot.weapon.moveProjectils()
        moveForward = Qt.Key.Key_W
        moveBack = Qt.Key.Key_S
        turnLeft = Qt.Key.Key_A
        turnRight = Qt.Key.Key_D
        shootWeapon = Qt.Key.Key_F
        dashKey = Qt.Key.Key_Shift
        PressedMoveForward = moveForward in keys and keys[moveForward]
        PressedMoveBack = moveBack in keys and keys[moveBack]
        PressedTurnLeft = turnLeft in keys and keys[turnLeft]
        PressedTurnRight = turnRight in keys and keys[turnRight]
        PressedShootWeapon = shootWeapon in keys and keys[shootWeapon]
        PressedDash = dashKey in keys and keys[dashKey]
        dashcooldownNotActive = self.dashcooldown < 1
        self.weaponsCurrentlyShootforSound = False

        moveVec = 0
        rotVec = 0

        if PressedMoveForward and not PressedMoveBack:
            moveVec += 1

        if PressedMoveBack and not PressedMoveForward:
            moveVec -= 1

        if PressedTurnLeft and not PressedTurnRight:
            rotVec -= 1

        if PressedTurnRight and not PressedTurnLeft:
            rotVec += 1

        self.robot.tick(moveVec, rotVec, 1 / 30)
        if PressedShootWeapon and self.ticksToNextShoot < 1:
            self.weaponsCurrentlyShootforSound = True
            match (self.robot.weapon.typ):
                case WeaponTyp.hitscan:
                    self.weaponsCurrentlyShoot = True
                    self.ticksToNextShoot = self.robot.weapon.ticksToNextShoot
                case WeaponTyp.projectile:
                    if self.weaponsCurrentlyShootforSound is True:
                        self.sound_player.play_sound(0)
                    self.weaponsCurrentlyShoot = True
                    self.ticksToNextShoot = self.robot.weapon.ticksToNextShoot
                    self.shootProjectile()
        else:
            match (self.robot.weapon.typ):
                case WeaponTyp.hitscan:
                    self.weaponsCurrentlyShoot = False
                case WeaponTyp.projectile:
                    self.weaponsCurrentlyShoot = (
                        len(self.robot.weapon.listOfPositionForProjectils) > 0
                    )

        self.robot.weaponsCurrentlyShootforSound = (
            self.weaponsCurrentlyShootforSound
        )
        self.robot.weaponsCurrentlyShoot = self.weaponsCurrentlyShoot
        if PressedDash and dashcooldownNotActive:
            self.sound_player.play_sound(1)
            if PressedMoveBack:
                self.dashAbility(dashDistance, -1)
                self.dashcooldown = dashcooldowntime
            else:
                self.dashAbility(dashDistance, 1)
                self.dashcooldown = dashcooldowntime

    def handleInputPlayer2(self, keys: dict):
        dashDistance = 8
        dashcooldowntime = 30
        self.reduceTimerToShoot()
        self.reduceAbilityCooldown()
        self.robot.weapon.moveProjectils()
        moveForward = Qt.Key.Key_Up
        moveBack = Qt.Key.Key_Down
        turnLeft = Qt.Key.Key_Left
        turnRight = Qt.Key.Key_Right
        shootWeapon = Qt.Key.Key_Return
        dashKey = Qt.Key.Key_Adiaeresis
        PressedMoveForward = moveForward in keys and keys[moveForward]
        PressedMoveBack = moveBack in keys and keys[moveBack]
        PressedTurnLeft = turnLeft in keys and keys[turnLeft]
        PressedTurnRight = turnRight in keys and keys[turnRight]
        PressedShootWeapon = shootWeapon in keys and keys[shootWeapon]
        PressedDash = dashKey in keys and keys[dashKey]
        dashcooldownNotActive = self.dashcooldown < 1
        self.weaponsCurrentlyShootforSound = False

        moveVec = 0
        rotVec = 0

        if PressedMoveForward and not PressedMoveBack:
            moveVec += 1

        if PressedMoveBack and not PressedMoveForward:
            moveVec -= 1

        if PressedTurnLeft and not PressedTurnRight:
            rotVec -= 1

        if PressedTurnRight and not PressedTurnLeft:
            rotVec += 1

        self.robot.tick(moveVec, rotVec, 1 / 30)
        if PressedShootWeapon and self.ticksToNextShoot < 1:
            self.weaponsCurrentlyShootforSound = True
            match (self.robot.weapon.typ):
                case WeaponTyp.hitscan:
                    self.weaponsCurrentlyShoot = True
                    self.ticksToNextShoot = self.robot.weapon.ticksToNextShoot
                case WeaponTyp.projectile:
                    if self.weaponsCurrentlyShootforSound is True:
                        self.sound_player.play_sound(0)
                    self.weaponsCurrentlyShoot = True
                    self.ticksToNextShoot = self.robot.weapon.ticksToNextShoot
                    self.shootProjectile()
        else:
            match (self.robot.weapon.typ):
                case WeaponTyp.hitscan:
                    self.weaponsCurrentlyShoot = False
                case WeaponTyp.projectile:
                    self.weaponsCurrentlyShoot = (
                        len(self.robot.weapon.listOfPositionForProjectils) > 0
                    )

        self.robot.weaponsCurrentlyShootforSound = (
            self.weaponsCurrentlyShootforSound
        )
        self.robot.weaponsCurrentlyShoot = self.weaponsCurrentlyShoot
        if PressedDash and dashcooldownNotActive:
            self.sound_player.play_sound(0)
            if PressedMoveBack:
                self.dashAbility(dashDistance, -1)
                self.dashcooldown = dashcooldowntime
            else:
                self.dashAbility(dashDistance, 1)
                self.dashcooldown = dashcooldowntime

    def reduceTimerToShoot(self) -> None:
        if self.ticksToNextShoot > 0:
            self.ticksToNextShoot -= 1

    def dashAbility(self, distance: int, vec: int) -> None:
        tick = 1 / 30
        rotation = 0
        for i in itertools.repeat(None, distance):
            self.robot.tick(vec, rotation, tick)

    def reduceAbilityCooldown(self) -> None:
        if self.dashcooldown > 0:
            self.dashcooldown -= 1

    def shootProjectile(self) -> None:
        self.robot.weapon.addProjectilePosition(self.robot.x, self.robot.y)
        self.robot.weapon.addProjectileVector(self.robot.alpha)
