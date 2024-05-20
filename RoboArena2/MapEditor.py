import configparser
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QMainWindow
from PyQt5.uic import loadUi

GRID_SIZE = 20
GRID_CELL_SIZE = 50

config = configparser.ConfigParser()
config.read("config.txt")
selected_map = config.get("Map", "selected_map")
arena_size_width = config.getint("Arena", "arena_size_width")
arena_size_height = config.getint("Arena", "arena_size_height")
tile_size = config.getint("Tiles", "tile_size")
tile_amount = config.getint("Tiles", "tile_amount")


class MapEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mapeditor")

        # Load the UI file
        loadUi("MenuAssets\\MapEditor.ui", self)

        # Make the window non-resizable
        self.setFixedSize(self.size())

        # Create a 2D grid to store the drawn shapes
        self.grid = [[None] * tile_amount for _ in range(tile_amount)]

        # Initialize the grid with empty labels
        for row in range(tile_amount):
            for col in range(tile_amount):
                label = QLabel(self)
                label.setGeometry(
                    col * tile_size,
                    row * tile_size,
                    tile_size,
                    tile_size,
                )
                label.setStyleSheet(
                    "background-color: white; border: 1px solid gray;"
                )
                self.grid[row][col] = label

        # Create buttons and connect signals
        self.water_button.clicked.connect(lambda: self.set_draw_mode("water"))
        self.fire_button.clicked.connect(lambda: self.set_draw_mode("fire"))
        self.wall_button.clicked.connect(lambda: self.set_draw_mode("wall"))
        self.boost_button.clicked.connect(lambda: self.set_draw_mode("boost"))
        self.spikes_button.clicked.connect(
            lambda: self.set_draw_mode("spikes")
        )
        self.normal_button.clicked.connect(
            lambda: self.set_draw_mode(("normal"))
        )
        self.undo_button.clicked.connect(lambda: self.undo())
        self.new_button.clicked.connect(lambda: self.clear_grid())
        self.save_button.clicked.connect(lambda: self.save_to_text_file())
        self.load_button.clicked.connect(lambda: self.load())
        self.back_button.clicked.connect(lambda: self.back())

        # self.player_1_button.clicked.connect()
        # self.player_2_button.clicked.connect()

        # Initialize draw mode to None
        self.draw_mode = None

        # Array to save state of grid
        self.tile_array = [["n"] * tile_amount for _ in range(tile_amount)]

        # List of all drawn tiles
        self.tiles_drawn = []

        self.left_button_pressed = False

    def set_draw_mode(self, mode):
        self.draw_mode = mode

    def mousePressEvent(self, event):
        if self.draw_mode and event.buttons() == Qt.LeftButton:
            self.left_button_pressed = True

            row = event.y() // tile_size
            col = event.x() // tile_size

            if 0 <= row < tile_amount and 0 <= col < tile_amount:
                label = self.grid[row][col]
                image_path = ""

                if self.draw_mode == "water":
                    image_path = "TileImages\\Water_tile.png"
                    self.tile_array[row][col] = "a"
                elif self.draw_mode == "fire":
                    image_path = "TileImages\\Fire_tile.png"
                    self.tile_array[row][col] = "f"
                elif self.draw_mode == "wall":
                    image_path = "TileImages\\Wall_tile.png"
                    self.tile_array[row][col] = "w"
                elif self.draw_mode == "boost":
                    image_path = "TileImages\\Boost_tile.png"
                    self.tile_array[row][col] = "b"
                elif self.draw_mode == "spikes":
                    image_path = "TileImages\\Spike_tile.png"
                    self.tile_array[row][col] = "s"
                else:
                    image_path = "TileImages\\Normal_tile.png"
                    self.tile_array[row][col] = "n"

                pixmap = QPixmap(image_path)
                label.setPixmap(pixmap.scaled(tile_size, tile_size))

                self.tiles_drawn.append([row, col])

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.left_button_pressed = False

    def mouseMoveEvent(self, event):
        if self.left_button_pressed and self.draw_mode:
            row = event.y() // tile_size
            col = event.x() // tile_size

            if 0 <= row < tile_amount and 0 <= col < tile_amount:
                label = self.grid[row][col]
                image_path = ""

                if self.draw_mode == "water":
                    image_path = "TileImages\\Water_tile.png"
                    self.tile_array[row][col] = "a"
                elif self.draw_mode == "fire":
                    image_path = "TileImages\\Fire_tile.png"
                    self.tile_array[row][col] = "f"
                elif self.draw_mode == "wall":
                    image_path = "TileImages\\Wall_tile.png"
                    self.tile_array[row][col] = "w"
                elif self.draw_mode == "boost":
                    image_path = "TileImages\\Boost_tile.png"
                    self.tile_array[row][col] = "b"
                elif self.draw_mode == "spikes":
                    image_path = "TileImages\\Spike_tile.png"
                    self.tile_array[row][col] = "s"
                else:
                    image_path = "TileImages\\Normal_tile.png"
                    self.tile_array[row][col] = "n"

                pixmap = QPixmap(image_path)
                label.setPixmap(pixmap.scaled(tile_size, tile_size))

                self.tiles_drawn.append([row, col])

    def clear_grid(self):
        for row in range(tile_amount):
            for col in range(tile_amount):
                label = self.grid[row][col]
                label.clear()  # Remove the pixmap from the label
                label.setStyleSheet(
                    "background-color: white; border: 1px solid gray;"
                )

    def save_to_text_file(self):
        # opens dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Map", "", "Text Files (*.txt)"
        )
        if file_path:
            with open(file_path, "w") as file:
                for row in range(tile_amount):
                    for col in range(tile_amount):
                        file.write(str(self.tile_array[row][col]))

    def undo(self):
        # removes last drawn tile
        if len(self.tiles_drawn) > 0:
            pos = self.tiles_drawn.pop(-1)

            row = pos[0]
            col = pos[1]

            label = self.grid[row][col]
            label.clear()  # Remove the pixmap from the label
            label.setStyleSheet(
                "background-color: white; border: 1px solid gray;"
            )

    def back(self):
        self.close()

    def getWindowPos(self):
        window_pos = self.pos()
        return window_pos

    def load(self):
        # Opens dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Map", "", "Text Files (*.txt)"
        )

        if file_path:
            with open(file_path, "r") as file:
                content = file.read().strip()  # Read the content of the file

            # Check if the file has the expected length of 400
            expected_length = tile_amount * tile_amount
            if len(content) != expected_length:
                raise ValueError(
                    "Invalid map file. The File is expected to contain:",
                    expected_length,
                    "letters.",
                )

            # Clear the grid and tile array
            self.clear_grid()
            self.tile_array = [["n"] * tile_amount for _ in range(tile_amount)]

            # Iterate over each character in the file and update
            # the grid and tile array
            index = 0

            for letter in content:
                row, col = divmod(index, tile_amount)
                index = index + 1
                label = self.grid[row][col]
                image_path = ""

                if letter == "a":
                    image_path = "TileImages\\Water_tile.png"
                elif letter == "f":
                    image_path = "TileImages\\Fire_tile.png"
                elif letter == "w":
                    image_path = "TileImages\\Wall_tile.png"
                elif letter == "b":
                    image_path = "TileImages\\Boost_tile.png"
                elif letter == "s":
                    image_path = "TileImages\\Spike_tile.png"
                elif letter == "n":
                    image_path = "TileImages\\Normal_tile.png"
                else:
                    raise ValueError(letter, " is not a valid letter")

                pixmap = QPixmap(image_path)
                label.setPixmap(pixmap.scaled(tile_size, tile_size))
                self.tile_array[row][col] = letter
                self.tiles_drawn.append([row, col])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapEditor()
    window.show()
    sys.exit(app.exec_())
