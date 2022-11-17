import pygame
from rssi import RSSI

colors = pygame.color.THECOLORS

class Robot(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((100,100))
        self.image.fill(colors['green'])
        
        self.rect = self.image.get_rect().move(0, 0)
        self.speed = 20
        self.currentRssi = 0
        self.previousRssi = 0
        self.previousReward = 0
        self.reward = 0

        # var iables below are not being used 
        self.totalSteps = 0
        self.previousAction = 0
        self.currentAction = 0

    
    def move(self,spriteGroup):
        """_summary_
            Check to see if it goes beyong bound walls 
            otherwise move one of four possible directions
        """ 
        SCREEN_WIDTH = 1100
        SCREEN_HEIGHT = 1100   
        if self.rect.left + self.movepos[0] * self.speed < 0:
            self.rect.left = 0
        elif self.rect.right + self.movepos[0] * self.speed > SCREEN_WIDTH:
            self.rect.right = 1100
        elif self.rect.top + self.movepos[1] * self.speed < 0:
            self.rect.top = 0
        elif self.rect.bottom + self.movepos[1] * self.speed > SCREEN_HEIGHT:
            self.rect.bottom = 1100
        else:
            dx, dy = self.movepos[0] * self.speed, self.movepos[1] * self.speed
            self.rect = self.rect.move(dx, dy)
    
    def rewardSystem(self):

        # Dont stay on the edge 
        if self.rect.x ==  1000 or self.rect.y == 1000 or self.rect.x == 0 or self.rect.y == 0:
            # print("oops")
            self.reward = -5
        # found the best rssi 
        elif self.currentRssi == 0.0:
            self.reward = 100
            
        else:
            self.previousReward = self.reward
            self.reward = self.currentRssi - (self.previousRssi)
            # dont go back and forth
            if abs(self.previousReward) == abs(self.reward):
                self.reward = -5
            # give more points if it goes from low to high
            elif self.reward > 0:
                self.reward *= 1.5

            elif self.currentAction == self.previousAction:
                self.reward -= 1.5

        

    def detectRssi(self,spriteGroup):
        """_summary_
            looks to see if robot collides with rssi square
            and assigns value of rssi square to the robot
        Args:
            spriteGroup (pygame.sprite.Group()): pygame feature; list of sprites
        """        
        for sprite in spriteGroup:
            if pygame.sprite.collide_rect(self,sprite):
                self.previousRssi = self.currentRssi
                self.currentRssi = sprite.value
                self.rewardSystem()
                




