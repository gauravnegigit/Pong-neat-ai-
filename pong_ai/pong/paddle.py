import pygame 

class Paddle :
    VEL = 4
    WIDTH = 20 
    HEIGHT = 100 

    def __init__(self , x , y):
        self.x = self.original_x = x
        self.y = self.original_y = y 

    def draw(self , win , color):
        pygame.draw.rect(win , color , (self.x , self.y , self.WIDTH , self.HEIGHT))
    
    def move(self , up = True):
        if up :
            self.y -= self.VEL 
        else :
            self.y += self.VEL 

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y 