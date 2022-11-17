from DDDQN import DDDQN
import pygame
import numpy as np

def main(trainAgent= False,getAgent=True,visualize=False):

    dddqn = DDDQN()
    env = dddqn.env
    env.populateRssi()

    if trainAgent:
        dddqn.train_agent(50_000)

    if getAgent:
        dddqn = dddqn.get_agent()
        scores = list()
        episodes = 100
        for episode in range(1, episodes+1):
            state = env.reset()
            done = False
            score = 0 
            
            while not env.game_done:

                if pygame.event.get(pygame.QUIT):
                    break
                if visualize:
                    env.render()
                action = dddqn.forward(env.state)
                n_state, reward, done, info = env.step(action)
                score+=reward

            scores.append(score)
            print('Episode:{} Score:{} x:{} y:{} rssi: {}'.format(episode, score, env.robot.rect.x,env.robot.rect.y,env.robot.currentRssi))

        print(np.mean(scores))


# Train
# main(trainAgent=True,getAgent=False,visualize=False)

# Test
main(trainAgent=False,getAgent=True,visualize=True)