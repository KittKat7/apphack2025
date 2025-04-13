from gameobject import GameObject
from gameobject import Food
from entity import Entity

class World:

    self.worldMap: list[list[GameObject]]

    def __init__(self, ) -> None:
        self.gameObjects: dict[Entity, tuple(int, int)]
        self.width: int
        self.height: int
        self.foodGrowthRate: float
        self.foodQuality: int
        self.geneRandomness: float

    def getWidth(self) -> int:
        return self.width

    def getHeight(self) -> int:
        return self.height
    
    def getFoodGrowthRate(self) -> float:
        return self.foodGrowthRate
    
    def getFoodQuality(self) -> int:
        return self.foodQuality
    
    def getGeneRandomness(self) -> float:
        return self.geneRandomness
    
    def makeEntity(speed: float, stamina: float, perception: float, strength: float, toughness: float, lifespan: float, energy: float) -> Entity:
        return Entity()
    
    def makeFood() -> Food:
        return Food()
