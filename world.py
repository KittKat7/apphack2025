from gameobject import GameObject
from entity import Entity

class World:
    def __init__(self) -> None:
        self.worldMap: list[list[GameObject]]
        self.gameObjects: dict[Entity, tuple(int, int)]
        self.foodGrowthRate: float
        self.foodQuality: int
        self.geneRandomness: float
