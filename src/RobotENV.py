
from rssi import RSSI
from robot import Robot
from rssiValues import rssiValues
import random
import numpy as np
# Pygame
import pygame
# openAI gym
from gym.spaces import Discrete, Box,Tuple
from gym import Env

import datetime

pygame.init()
colors = pygame.color.THECOLORS
screen = pygame.display.set_mode([1100,1100])

class RobotEnv(Env):
    def __init__(self):
        # We have 4 actions: up,down,left,right, and still
        self.action_space = Discrete(4)
        # Set start rssi
        self.state = rssiValues[0][0]
        # Set game length
        self.game_length = 10_000
        # our robot
        self.robot = Robot()
        # list like data structures that holds all sprites we can possibly collide with
        self.rssiBlockGroup = pygame.sprite.Group()
         # state format for neural network
        self.observation_space = np.array([self.state])
        self.game_done = False



    def step(self, action):
        # Apply action
        
        if action == 0:
            left, right, up, down = True, False, False, False
        if action == 1:
            left, right, up, down = False, True, False, False
        if action == 2:
            left, right, up, down = False, False, True, False
        if action == 3:
            left, right, up, down = False, False, False, True
        if self.robot.currentRssi == 0.0:
            left, right, up, down = False, False, False, False

        self.robot.movepos = -left + right, -up + down
        self.robot.reward = 0
        self.robot.move(self.rssiBlockGroup)
        self.robot.detectRssi(self.rssiBlockGroup)
        self.robot.currentAction = action

        # Reduce game length by 1 second
        self.game_length -= 1 
        
        reward = self.robot.reward
        self.state = self.robot.currentRssi
        # Check if game is done
        if self.game_length <= 0:
            self.game_done = True
        else:
            self.game_donene = False
        
        # Apply rssi noise
        # self.state += random.uniform(0.001, 0.009)

        # Set placeholder for info (this is to comply with openai gym)
        info = {}
        
        # Return step information
        return self.state, reward, self.game_done, info

    def render(self):
        # visualize game
        screen.fill(colors['white'])
    
        for rssiBlock in self.rssiBlockGroup:
            screen.blit(rssiBlock.image, rssiBlock.rect.topleft)

        screen.blit(self.robot.image, self.robot.rect.topleft)
        pygame.display.flip()
         
    def reset(self):
        x = random.randint(0,10)
        y = random.randint(0,10)
        previousAction = self.robot.currentAction
        self.state = rssiValues[x][y]
        self.observation_space = np.array(self.state)
        self.robot = Robot()
        self.robot.previousAction = previousAction
        self.robot.currentRssi = self.state
        self.robot.rect.x = x * 100
        self.robot.rect.y = y * 100
        self.game_length = 200
        self.game_done = False
        return self.state

    def populateRssi(self):
        # assigns from left to right -> next row
        for y in range(11):
            for x in range(11):
                rssi = RSSI()
                rssi.rect.x = x * 100
                rssi.rect.y = y * 100
                rssi.value = rssiValues[y][x]
                if rssi.value == 0:
                    rssi.image.fill(colors['yellow'])
                self.rssiBlockGroup.add(rssi)

    
            


# env = RobotEnv()
# env.populateRssi()
# scores = list()
# episodes = 100
# for episode in range(1, episodes+1):
#     state = env.reset()
#     done = False
#     score = 0 
    
#     while not env.game_done:

#         if pygame.event.get(pygame.QUIT):
#             break
#         env.render()
#         action = env.action_space.sample()
#         n_state, reward, done, info = env.step(action)
#         print(reward)
#         score+=reward
#     print("_"*50)
#     scores.append(score)
#     print('Episode:{} Score:{} x:{} y:{}'.format(episode, score, env.robot.rect.x,env.robot.rect.y))

# print(np.mean(scores))






