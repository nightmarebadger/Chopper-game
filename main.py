import pygame, sys
from random import randint
from pygame.locals import *
from colors import *  
    
def terminate():
    pygame.quit()
    sys.exit()

def normalFont(size, font_name = "menu_font"):
    """
    if(font_debug):
        print("------------")
        print(size)
        print(pygame.font.Font("fonts/{0}.ttf".format(font_name), size).get_height())
        print(pygame.font.SysFont(None, size).get_height())
        print(pygame.font.Font("fonts/{0}.ttf".format(font_name), int(size * 0.54)).get_height())
    """
    #try:
        #print("Ratalo")
    return pygame.font.Font("fonts/{0}.ttf".format(font_name), int(size * 0.54))
    #except:
    #    print("Ni")
    #    #print(errno, strerror)
    #    return pygame.font.Font(None, size)

def drawText(text, font, surface, x, y, color, option="center"):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if(option == "center"):
        textrect.center = (x, y)
    elif(option == "left"):
        textrect.left = x
        textrect.centery = y
    elif(option == "right"):
        textrect.right = x
        textrect.centery = y
    else:
        textrect.center = (x, y)
    surface.blit(textobj, textrect)
    return textrect


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
        self.vy = 0
        #self.vx = -speed
        self.movex = self.movey = 0
        
        self.color()
        
    def color(self):
        self.image.fill(GREEN)
        
    def update(self, time):
        self.vx = -self.game.speed
        self.move(self.vx*time, self.vy*time)
    
    def move(self, dx, dy):
        self.movex += dx
        self.movey += dy
        x = int(self.movex)
        y = int(self.movey)
        
        self.rect.x += x
        if(self.rect.right < 0):
            #print("Ubijam")
            self.kill()
        
        self.movex -= x
        self.movey -= y

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, speed=50, jumping = False):
        pygame.sprite.Sprite.__init__(self)
        
        self.game = game
        self.speed = speed
        
        self.image = pygame.Surface((width, height))
        
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x,y)
        
        self.color()
        
        self.vx = self.vy = 0
        self.movex = self.movey = 0
        
        self.jumping = jumping
        #self.jumptimerbase = 1
        #self.jumptimer = 0
        self.holdingJump = False
        
        self.keyJump = (MOUSEBUTTONDOWN, 1)
        self.keyJumpStop = (MOUSEBUTTONUP, 1)
        
        
        
    def color(self):
        self.image.fill(RED)
        
    def update(self, time):
        self.calculateMove(time)
        self.move(0, self.vy*time)
        for block in self.game.blockGroup:
            if(self.rect.colliderect(block.rect)):
                self.game.gameOver()
        #print(self.vy)
        
    def calculateMove(self, time):
        self.vx = self.speed
        #if(self.jumping):
        #    self.vy = - self.game.gravity
        #else:
        self.vy += self.game.gravity*time
        if(self.holdingJump):
            self.vy -= 2*self.game.gravity*time
            
    def move(self, dx, dy):
        self.movex += dx
        self.movey += dy
        x = int(self.movex)
        y = int(self.movey)
        
        if(self.rect.bottom + y > self.game.checkheight):
            self.rect.bottom = self.game.checkheight
            self.game.gameOver()
        elif(self.rect.top + y < 100):
            self.game.gameOver()
            
        else:
            self.rect.y += y
        
        self.rect.x += x
        
        self.movex -= x
        self.movey -= y
        
    def keyPress(self, button):
        #t = type
        #b = button
        if(button == self.keyJump):
            #self.jump()
            self.startJump()
        elif(button == self.keyJumpStop):
            self.stopJump()
    
    def startJump(self):
        self.holdingJump = True
    
    def stopJump(self):
        self.holdingJump = False
        
    def jump(self):
        if(not self.jumping):
            self.jumping = True
            self.vy -= 2*self.game.gravity
        
        
        
class Game:
    def __init__(self, windowwidth, windowheight, gravity = 500, fps=120, checkwidth = None, checkheight = None):
        
        self.windowwidth = windowwidth
        self.windowheight = windowheight
        self.checkwidth = checkwidth
        self.checkheight = checkheight
        
        
        if(not checkwidth):
            self.checkwidth = windowwidth
        if(not checkheight):
            self.checkheight = checkheight
        self.fps = fps
        self.gravity = gravity
        
        self.backgroundcolor = BLACK
        self.floorcolor = GREEN
        self.background = pygame.Surface((self.windowwidth, self.windowheight))
        self.background.fill(self.backgroundcolor)
        self.background.fill(self.floorcolor, rect=(0,0,self.windowwidth, 100))
        self.background.fill(self.floorcolor, rect=(0, self.checkheight, self.windowwidth, self.windowheight - self.checkheight))
        
        self.caption = "Runner"
        
        self.speed = 100
        self.timer = 0
        self.makeBlock = True
        
        self.timesincestart = 0
        self.score = 0
        #self.scoreadd = 0
        
    def setup(self):
        pygame.init()
        #pygame.font.init()
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((self.windowwidth, self.windowheight), SRCALPHA, 32)
        
        #Sprite groups
        self.playerGroup = pygame.sprite.RenderPlain()
        self.blockGroup = pygame.sprite.RenderPlain()
        
        
        self.playerGroup.add(Player(self,100,300,50,50, jumping=True))
        
        
    def addBlock(self):
        width = randint(80,200)
        height = randint(10,50)
        self.blockGroup.add(Block(self, self.windowwidth + width, randint(105 + height,695 - height), width, height))
        #self.blockGroup.add(Block(self, 400,400,100,100))
        
    def gameloop(self):
        self.continue_playing = True
        self.clock.tick()
        while(self.continue_playing):
            time = self.clock.tick(self.fps)
            self.timer += time/1000
            self.timesincestart += time/1000
            self.score += self.speed*time/1000
            #self.scoreadd += self.speed*time/1000
            #self.score += (self.scoreadd//100) * 100
            #self.scoreadd -= (self.scoreadd//100) * 100
            #self.scoreadd > 10):
            #    self.score += 10
            if(self.timer >= (1/(self.speed/100)*2)):
                self.timer = 0
                self.speed += 5
                if(self.makeBlock):
                    self.addBlock()
                    self.makeBlock = False
                else:
                    self.makeBlock = True
                #print(self.speed)
            #print(self.lattice)
            #print(self.clock.get_fps())
            
            #Key handler
            for event in pygame.event.get():
                if(event.type == QUIT):
                    terminate()
                elif(event.type == KEYDOWN):
                    if(event.key == K_ESCAPE):
                        terminate()
                elif(event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP):
                    for player in self.playerGroup:
                        player.keyPress((event.type, event.button))
                    """
                        1: levi
                        2: srednji
                        3: desni
                        4: kolešček gor
                        5: kolešček dol
                        8: stranski
                    """
               
            #Update groups
            self.playerGroup.update(time/1000)
            self.blockGroup.update(time/1000)
            
            
            #Drawing
            self.surface.blit(self.background, (0,0))
            
            self.playerGroup.draw(self.surface)
            self.blockGroup.draw(self.surface)
            drawText("FPS: {0}".format(round(self.clock.get_fps(), 0)), normalFont(50), self.surface, 50, 750, BLACK, option = "left")
            drawText("Speed: {0}".format(self.speed), normalFont(50), self.surface, self.windowwidth - 50, 750, BLACK, option = "right")
            drawText("Time: {0}".format(round(self.timesincestart, 1)), normalFont(50), self.surface, 50, 50, BLACK, option = "left")
            #drawText("Score:".format(round(self.score, 0)), normalFont(50), self.surface, self.windowwidth - 150, 50, BLACK, option = "right")
            drawText("Score: {0}".format(round(self.score)), normalFont(50), self.surface, self.windowwidth - 50, 50, BLACK, option = "right")
            
            pygame.display.update()
    
    def gameOver(self):
        terminate()


if( __name__ == "__main__") :
    game = Game(800, 800, fps=240, checkheight = 700)
    game.setup()
    game.gameloop()
"""
with open("test.txt", 'w') as f:
    f.write("Blabla")
with open("fonts/menu_font.ttf") as f:
    print(f.read())
"""
