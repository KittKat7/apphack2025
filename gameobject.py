import game as Game
class GameObject:
    """
    """ 
    def __init__(self, type:str, x:int=None, y:int=None)->None:
        self:GameObject = self
        self.type:str = type
        self.x:int = x
        self.y:int = y
    
    def getPos(self)->tuple[int, int]:
        x, y = Game.getGameObjectPos(self)
        self.x = x
        self.y = y
        return (x,y)        

class Food(GameObject):
    """
    """