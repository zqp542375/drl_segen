# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 17:35:25 2024

@author: SERC
"""
import gymnasium
import numpy as np
import os

from sb3_contrib import RecurrentPPO
from stable_baselines3 import PPO
from segen.envs.randomly_select_envs import RandomEnv

def mask_fn(env:gymnasium.Env) -> np.ndarray:
    # Do whatever you'd like in this function to return the action mask
    # for the current env. In this example, we assume the env has a
    # helpful method we can rely on.
    return env.valid_action_mask()


def check_env_random_baseline(env:gymnasium, episodes:int=10):
 	for episode in range(episodes):
 	 	# print('========================')
 	 	obs,_ = env.reset()
 	 	i=0
 	 	while not env.done:#not done:

 	 	 	print('------------------------')
 	 	 	print('time step: ',i)
 	 	 	random_action = env.action_space.sample()
 	 	 	print("state: ",obs)
 	 	 	print("action: ",random_action)
 	 	 	obs, reward, done,_, info = env.step(random_action)
 	 	 	print('reward: ',reward)
 	 	 	print('new state: ',obs)
 	 	 	i+=1
		# print(f'episode {episode}; socre: {env.score}; state:{env.state}')
		# if episode%500==0:
		# 	print(f'episode {episode}; socre: {env.score}; state:{env.state}')
 	 	if env.score>=2:
 	 	 	print(f'episode {episode}; socre: {env.score};  obs:{obs}')


def PPO_MlpLstmPolicy_train_RanomEnv(env_list,models_dir:str,logdir:str,iterations:int=2):
  """
  train in multiple environments
  """
    
  if not os.path.exists(models_dir):
    os.makedirs(models_dir)

  if not os.path.exists(logdir):
    os.makedirs(logdir)


  TIMESTEPS = 10000
  iters = 0 
 

  env = RandomEnv(env_list)
 
  env.reset() 

  model = RecurrentPPO("MlpLstmPolicy", env,verbose=1,tensorboard_log=logdir)
 

  for i in range(iterations):
    iters += 1
    model.learn(TIMESTEPS, reset_num_timesteps=False)
    model.save(f"{models_dir}/{TIMESTEPS*iters}")


def PPO_mlpPolicy_train_RanomEnv(env_list,models_dir:str,logdir:str,iterations:int=2):
  """
  train in multiple environments
  """
    
  if not os.path.exists(models_dir):
    os.makedirs(models_dir)

  if not os.path.exists(logdir):
    os.makedirs(logdir)


  TIMESTEPS = 10000
  iters = 0 
 

  
  env = RandomEnv(env_list) 
  env.reset() 

  
  model = PPO('MlpPolicy', env, verbose=1,tensorboard_log=logdir,batch_size=64)

  for i in range(iterations):
    iters += 1
    model.learn(TIMESTEPS, reset_num_timesteps=False)
    model.save(f"{models_dir}/{TIMESTEPS*iters}")
    
def evaluate_details(model,env_list,num_episodes:int=5):
    
  def evaluate(env,num_episodes):
      for i in range(num_episodes):
          obs,_ = env.reset()
          while not env.done:         
            action, _states = model.predict(obs)
            obs, reward, done, _,info = env.step(action)
            # print(f'\taction:{action};reward:{reward};obs:{obs}')
          if env.env_name is not None and env.env_name in ["ContractEnv_55"]:
              print(f'score:{env.score}')            
              print(f'\taction seq:{env.previous_actions}')
              print(f'\t  func seq:{env.func_seq}')
          else:
              print(f'score:{env.score};obs(last 5 elements):{obs[-5:]}')

  for env in env_list:
    env.test=True
    
    if env.env_name in ["ContractEnv_55"]:
        print(f'\n==== {env.solidity_name}:{env.contract_name} ====')
            
        for key,info in env.conEnvData_wsa["function_data"].items():
          print(f'{key}:{info["name"]}')
          
        for target in env.conEnvData_wsa["target_functions_in_integer"]:
          env.goal=target
          # print(env.conEnvData_wsa["function_data"].keys())
          print(f'target : {target} : {env.conEnvData_wsa["function_data"][str(target)]["name"]}')
          evaluate(env,num_episodes)
    else:
    
        if len(env.contract_name)>0:
            name=env.contract_name
            name=name.replace(".sol",".sol:")
            print(f'\n==== {name} ====')
            
        for key,info in env.conEnvDataWrapper.function_data.items():
          print(f'{key}:{info["name"]}')
          
        for target in env.conEnvDataWrapper.targets:
          env.goal=target
          print(f'target : {target} : {env.conEnvDataWrapper.function_data[target]["name"]}')
          
          evaluate(env,num_episodes)






def evaluate_model(models_dir:str,env_list,model_name_sufix:str,num_episodes:int=5):    
    
  model = PPO.load(f"{models_dir}/{model_name_sufix}.zip")
  evaluate_details(model,env_list,num_episodes=num_episodes)



