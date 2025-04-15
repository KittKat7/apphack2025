from __future__ import annotations
from threading import Thread
from typing import Callable, Union
from gameobject import GameObject
from gameobject import Food
from entity import Entity
import random
import time

DEFAULTWIDTH = 15
DEFAULTHEIGHT = 15
SIM_SPEED = 0.1

class World:

    ENERGY_LOST: int = 10
    FOOD_ENERGY: int = 7
    MAX_ENERGY: int = 30

    activeWorld: World

    def __init__(self, width=DEFAULTWIDTH, height=DEFAULTHEIGHT) -> None:
        World.activeWorld = self
        self.worldMap: list[list[Union[GameObject, None]]] = []
        self.gameObjects: dict[GameObject, tuple[int, int]] = {}
        self.width: int = width
        self.height: int = height
        self.foodGrowthRate: float = 3
        self.foodQuality: int
        self.geneRandomness: float
        self.worldThread: Thread

        Entity.perceiveCallback = self.handlePerceive
        Entity.moveCallback = self.handleMove
        Entity.attackCallback = self.handleAttack

        self.running = True
        self.paused = False

        for i in range(width):
            self.worldMap.append([None] * height)

        for i in range(int(10)):
            x = random.randrange(0, self.width, 1)
            y = random.randrange(0, self.height, 1)
            if self.worldMap[x][y] == None:
                e = Entity(random.random(), random.random(), random.random(), random.random(), random.random(), random.random(), random.random() * World.MAX_ENERGY)
                self.worldMap[x][y] = e
                self.gameObjects[e] = (x, y)
        self.genFood()


    def run(self):
        while self.running:
            if self.paused:
                time.sleep(1)
                continue
            entities = list(self.gameObjects.keys())
            if len(entities) == 0:
                self.running = False

            for e in entities: # type: ignore
                e: Entity = e
                if e.energy > World.MAX_ENERGY:
                    e.energy = World.MAX_ENERGY
                turns = 5 * e.speed
                e.energy -= 2
                for i in range(int(turns)):
                    # e.energy -= 2 * (100 - e.stamina) * (random.randrange(8, 11, 1) / 10)
                    e.think()
                    if e.energy > 25:
                        self.reproduce(e)
                        e.energy -= 20
                    time.sleep(SIM_SPEED)
                if e.energy <= 0:
                    self.worldMap[self.gameObjects[e][0]][self.gameObjects[e][1]] = Food(Food.ENTITY)
                    self.gameObjects.pop(e)
            self.genFood()

    def genFood(self):
        for i in range(int(self.foodGrowthRate)):
            x = random.randrange(0, self.width, 1)
            y = random.randrange(0, self.height, 1)
            if self.worldMap[x][y] == None:
                self.worldMap[x][y] = Food(Food.NORMAL)
            elif isinstance(self.worldMap[x][y], Entity):
                # self.worldMap[x][y].energy += World.FOOD_ENERGY # type: ignore
                continue

    def reproduce(self, entity: Entity):
        x, y = self.gameObjects[entity]
        for i in range(3):
            for j in range (3):
                try:
                    if i == 1 and j == 1:
                        continue
                    g = self.worldMap[x + i - 1][y + j - 1]
                    if g == None:
                        self.worldMap[x + i - 1][y + j -1] = Entity(entity.speed, entity.stamina, entity.perception, entity.toughness, entity.toughness, entity.lifespan, 20)
                        self.worldMap[x + i - 1][y + j -1].rand() # type: ignore
                        self.gameObjects[self.worldMap[x + i - 1][y + j - 1]] = (x + i - 1, y + j - 1) # type: ignore
                        return
                except:
                    continue


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
    
    def makeEntity(self, speed: float, stamina: float, perception: float, strength: float, toughness: float, lifespan: float, energy: float) -> Entity:
        return Entity(speed, stamina, perception, strength, toughness, lifespan, energy)
    
    def getGameObjectPos(self, obj: GameObject) -> tuple[int, int] | None:
        if(self.gameObjects.get(obj) != None):
            return self.gameObjects.get(obj)
        else:
            return None
    
    def handleAttack(self, attacker: Entity, defender: Entity) -> None:
        attacker.energy -= 5
        return
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
        ex, ey = self.gameObjects[ent]
        try:
            self.worldMap[ex + pos[0]][ey + pos[1]]
        except:
            return
        # For consuming food
        if isinstance(self.worldMap[ex + pos[0]][ey + pos[1]], Food):
            self.worldMap[ex + pos[0]][ey + pos[1]] = None
            ent.energy += World.FOOD_ENERGY
        # Move entity
        if self.worldMap[ex + pos[0]][ey + pos[1]] == None:
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
            
    def handlePerceive(self, entity: Entity) -> list[list[GameObject]]:
        x, y = self.gameObjects[entity]
        r = int(round(Entity.maxPerception * (entity.perception + 1)))

        retData: list[list[GameObject]] = []
        for i in range(-r + 1, r):
            tmp = []
            for j in range(-r + 1, r):
                if x + i < 0 or x + i >= self.width or y + j < 0 or y + j >= self.height:
                    tmp.append(None)
                else:
                    tmp.append(self.worldMap[x + i][y + j])
            retData.append(tmp)
        return retData