from segen.config import contracts_data_path, RL_dir

from segen.contract_env_data.contract_info import small_dataset_train_g_8_19

from segen.train_interface import TrainWrapper
import time

contract_data_root_path=contracts_data_path
result_path= f'{RL_dir}results/'

# ==================================
# August 20th, 2024
# train on the 20 contracts from the small dataset
# 8:20

contract_data_root_path=contracts_data_path
result_path= f'{RL_dir}results/'

contract_data_in_json_file='rl_small_dataset_contracts_data_for_env_construction_8_19_2024_8_in_integer.json'
contracts_info=small_dataset_train_g_8_19

env_name='ContractEnv_55'
iteration=10000
flag_model=7
goal_indicator=2
mode='train'
maskable=False
dataset="small_dataset"
myTrain=TrainWrapper(env_name,contracts_info,contract_data_root_path,result_path,iterations=iteration,flag_write_record=True,goal_indicator=goal_indicator,num_svar=8,flag_model=flag_model,mode=mode,contract_data_in_json=contract_data_in_json_file)
time_name=int(time.time())
model_dir = f"{result_path}models/{env_name}_model{flag_model}_{dataset}_{num_svar}_{time_name}/"
log_dir = f"{result_path}logs/{env_name}_model{flag_model}_{dataset}_{num_svar}_{time_name}/"
myTrain.train(models_dir=model_dir, logdir=log_dir)

"""
tensorboard --logdir "path to the log files"
"""


