from gameobject import GameObject

class Entity(GameObject):
    def __init__(self, speed:float, stamina:float, perception:float, strength:float, toughness:float, lifespan:float, energy:float, perceive:function) -> None:
        self.speed: float = speed
        self.stamina: float = stamina
        self.perception: float = perception # used by world to figure out the return function
        self.strength: float = strength
        self.toughness: float = toughness
        self.lifespan: float = lifespan
        self.energy: float = energy#main balancing factor of sim, start off with full energy
        self.perceive:function = perceive
        
    def getPos(self):
        return super().getPos()
        
    def think(self):
        observableWorld:list[list[GameObject]] = self.perceive()
        
        
        
