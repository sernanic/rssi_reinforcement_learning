from RobotENV import RobotEnv 
# tensorflow
from tensorflow import keras
from keras.layers import Dense,Flatten,LSTM
from keras.models import Sequential, load_model
from keras.optimizers import Adam
# tensorflow reinforcement learning
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
import numpy as np
import wandb
from wandb.keras import WandbCallback

wandb.init(project="my-test-project")
wandb.define_metric("batch")
wandb.define_metric("epoch")

wandb.define_metric("train_accuracy", step_metric="batch")
wandb.define_metric("val_accuracy", step_metric="epoch")
class DDDQN():
  
  def __init__(self):
    self.model = Sequential()
    self.policy = BoltzmannQPolicy()
    self.memory = SequentialMemory(limit=50_000, window_length=1)
    self.env = RobotEnv()

  def build_model(self,states, actions):   
    self.model.add(Dense(24, activation='relu', input_shape=states))
    self.model.add(Dense(24, activation="relu"))
    self.model.add(Dense(actions, activation='linear'))
    return self.model

  def build_agent(self, actions):
      
      dqn = DQNAgent(model=self.model, memory=self.memory,policy=self.policy,
                    nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2,
                    enable_double_dqn=True,enable_dueling_network=True,dueling_type="avg")
      return dqn

  def train_agent(self,steps=50_000):
    self.env.populateRssi()
    states = self.env.observation_space.shape
    actions = self.env.action_space.n
    self.model = self.build_model(states, actions)
    # self.model.summary()
    dqn = self.build_agent(actions)
    dqn.compile(Adam(lr=1e-3), metrics=['accuracy'])
    dqn.fit(self.env, nb_steps=steps, visualize=False, verbose=1,callbacks=[WandbCallback()])
    dqn.save_weights('dqn_weights_LSTM.h5f', overwrite=True)
  
  def get_agent(self):
    self.env.populateRssi()
    actions = self.env.action_space.n
    states = self.env.observation_space.shape
    print(states)
    model = self.build_model(states, actions)
    dqn = self.build_agent(actions)
    dqn.compile(Adam(lr=1e-3), metrics=['accuracy'])
    dqn.load_weights('dqn_weights_LSTM.h5f')
    return dqn




