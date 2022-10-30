from enum import Enum


class Terrain(Enum):
    PLAIN = 1
    RAINFOREST = 2
    SNOW = 3
    DESERT = 4


map_one = {
    "name": "New Rocknesse",
    "location": "36",
    "is_positive": True,
    "is_negative": False,
    "terrain": Terrain.PLAIN,
    "map": "pixel map file"
}
