# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 17:36:31 2024

@author: SERC
"""
import gymnasium

from segen.utils import weighted_random_selection


class RandomEnv(gymnasium.Env):

  def __init__(self, envs):
    super(RandomEnv, self).__init__()
    self.envs= envs
    self.env_idx=0
    self.num_envs = len(envs)
    self.action_space=envs[0].action_space
    self.observation_space=envs[0].observation_space
    if envs[0].env_name in ["ContractEnv_33","ContractEnv_55","ContractEnv_70"]:
        self.weights=[len(env.conEnvData_wsa["function_data"].keys())**2/3 for env in envs]

    else:        
        self.weights=[len(env.conEnvDataWrapper.function_data.keys())**2/3 for env in envs]

  def step(self,action):
    # Sample an environment
    env = self.envs[self.env_idx]
    # Step wait on it
    obs, reward, done, _,info = env.step(action)
    return obs, reward, done, _,info
    # method_name = "step"
    # return self.venv.env_method(method_name,indices=self.env_idx)

  def reset(self,seed:int=None,options={}):
    # self.env_idx = random.randint(0, self.num_envs - 1)
    self.env_idx=weighted_random_selection(list(range(0,self.num_envs,1)), self.weights)
   
    return self.envs[self.env_idx].reset()
    # return self.venv.env_method(method_name, indices=self.env_idx)

  # def valid_action_mask(self):
  #     env=self.envs[self.env_idx]
  #     action_mask = np.zeros(env.action_space.n)
  #     for valid_action in env.valid_actions:
  #       action_mask[valid_action]=1
  #     return action_mask
  def valid_action_mask(self):
      env=self.envs[self.env_idx]
      # action_mask = np.zeros(env.action_space.n)
      # for valid_action in env.valid_actions:
      #   action_mask[valid_action]=1
      return env.action_masks()