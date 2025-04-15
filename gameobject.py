class GameObject:
    """
    """ 

class Food(GameObject):
    NORMAL: int = 0
    ENTITY: int = 1

    """
    """
    def __init__(self, type: int):
        self.type: int = type