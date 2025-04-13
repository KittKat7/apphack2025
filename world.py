from gameobject import GameObject
from gameobject import Food
from entity import Entity
import random

DEFAULTWIDTH = 100
DEFAULTHEIGHT = 100

class World:

    worldMap: list[list[GameObject]]
    ENERGY_LOST: int = 10

    def __init__(self, width=DEFAULTWIDTH, height=DEFAULTHEIGHT) -> None:
        self.gameObjects: dict[GameObject, tuple[int, int]]
        self.width: int = width
        self.height: int = height
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
        
    def setFoodQuality(self, val: int) -> None:
        self.foodQuality = val
        
    def setGeneRandomness(self, val: float) -> None:
        self.geneRandomness = val
    
    def makeEntity(self, speed: float, stamina: float, perception: float, strength: float, toughness: float, lifespan: float, energy: float, percieve) -> Entity:
        return Entity(speed, stamina, perception, strength, toughness, lifespan, energy, percieve)
    
    def makeFood(self) -> Food:
        return Food()

    def getGameObjectPos(self, obj: GameObject) -> tuple[int, int] | None:
        if(self.gameObjects.get(obj) != None):
            return self.gameObjects.get(obj)
        else:
            return None
    
    def handleAttack(self, attacker: Entity, defender: Entity) -> None:
        totalStats: float = attacker.strength + defender.toughness
        survivability: float = defender.toughness / totalStats
        if((random.random() * 100) > survivability):
            attacker.energy -= attacker.strength * World.ENERGY_LOST
            attacker.energy += defender.energy
            del self.gameObjects[defender]
            World.worldMap[self.gameObjects[defender][0]][self.gameObjects[defender][1]]
            if(attacker.energy <= 0):
                del self.gameObjects[defender]
                World.worldMap[self.gameObjects[attacker][0]][self.gameObjects[attacker][1]]
                return
            else:
                return
        else:
            attacker.energy -= attacker.strength * World.ENERGY_LOST
            if(attacker.energy <= 0):
                del self.gameObjects[defender]
                World.worldMap[self.gameObjects[attacker][0]][self.gameObjects[attacker][1]]
                return
            else:
                return
    """
    def handleMove(self, ent: Entity, pos: tuple[int, int]) -> None:
        if(World.worldMap[self.gameObjects.get(ent).][]
        self.gameObjects.insert(ent, pos)
        World.worldMap.insert(ent, pos)
    """    