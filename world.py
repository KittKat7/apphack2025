from typing import Callable, Union
from gameobject import GameObject
from gameobject import Food
from entity import Entity
import random
import time

DEFAULTWIDTH = 25
DEFAULTHEIGHT = 25

class World:

    ENERGY_LOST: int = 10
    FOOD_ENERGY: int = 10

    def __init__(self, width=DEFAULTWIDTH, height=DEFAULTHEIGHT) -> None:
        self.worldMap: list[list[Union[GameObject, None]]] = []
        self.gameObjects: dict[GameObject, tuple[int, int]] = {}
        self.width: int = width
        self.height: int = height
        self.foodGrowthRate: float = 10
        self.foodQuality: int
        self.geneRandomness: float

        self.running = True

        for i in range(width):
            self.worldMap.append([None] * height)

        for i in range(int(self.foodGrowthRate)):
            x = random.randrange(0, self.width, 1)
            y = random.randrange(0, self.height, 1)
            if self.worldMap[x][y] == None:
                e = Entity(random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), self.percieve, self.handleAttack, self.handleMove)
                self.worldMap[x][y] = e
                self.gameObjects[e] = (x, y)
        self.genFood()


    def run(self):
        while self.running:
            entities = list(self.gameObjects.keys())
            if len(entities) == 0:
                self.running = False

            for e in entities: # type: ignore
                e: Entity = e
                turns = 5 * e.speed
                for i in range(int(turns)):
                    e.think()
                    time.sleep(0.1)
                if e.energy <= 0:
                    self.worldMap[self.gameObjects[e][0]][self.gameObjects[e][1]] = Food()
                    self.gameObjects.pop(e)
            self.genFood()

    def genFood(self):
        for i in range(int(self.foodGrowthRate * 10)):
            x = random.randrange(0, self.width, 1)
            y = random.randrange(0, self.height, 1)
            if self.worldMap[x][y] == None:
                self.worldMap[x][y] = Food()
            elif isinstance(self.worldMap[x][y], Entity):
                self.worldMap[x][y].energy += World.FOOD_ENERGY # type: ignore


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
    
    def makeEntity(self, speed: float, stamina: float, perception: float, strength: float, toughness: float, lifespan: float, energy: float, percieve: Callable[[], list[list[GameObject]]], attack: Callable[[Entity, Entity], None], move: Callable[[Entity, tuple[int, int]], None]) -> Entity:
        return Entity(speed, stamina, perception, strength, toughness, lifespan, energy, percieve, attack, move)
    
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
            attacker.energy += defender.energy + World.FOOD_ENERGY
            defender.energy = -1
            # self.worldMap[self.gameObjects[defender][0]][self.gameObjects[defender][1]] = None
            # del self.gameObjects[defender]
            if(attacker.energy <= 0):
                # self.worldMap[self.gameObjects[attacker][0]][self.gameObjects[attacker][1]] = None
                # del self.gameObjects[attacker]
                return
            else:
                return
        else:
            attacker.energy -= attacker.strength * World.ENERGY_LOST
            if(attacker.energy <= 0):
                # del self.gameObjects[defender]
                # self.worldMap[self.gameObjects[attacker][0]][self.gameObjects[attacker][1]]
                return
            else:
                return
    
    def handleMove(self, ent: Entity, pos: tuple[int, int]) -> None:
        # For consuming food
        ex, ey = self.gameObjects[ent]
        if(self.worldMap[ex + pos[0]][ey + pos[1]] is Food):
            self.worldMap[ex][ey] = None
            ent.energy += World.FOOD_ENERGY
        # Move entity
        if(self.worldMap[ex + pos[0]][ey + pos[1]] == None):
            self.worldMap[ex + pos[0]][ey + pos[1]] = ent
            self.worldMap[ex][ey] = None
            self.gameObjects[ent] = (ex + pos[0], ey + pos[1])
        else:
            objAtLocation = self.worldMap[ex + pos[0]][ey + pos[1]]
            if(isinstance(objAtLocation, Entity)):
                self.handleAttack(ent, objAtLocation)
                return
            else:
                #???
                return
            
    def percieve(self, entity: Entity) -> list[list[GameObject]]:
        x, y = self.gameObjects[entity]
        r = int(round(Entity.maxPerception * entity.perception)) + 1

        retData: list[list[GameObject]] = []
        for i in range(-r + 1, r):
            if x + i < 0 or x + i >= self.width:
                continue
            tmp = []
            for j in range(-r + 1, r):
                if x + i < 0 or x + i >= self.width or y + j < 0 or y + j >= self.height:
                    continue
                tmp.append(self.worldMap[x + i][y + j])
            retData.append(tmp)
        return retData