from dataclasses import dataclass, field
import random


@dataclass
class BaseStats:
    entity: str
    level: int
    curr_health: int
    max_health: int
    attack: int
    defense: int
    curr_xp: int
    max_xp: int
    health_percent: float = field(init=False)

    def __post_init__(self):
        self.health_percent = (self.curr_health / self.max_health) * 100


@dataclass
class Player(BaseStats):
    name: str

    def raw(self) -> dict:
        raw_data: dict = {
            "entity": "Player", "name": self.name, "level": self.level, "current_health": self.curr_health,
            "max_health": self.max_health,
            "attack": self.attack, "defense": self.defense, "current_xp": self.curr_xp, "max_xp": self.max_xp,
            "health_percentage": self.health_percent
        }
        return raw_data


@dataclass
class PlayerData:
    curr_pos: int

    def raw(self) -> dict:
        raw_data: dict = {
            "curr_pos": self.curr_pos
        }
        return raw_data


@dataclass
class Mob:
    entity: str
    name: str
    level: int
    xp: int
    health: int
    attack: int
    defense: int


class Spider(Mob):
    def __init__(self, entity=None, name=None, level=None, xp=None, health=None, attack=None, defense=None):
        super().__init__(entity, name, level, xp, health, attack, defense)
        self.entity = "Mob"
        self.name = "🕷 Spider"
        self.level = level
        self.xp = random.choice([130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140])
        self.health = health
        self.attack = attack
        self.defense = defense

    def raw(self) -> dict:
        self.level = random.randrange(1, 101)
        if self.level >= 11:
            self.attack = random.randrange(self.level - 11, self.level + 11)
            self.defense = random.randrange(self.level - 11, self.level + 11)
        else:
            self.attack = random.randrange(0, self.level + 11)
            self.defense = random.randrange(0, self.level + 11)
        raw_data: dict = {
            "entity": self.entity, "name": self.name, "level": self.level, "health": self.level + 100,
            "attack": self.attack, "defense": self.defense, "xp": self.xp
        }
        return raw_data
