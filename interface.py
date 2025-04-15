if __name__ == "__main__":
    import main
    exit()

import contextlib
with contextlib.redirect_stdout(None):
    try:
        import pygame as pg
    except:
        print("ERR: PyGame is not installed!!!")
        quit()
import threading

from gameobject import Food, GameObject
import gameobject
from widgets import *
from world import World

WIDTH = 360
HEIGHT = 480
FPS = 30

# Define Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Display:
    def __init__(self) -> None:
        """
        """
        pg.init()
        pg.font.init()
        Widget.setFont(pg.font.Font("./assets/game-paused-demo/Game Paused DEMO.otf", 50))
        self.pgscreen: pg.Surface = pg.display.set_mode((0, 0), pg.RESIZABLE)
        pg.display.set_caption("EVO SIM")
        self.clock: pg.Clock = pg.time.Clock() # type: ignore
        self.screen = MenuScreen(self)
        

    def run(self):
        """
        """
        self.clock.tick(60)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.close()
                else:
                    self.screen.event(event)
                

            w, h = pg.display.get_surface().get_size()
            scalew = w / 1280
            scaleh = h / 720
            if scalew <= scaleh:
                self.scale = scalew
            else:
                self.scale = scaleh
            self.pgscreen.fill('#00AA77')
            self.screen.render(self.pgscreen, self.scale)
            pg.display.flip()
            pg.display.update()

    def setScreen(self, screen) -> None:
        self.screen = screen

    def close(self):
        if hasattr(World, 'activeWorld'):
            World.activeWorld.running = False
            World.activeWorld.worldThread.join()
        pg.quit()
        print("Exiting...")
        quit()


        
class Screen:
    def __init__(self, display: Display) -> None:
        """
        """
        self.display: Display = display
        self.widgets = list[Widget]

    @abstractmethod
    def render(self, screen, scale):
        pass

    @abstractmethod
    def event(self, event):
        pass
    

class MenuScreen(Screen):
    def __init__(self, display: Display) -> None:
        """
        """
        self.titleText = Text(0, 0, 0, 0, None, "EVO SIM")
        self.startButton = Button(0, 0, 500, 100, self.startGame, buttonText="START")
        self.quitButton = Button(0, 0, 500, 100, display.close, buttonText="QUIT")
        self.widgets = [self.titleText, self.startButton, self.quitButton]
        self.display = display
    
    def render(self, screen, scale):
        w, h = pg.display.get_surface().get_size()
        self.titleText.x = int(w / 2 - self.titleText.width / 2)
        self.titleText.y = int(h / 8 * (8-6) - self.titleText.height / 2)
        self.titleText.render(screen, scale * 3)
        self.startButton.x = int(w / 2 - self.startButton.width / 2)
        self.startButton.y = int(h / 8 * (8-4) - self.startButton.height / 2)
        self.startButton.render(screen, scale)
        self.quitButton.x = int(w / 2 - self.quitButton.width / 2)
        self.quitButton.y = int(h / 8 * (8-2) - self.quitButton.height / 2)
        self.quitButton.render(screen, scale)

    def event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse = pg.mouse.get_pos()
            for w in self.widgets:
                w.event(event)
    
    def startGame(self):
        world: World = World()
        self.display.setScreen(SimScreen(self.display, world))
        t = threading.Thread(target=world.run)
        World.activeWorld.worldThread = t
        t.start()

class SimSettingScreen(Screen):
    # TODO
    pass

class SimScreen(Screen):
    def __init__(self, display: Display, world: World) -> None:
        self.world: World = world
        self.worldW: int = world.getWidth()
        self.worldH: int = world.getHeight()

    def render(self, screen, scale):
        w, h = pg.display.get_surface().get_size()
        scalew: float = (w * 0.8) / self.worldW
        scaleh: float = h / self.worldH
        scaleTile: float = scalew
        if scaleh < scalew:
            scaleTile = scaleh
        
        drawW = scaleTile * self.worldW
        drawH = scaleTile * self.worldH

        startx = (w * 0.8) / 2 - drawW / 2
        starty = h / 2 - drawW / 2

        screen.fill('#000000')

        pg.draw.rect(screen, '#333333', [startx, starty, drawW, drawH])
        for i in range(self.worldW):
            for j in range(self.worldH):
                # pg.draw.rect(screen, '#333333', [
                #     i * scaleTile + startx,
                #     j * scaleTile + starty,
                #     scaleTile,
                #     scaleTile])
                pg.draw.rect(screen, '#007744', [
                    i * scaleTile + 1 * scale + startx,
                    j * scaleTile + 1 * scale + starty,
                    scaleTile - 2 * scale,
                    scaleTile - 2 * scale])
            
                gobject: GameObject | None = self.world.worldMap[i][j]
                if isinstance(gobject, GameObject):
                    if isinstance(gobject, Food):
                        fobject: Food = gobject
                        f = FoodWidget(int(i * scaleTile + startx), int(j * scaleTile + starty), int(scaleTile), int(scaleTile), fobject.type)
                        f.render(screen, 1)
                    elif isinstance(self.world.worldMap[i][j], Entity):
                        e = EntityWidget(int(i * scaleTile + startx), int(j * scaleTile + starty), int(scaleTile), int(scaleTile), self.world.worldMap[i][j]) # type: ignore
                        e.render(screen, 1)


        pg.draw.rect(screen, '#777777', [w - w * 0.20, starty, w * 0.20, drawH])


