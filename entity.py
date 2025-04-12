from gameobject import GameObject

class Entity(GameObject):
    def __init__(self) -> None:
        speed: float
        stamina: float
        perception: float
        strength: float
        toughness: float
        lifespan: float
