from gameobject import GameObject

class World:
    def __init__(self) -> None:
        worldMap: list[list[GameObject]]
        x: int 
        y: int 
        foodGrowthRate: float
        foodQuality: int
        geneRandomness: float
        