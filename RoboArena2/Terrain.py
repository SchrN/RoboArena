class terrain:
    def __init__(self):
        self.movement
        self.solid
        self.damage
        self.type
        self.imagePath

    def getCollision(self):
        return self.solid


class water(terrain):  # inherits from the motherclass terrain
    # and gets the attributes from terrain
    movement = (
        0.5  # multiplicator how fast the robot move through this terrain
    )
    solid = 0  # if the robot can move through this terrain
    # (0=passable, 1= not passable)
    damage = 0  # how much damage the robot takes when passing through
    type = "a"
    imagePath = "TileImages/Water_tile.png"


class fire(terrain):
    movement = 1.0
    solid = 0
    damage = 5
    type = "f"
    imagePath = "TileImages/Fire_tile.png"


class spikes(terrain):
    movement = 1.0
    solid = 0
    damage = 2
    type = "s"
    imagePath = "TileImages/Spike_tile.png"


class wall(terrain):
    movement = 1.0
    solid = 1
    damage = 0
    type = "w"
    imagePath = "TileImages/Wall_tile.png"


class boost(terrain):
    movement = 2.0
    solid = 0
    damage = 0
    type = "b"
    imagePath = "TileImages/Boost_tile.png"


class normal(terrain):
    movement = 1.0
    solid = 0
    damage = 0
    type = "n"
    imagePath = "TileImages/Normal_tile.png"


class player1(terrain):
    movement = 1.0
    solid = 0
    damage = 0
    type = "n"
    imagePath = "TileImages/Normal_tile.png"


class player2(terrain):
    movement = 1.0
    solid = 0
    damage = 0
    type = "n"
    imagePath = "TileImages/Normal_tile.png"


test_tyle = water()
print(test_tyle.movement)
print(test_tyle.solid)
print(test_tyle.damage)
print(test_tyle.type)
