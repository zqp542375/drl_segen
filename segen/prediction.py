from sb3_contrib import MaskablePPO
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy


def my_model_prediction(model, env, num_episodes):

  result_list=[]
  for i in range(num_episodes):
      obs, _ = env.reset()
      while not env.done:

          action, _states = model.predict(obs)
          obs, reward, done, _, info = env.step(action)

      if env.env_name is not None and env.env_name in [ "ContractEnv_55",]:
          print(f'score:{env.score}')
          print(f'\taction seq:{env.previous_actions}')
          print(f'\t  func seq:{env.func_seq}')
          result_list.append([env.conEnvData_wsa["function_data"][str(func)]["name"] for func in env.func_seq])

      elif env.env_name in ["ContractEnv_33"]:

          print(f'score:{env.score}')
          print(f'\taction seq:{env.previous_actions}')
          result_list.append(
              [env.conEnvData_wsa["function_data"][str(func)]["name"] for func
               in env.previous_actions])
          # start_funtions=env.conEnvData_wsa["start_functions_in_integer"]
          # if env.previous_actions[0] in start_funtions:
          #     print(f'score:{env.score}')
          #     print(f'\taction seq:{env.previous_actions}')
          #     result_list.append(
          #         [env.conEnvData_wsa["function_data"][str(func)]["name"] for func
          #          in env.previous_actions])

      else:
          return []

      if len(result_list)==num_episodes:
          break


  return result_list


def my_model_prediction_rewards(model, env, num_episodes, flag_maskable:bool=True):
  rewards=[]

  for i in range(num_episodes):
      obs, _ = env.reset()
      while not env.done:
          if flag_maskable:
              action_masks = env.action_masks()
              action, _states = model.predict(obs, action_masks=action_masks)
              # action, _states = model.predict(obs)
              obs, reward, done, _, info = env.step(action)
              # print(f'\taction:{action};reward:{reward};obs:{obs}')
          else:
              action, _states = model.predict(obs)
              obs, reward, done, _, info = env.step(action)


      rewards.append(env.score)

      if len(rewards)==num_episodes:
          break


  return rewards



def print_functions(function_data:dict,target_functions:list):
    for func_int, data in function_data.items():
        print(f'{func_int}: {data["pure_name"]}')
    print(f'targets:{target_functions}')



def evaluate_general(models_dir, env, model_file_name, num_episodes:int=5, flag_maskable:bool=False):
    if flag_maskable:
        model =  MaskablePPO.load(f"{models_dir}/{model_file_name}.zip")
    else:
        model = PPO.load(f"{models_dir}/{model_file_name}.zip")

    env.test = True
    results=[]
    if env.env_name in ["ContractEnv_55", "ContractEnv_33"]:
        # print(f'\n==== {env.solidity_name}:{env.contract_name} ====')
        # for key, info in env.conEnvData_wsa["function_data"].items():
        #     print(f'{key}:{info["name"]}')

        for target in env.conEnvData_wsa["target_functions_in_integer"]:
            result=[target,env.conEnvData_wsa["function_data"][str(target)]['name']]
            env.goal = target

            # # print(env.conEnvData_wsa["function_data"].keys())
            # print(f'target : {target} : {env.conEnvData_wsa["function_data"][str(target)]["name"]}')

            # Evaluate the agent
            if flag_maskable:
                mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=num_episodes)
                # print(f'\tMean reward: {mean_reward}, Std reward: {std_reward}')
            else:
                mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=num_episodes)
                # print(f'\tMean reward: {mean_reward}, Std reward: {std_reward}')
            result.append(mean_reward)
            result.append(std_reward)
            results.append(result)
    return results
