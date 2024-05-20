import configparser
import importlib
import os
import sys

from Arena import Arena
from PyQt5.QtCore import QCoreApplication, QEvent, Qt, QTimer, QUrl
from PyQt5.QtGui import QFont, QKeyEvent, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel, QMainWindow,
                             QMessageBox)
from PyQt5.uic import loadUi

# Set up config file
config = configparser.ConfigParser()
config.read("config.txt")

flag = 0


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFocus()
        self.width = 1000
        self.height = 1000

        # Load and display the image
        self.loadImage(r"MenuAssets\\arobot.jpg")

        # Load the UI file
        loadUi("MenuAssets\\MainMenu.ui", self)

        # Set the window title and add a headline
        self.setWindowTitle("Roboarena")

        # Make the window non-resizable
        self.setFixedSize(self.size())

        # Access the elements defined in the UI here
        # self.button.clicked.connect(self.buttonClicked)
        self.PlayButton.clicked.connect(self.playClicked)
        self.SettingsButton.clicked.connect(self.settingsClicked)
        self.QuitButton.clicked.connect(self.quitClicked)
        self.ExtrasButton.clicked.connect(self.extrasClicked)

    def update_position(self):
        position = self.getWindowPos()
        x_coord = position.x()
        y_coord = position.y()

        config.read("config.txt")  # Path to config file
        config.set("Position", "x", str(x_coord))
        config.set("Position", "y", str(y_coord))

        # Overwrite config file
        with open("config.txt", "w") as config_file:
            config.write(config_file)

    def loadImage(self, path):
        # Path to the image (use the absolute path)
        image_path = os.path.abspath(path)

        # Load the image and create a QLabel widget
        pixmap = QPixmap(image_path)
        image_label = QLabel(self)

        # Resize the image to match the window size
        pixmap = pixmap.scaled(self.width, self.height)

        # Set the pixmap to the QLabel
        image_label.setPixmap(pixmap)

        # Set the position and size of the QLabel to cover the whole window
        image_label.setGeometry(0, 0, self.width, self.height)

    def playClicked(self):
        self.setCentralWidget(PlayMenu())

    def settingsClicked(self):
        self.setCentralWidget(SettingsMenu())

    def quitClicked(self):
        self.close()
        sys.exit()

    def extrasClicked(self):
        self.setCentralWidget(ExtrasMenu())


class PlayMenu(MainMenu):
    def __init__(self):
        super().__init__()

        self.loadImage(r"MenuAssets\\brobot.png")

        loadUi("MenuAssets\\PlayMenu.ui", self)

        self.SoloButton.clicked.connect(self.SoloClicked)
        self.BackButton.clicked.connect(self.BackClicked)

        # Set the window title and add a headline
        self.setWindowTitle("Play Menu")

    def SoloClicked(self):
        self.setCentralWidget(SoloMenu())

    def BackClicked(self):
        self.setCentralWidget(MainMenu())


class SettingsMenu(MainMenu):
    def __init__(self):
        super().__init__()

        self.loadImage(r"MenuAssets\\robotc.png")

        loadUi("MenuAssets\\SettingsMenu.ui", self)

        self.BackButton.clicked.connect(self.BackClicked)

        # Connect the slider valueChanged signal to a function
        self.SoundSlider.valueChanged.connect(self.sliderValueChanged)
        self.SoundSlider_2.valueChanged.connect(self.sliderValueChanged2)

        # Get music and game_sound volume from config file
        config.read("config.txt")  # Path to config file
        music = config.getint("Settings", "music")
        game_sounds = config.getint("Settings", "game_sounds")

        # QLabel for displaying volume text music
        self.musicLabel = QLabel(self)
        self.musicLabel.setGeometry(600, 370, 181, 121)

        # QLabel for displaying volume text game sounds
        self.game_sound_Label = QLabel(self)
        self.game_sound_Label.setGeometry(600, 570, 181, 121)

        # Display Volume Label and change font
        font = QFont()
        font.setPointSize(14)  # Set the desired font size
        font.setBold(True)  # Optionally, set the font weight to bold
        self.musicLabel.setFont(font)
        self.musicLabel.setText(f"Volume: {music}")
        self.musicLabel.setStyleSheet("color: white;")  # Set white font color
        self.game_sound_Label.setFont(font)
        self.game_sound_Label.setText(f"Volume: {game_sounds}")
        self.game_sound_Label.setStyleSheet(
            "color: white;"
        )  # Set white font color

        # Set the window title and add a headline
        self.setWindowTitle("Settings Menu")

    def sliderValueChanged(self, value):
        # Update the configuration file with the new volume value

        config.read("config.txt")  # Path to config file
        config.set("Settings", "music", str(value))

        # Overwrite config file
        with open("config.txt", "w") as config_file:
            config.write(config_file)

        self.musicLabel.setText(f"Volume: {value}")

    def sliderValueChanged2(self, value):
        # Update the configuration file with the new volume value

        config.read("config.txt")  # Path to config file
        config.set("Settings", "game_sounds", str(value))

        # Overwrite config file
        with open("config.txt", "w") as config_file:
            config.write(config_file)

        self.game_sound_Label.setText(f"Volume: {value}")

    def BackClicked(self):
        self.setCentralWidget(MainMenu())


class ExtrasMenu(MainMenu):
    def __init__(self):
        super().__init__()

        self.loadImage(r"MenuAssets\\scaryrobot.png")

        loadUi("MenuAssets\\ExtrasMenu.ui", self)

        self.MapEditorButton.clicked.connect(self.MapEditorClicked)
        self.BackButton.clicked.connect(self.BackClicked)

        # Set the window title and add a headline
        self.setWindowTitle("Extras")

    def MapEditorClicked(self):
        MapEditor = importlib.import_module("MapEditor").MapEditor
        map_editor_window = MapEditor()
        map_editor_window.show()

    def BackClicked(self):
        self.setCentralWidget(MainMenu())


class SoloMenu(MainMenu):
    def __init__(self):
        super().__init__()

        self.loadImage(r"MenuAssets\\robotc.png")

        loadUi("MenuAssets\\SoloMenu.ui", self)

        # To prevent starting the game without robot/arena chosen
        self.robot_selected = False
        self.arena_selected = False

        self.PlayButton.clicked.connect(self.PlayClicked)
        self.RobotButtonP1.clicked.connect(self.RobotClickedP1)
        self.RobotButtonP2.clicked.connect(self.RobotClickedP2)
        self.ArenaButton.clicked.connect(self.ArenaClicked)
        self.BackButton.clicked.connect(self.BackClicked)

        # Set the window title and add a headline
        self.setWindowTitle("Local")

        # To select Robot class
        self.robot_class_list_P1 = ["Destroyer", "Tank", "Velocity"]
        self.robot_class_list_P2 = ["Destroyer", "Tank", "Velocity"]

    def PlayClicked(self):
        if (
            self.RobotButtonP1.text() == "Robot Player1"
            or self.RobotButtonP2.text() == "Robot Player2"
        ):
            error_message = "No Robot selected"
            QMessageBox.critical(self, "Error", error_message)
        elif self.ArenaButton.text() == "Arena":
            error_message = "No Arena selected"
            QMessageBox.critical(self, "Error", error_message)
        else:
            config.read("config.txt")  # Path to config file
            config.set("Settings", "soundtrack", "Sounds\\Drive.mp3")
            with open("config.txt", "w") as config_file:
                config.write(config_file)
            arena = Arena()
            arena.listOfThreads.clear()
            arena.robots.clear()
            self.setCentralWidget(arena)
            arena.setFocusPolicy(Qt.StrongFocus)
            key_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.NoModifier)
            QCoreApplication.postEvent(arena, key_event)
            arena.start_game()
            arena.runTask()

    def RobotClickedP1(self):
        robot_class = self.robot_class_list_P1.pop(0)
        self.robot_class_list_P1.append(robot_class)
        self.RobotButtonP1.setText(robot_class)
        config.read("config.txt")  # Path to config file
        config.set("Class", "selected_class_p1", robot_class)
        # Overwrite config file
        with open("config.txt", "w") as config_file:
            config.write(config_file)

    def RobotClickedP2(self):
        robot_class = self.robot_class_list_P2.pop(0)
        self.robot_class_list_P2.append(robot_class)
        self.RobotButtonP2.setText(robot_class)
        config.read("config.txt")  # Path to config file
        config.set("Class", "selected_class_p2", robot_class)
        # Overwrite config file
        with open("config.txt", "w") as config_file:
            config.write(config_file)

    def ArenaClicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Choose Arena", "", "Text Files (*.txt)"
        )

        if file_path:
            self.ArenaButton.setText(os.path.basename(file_path))
            config.read("config.txt")  # Path to config file
            config.set("Map", "selected_map", file_path)
            # Overwrite config file
            with open("config.txt", "w") as config_file:
                config.write(config_file)

    def BackClicked(self):
        self.setCentralWidget(PlayMenu())


class MusicPlayer:
    def __init__(self):
        self.media_player = QMediaPlayer()
        self.tracks = [0, 1]
        self.tracks[0] = QMediaContent(
            QUrl.fromLocalFile("Sounds\\nicebassiguess.mp3")
        )
        self.tracks[1] = QMediaContent(QUrl.fromLocalFile("Sounds\\DRIVE.mp3"))

        # Get Volume from config file
        config = configparser.ConfigParser()
        config.read("config.txt")  # Path to config file
        self.music = config.getint("Settings", "music")
        self.current_track = config.get("Settings", "soundtrack")

        # Adjust volume
        self.media_player.setVolume(self.music)
        self.media_player.mediaStatusChanged.connect(self.restart_playback)

        # Create a QTimer to update the volume regularly
        self.music_timer = QTimer()
        self.music_timer.timeout.connect(self.update_music)
        self.music_timer.timeout.connect(self.change_track)
        self.music_timer.start(500)

    def restart_playback(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

    def update_music(self):
        # Get Volume from config file
        config.read("config.txt")  # Path to config file
        self.music = config.getint("Settings", "music")

        # Adjust volume
        self.media_player.setVolume(self.music)

    def change_track(self):
        config.read("config.txt")  # Path to config file
        soundtrack = config.get("Settings", "soundtrack")
        soundtrack = str(soundtrack)
        if self.current_track != soundtrack:
            self.current_track = soundtrack
            self.media_player.stop()
            self.media_player.setMedia(
                QMediaContent(QUrl.fromLocalFile(self.current_track))
            )
            self.media_player.play()

    def stop(self):
        self.media_player.stop()

    def play(self, index):
        self.media_player.stop()
        self.media_player.setMedia(self.tracks[index])
        self.media_player.play()


if __name__ == "__main__":
    flag = 1
    # Set correct Menu Window
    config.read("config.txt")
    config.set("Settings", "soundtrack", "Sounds\\nicebassiguess.mp3")
    with open("config.txt", "w") as config_file:
        config.write(config_file)

    # Create the QApplication instance in the main thread
    app = QApplication(sys.argv)

    music_player = MusicPlayer()
    music_player.play(0)
    # Continue with the main program execution
    window = MainMenu()
    window.move(config.getint("Position", "x"), config.getint("Position", "y"))
    window.show()
    window.setFocus()

    sys.exit(app.exec_())
