from gameobject import GameObject
from gameobject import Food

maxPerception:int = 5
class Entity(GameObject):
    
    def __init__(self, speed:float, stamina:float, perception:float, strength:float, toughness:float, lifespan:float, energy:float, perceive) -> None:
        self.speed: float = speed
        self.stamina: float = stamina
        self.perception: float = perception # used by world to figure out the return function
        self.strength: float = strength
        self.toughness: float = toughness
        self.lifespan: float = lifespan
        self.energy: float = energy#main balancing factor of sim, start off with full energy
        self.perceive = perceive
        
    def think(self):
        observableWorld:list[list[GameObject]] = self.perceive()
        
        #look for things nearby
        entities:dict = dict()
        foods:dict = dict()
        obsWrldHeight:int = len(observableWorld)
        obsWrldWidth:int = len(observableWorld[0])
        
        rawPerception:int = int(self.perception*maxPerception)
        
        #find nearby things [..., self, ....]
        for i in range(0,rawPerception+1+rawPerception):
            for j in range(0,rawPerception+1+rawPerception):
                if(i < 0 or i >= obsWrldHeight or j < 0 or j >= obsWrldWidth): # bounds checking
                    continue
                tmp = observableWorld[i][j]
                if isinstance(tmp, Entity):
                    entities.update({tmp:(i,j)})
                elif isinstance(tmp, Food):
                    foods.update({tmp:(i,j)})
                else:
                    pass #don't care abt empty spaces
            
        #first priority is surviving so if you see something with strength greater than your toughness run
        #second priority is getting food, if you see food or 
        
        
        
