from __future__ import annotations
from typing import Callable
from gameobject import GameObject
from gameobject import Food
import random
import math
import time

if __name__ == "__main__":
    import main
    exit()

class Entity(GameObject):

    perceiveCallback: Callable[[Entity], list[list[GameObject]]]
    moveCallback: Callable[[Entity, tuple[int, int]], None]
    attackCallback: Callable[[Entity, Entity], None]

    maxPerception:int = 5
    maxTileMovement:int = 3
    
    def __init__(self, speed:float, stamina:float, perception:float, strength:float, toughness:float, lifespan:float, energy:float) -> None:
        self.speed: float = speed
        self.stamina: float = stamina
        self.perception: float = perception # used by world to figure out the return function
        self.strength: float = strength
        self.toughness: float = toughness
        self.lifespan: float = lifespan
        self.energy: float = energy#main balancing factor of sim, start off with full energy

    def rand(self):
        self.speed += (random.randrange(-10, 10, 1) / 100)
        self.stamina += (random.randrange(-10, 10, 1) / 100)
        self.perception += (random.randrange(-10, 10, 1) / 100)
        self.strength += (random.randrange(-10, 10, 1) / 100)
        self.toughness += (random.randrange(-10, 10, 1) / 100)
        self.lifespan += (random.randrange(-10, 10, 1) / 100)
        
    def think(self):
        observableWorld:list[list[GameObject]] = Entity.perceiveCallback(self)
        
        #look for things nearby
        entities:dict[Entity, tuple[int,int]] = dict()
        foods:dict[Food, tuple[int,int]] = {}
        gameObjects:dict[GameObject, tuple[int,int]] = dict()
        obsWrldWidth:int = len(observableWorld)
        obsWrldHeight:int = len(observableWorld[0])
        cx = round(obsWrldWidth / 2)
        cy = round(obsWrldHeight / 2)
        
        rawPerception:int = round(self.perception*self.maxPerception)
        
        #find nearby things [..., self, ....(
        for i in range(0,obsWrldWidth):
            for j in range(0,obsWrldHeight):
                if i < 0 or i >= obsWrldWidth or j < 0 or j >= obsWrldHeight: # bounds checking
                    continue
                tmp = observableWorld[i][j]
                if isinstance(tmp, Entity):
                    entities[tmp] = (i - cx, j - cy)
                    gameObjects.update({tmp:(i,j)})
                elif isinstance(tmp, Food):
                    foods[tmp] = (i - cx, j - cy)
                    gameObjects.update({tmp:(i,j)})
                else:
                    pass #don't care abt empty spaces
             
        #Decide which of the following scenarios are happening
            #first priority is surviving so if you see something with strength greater than your toughness run
            #second priority is eating things with a lower toughness, than your strength
            #third priority is eating food scattered around the world
            #lastly if you don't see anything move around randomly
            
        run:bool = False
        chase:bool = False
        gettingFood:bool = False
        movingRandomly:bool = True #default action
        
        # for entity in entities:
        #     if entity.strength > self.toughness: #run away
        #         run = True
        #         chase = False
        #         gettingFood = False
        #         movingRandomly = False
        #         break #don't need to check anymore if running
        #     elif entity.toughness < self.strength and not run:
        #         chase = True 
        #         gettingFood = False
        #         movingRandomly = False
             
        if not run and not chase:  
            if len(foods) > 0: #entity can see food
                gettingFood = True
                movingRandomly = False
                    
        if not run and not chase and not gettingFood: #redundant check 
            movingRandomly = True     
        
        moveX:int = 0
        moveY:int = 0
        #do actions based on what was decided
        if run:
            hostileEntities: int = 0
            
            for entity in entities:
                if entity.strength > self.toughness:
                    moveX = moveX - entities[entity][0] #negative because moving away
                    moveY = moveY - entities[entity][1] #negative because moving away
                    hostileEntities = hostileEntities + 1
            
            moveXavg = moveX/hostileEntities #hostilesentitites should never be 0
            moveYavg = moveY/hostileEntities #hostilesentitites should never be 0
                        
            if(moveXavg == 0):
                normalizedX = 0
            else:
                normalizedX = moveXavg/abs(moveXavg) #use abs to prevent -*-=+
                
            if(moveYavg == 0):
                normalizedY = 0
            else:
                normalizedY = moveYavg/abs(moveYavg) #use abs to prevent -*-=+
            
            discretizedNormalizedX = round(normalizedX)
            discretizedNormalizedY = round(normalizedY)
            
            Entity.moveCallback(self, (discretizedNormalizedX, discretizedNormalizedY))    

        elif chase:
            # find closes entity
            closestEntity:Entity | None = None
            for entity in entities:
                if closestEntity is None or (abs(entities[entity][0]) + abs(entities[entity][1])) / 2 < (abs(entities[closestEntity][0]) + abs(entities[closestEntity][1])) / 2:
                    closestEntity = entity
            
            #if in the 8 adjecent tiles then attack
            if closestEntity is not None and entities[closestEntity][0] <= 1 and entities[closestEntity][0] >= -1 and entities[closestEntity][1] <= 1 and entities[closestEntity][1] >= -1:
                self.attack(self, closestEntity)
            
            #move toward stuff
            if closestEntity is not None: #should always be the case
                if(entities[closestEntity][0] == 0):
                    moveX = 0
                else:
                    moveX = round(entities[closestEntity][0]/abs(entities[closestEntity][0])) #use abs to prevent -*-=+
                
                if(entities[closestEntity][1] == 0):
                    moveY = 0
                else:
                    moveY = round(entities[closestEntity][1]/abs(entities[closestEntity][1])) #use abs to prevent -*-=+
                    
            Entity.moveCallback(self, (moveX, moveY))
                            
        elif gettingFood:
            # find closes entity
            closestFood:Food | None = None
            for food in foods:
                if closestFood is None or (abs(foods[food][0]) + abs(foods[food][1])) / 2 < (abs(foods[closestFood][0]) + abs(foods[closestFood][1])) / 2:
                    closestFood = food
                                
            #move toward stuff
            if closestFood is not None: #should always be the case
                if(foods[closestFood][0] == 0):
                    moveX = 0
                else:
                    if foods[closestFood][0] < 0:
                        moveX = -1
                    else:
                        moveX = 1
                
                if(foods[closestFood][1] == 0):
                    moveY = 0
                else:
                    if foods[closestFood][1] < 0:
                        moveY = -1
                    else:
                        moveY = 1

            Entity.moveCallback(self, (moveX, moveY))
            return
                
            
        else: #moves randomly
            direction: int = random.randint(1, 8)
            if(direction == 1):
                #move north
                Entity.moveCallback(self, (0, 1))
            elif(direction == 2):
                #move northeast
                Entity.moveCallback(self, (1, 1))
            elif(direction == 3):
                #move east
                Entity.moveCallback(self, (1, 0))
            elif(direction == 4):
                #move southeast
                Entity.moveCallback(self, (1, -1))
            elif(direction == 5):
                #move south
                Entity.moveCallback(self, (0, -1))
            elif(direction == 6):
                #move southwest
                Entity.moveCallback(self, (-1, -1))
            elif(direction == 7):
                #move west
                Entity.moveCallback(self, (-1, 0))
            elif(direction == 8):
                #move northwest
                Entity.moveCallback(self, (-1, 1))
            else:
                #should never reach
                return