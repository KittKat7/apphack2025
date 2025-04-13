from gameobject import GameObject
from gameobject import Food
from entity import Entity
import random

class World:

    worldMap: list[list[GameObject]]
    ENERGY_LOST: 10

    def __init__(self, ) -> None:
        self.gameObjects: dict[GameObject, tuple[int, int]]
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
    
    def setFoodGrowthRate(self, val: float) -> None:
        self.foodGrowthRate = val
        
    def setFoodQuality(self, val: float) -> None:
        self.foodQuality = val
        
    def setGeneRandomness(self, val: float) -> None:
        self.geneRandomness = val
    
    def makeEntity(speed: float, stamina: float, perception: float, strength: float, toughness: float, lifespan: float, energy: float) -> Entity:
        return Entity()
    
    def makeFood() -> Food:
        return Food()

    def getGameObjectPos(self, obj: GameObject) -> tuple[int, int]:
        return self.gameObjects.get(obj)
    
    def handleAttack(self, attacker: Entity, defender: Entity) -> None:
        totalStats: float = attacker.strength + defender.toughness
        survivability: float = defender.toughness / totalStats
        if((random.random() * 100) > survivability):
            attacker.energy -= attacker.strength * World.ENERGY_LOST
            attacker.energy += defender.energy
            self.gameObjects.remove(defender)
            World.worldMap.remove(defender)
            if(attacker.energy <= 0):
                self.gameObjects.remove(attacker)
                World.worldMap.remove(attacker)
                return
            else:
                return
        else:
            attacker.energy -= attacker.strength * World.ENERGY_LOST
            if(attacker.energy <= 0):
                self.gameObjects.remove(attacker)
                World.worldMap.remove(attacker)
                return
            else:
                return
    """
    def handleMove(self, ent: Entity, pos: tuple[int, int]) -> None:
        if(World.worldMap[self.gameObjects.get(ent).][]
        self.gameObjects.insert(ent, pos)
        World.worldMap.insert(ent, pos)
    """    