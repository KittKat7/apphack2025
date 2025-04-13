from gameobject import GameObject
from gameobject import Food

class Entity(GameObject):
    maxPerception:int = 5
    
    def __init__(self, speed:float, stamina:float, perception:float, strength:float, toughness:float, lifespan:float, energy:float, perceive, attack, move) -> None:
        self.speed: float = speed
        self.stamina: float = stamina
        self.perception: float = perception # used by world to figure out the return function
        self.strength: float = strength
        self.toughness: float = toughness
        self.lifespan: float = lifespan
        self.energy: float = energy#main balancing factor of sim, start off with full energy
        self.perceive = perceive
        self.attack = attack
        self.move = move
        
    def think(self):
        observableWorld:list[list[GameObject]] = self.perceive()
        
        #look for things nearby
        entities:dict[Entity, tuple[int,int]] = dict()
        foods:dict[Food, tuple[int,int]] = dict()
        gameObjects:dict[GameObject, tuple[int,int]] = dict()
        obsWrldHeight:int = len(observableWorld)
        obsWrldWidth:int = len(observableWorld[0])
        
        rawPerception:int = round(self.perception*self.maxPerception)
        
        #find nearby things [..., self, ....]
        for i in range(0,rawPerception+1+rawPerception):
            for j in range(0,rawPerception+1+rawPerception):
                if(i < 0 or i >= obsWrldHeight or j < 0 or j >= obsWrldWidth): # bounds checking
                    continue
                tmp = observableWorld[i][j]
                if isinstance(tmp, Entity):
                    entities.update({tmp:(i,j)})
                    gameObjects.update({tmp:(i,j)})
                elif isinstance(tmp, Food):
                    foods.update({tmp:(i,j)})
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
        
        for entity in entities:
            if entity.strength > self.toughness: #run away
                run = True
                chase = False
                gettingFood = False
                movingRandomly = False
                break #don't need to check anymore if running
            elif entity.toughness <= self.strength and not run:
                chase = True 
                gettingFood = False
                movingRandomly = False
             
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
            
            moveXavg = round(moveX/hostileEntities)
            moveYavg = round(moveY/hostileEntities)
            
            self.move(self, (moveXavg, moveYavg))    

        elif chase:
            # find closes entity
            closestEntity:Entity
            for entity in entities:
                # if entity is None or 
                pass
        elif gettingFood:
            pass #TODO
        else: #moves randomly
            pass #TODO