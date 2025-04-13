from typing import Callable, Union
from gameobject import GameObject
from gameobject import Food
from entity import Entity
import random

DEFAULTWIDTH = 25
DEFAULTHEIGHT = 25

class World:

    ENERGY_LOST: int = 10
    FOOD_ENERGY: int = 10

    def __init__(self, width=DEFAULTWIDTH, height=DEFAULTHEIGHT) -> None:
        self.worldMap: list[list[Union[GameObject, None]]] = []
        self.gameObjects: dict[GameObject, tuple[int, int]]
        self.width: int = width
        self.height: int = height
        self.foodGrowthRate: float
        self.foodQuality: int
        self.geneRandomness: float

        for i in range(width):
            self.worldMap.append([None] * height)

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
    
    def makeEntity(self, speed: float, stamina: float, perception: float, strength: float, toughness: float, lifespan: float, energy: float, percieve: Callable[[], list[list[GameObject]]]) -> Entity:
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
            self.worldMap[self.gameObjects[defender][0]][self.gameObjects[defender][1]]
            if(attacker.energy <= 0):
                del self.gameObjects[defender]
                self.worldMap[self.gameObjects[attacker][0]][self.gameObjects[attacker][1]]
                return
            else:
                return
        else:
            attacker.energy -= attacker.strength * World.ENERGY_LOST
            if(attacker.energy <= 0):
                del self.gameObjects[defender]
                self.worldMap[self.gameObjects[attacker][0]][self.gameObjects[attacker][1]]
                return
            else:
                return
    
    def handleMove(self, ent: Entity, pos: tuple[int, int]) -> None:
        # For consuming food
        if(self.worldMap[self.gameObjects[ent][0]][self.gameObjects[ent][1]] is Food):
            self.worldMap[self.gameObjects[ent][0]][self.gameObjects[ent][1]] = None
            ent.energy += World.FOOD_ENERGY
        # Move entity
        if(self.worldMap[self.gameObjects[ent][0]][self.gameObjects[ent][1]] == None):
            self.gameObjects[ent] = (self.gameObjects[ent][0] + pos[0], self.gameObjects[ent][1] + pos[1])
            self.worldMap[self.gameObjects[ent][0]][self.gameObjects[ent][1]] = ent
        else:
            objAtLocation = self.worldMap[self.gameObjects[ent][0] + pos[0]][self.gameObjects[ent][1] + pos[1]]
            if(isinstance(objAtLocation, Entity)):    
                self.handleAttack(ent, objAtLocation)
                return
            else:
                #???
                return