
# -*- coding: utf-8 -*-
"""
Rely on static analysis on the source code to get R/W of the state variables

"""
import time



from segen.config import RL_dir, contracts_data_path,num_svar
from segen.train_interface import TrainWrapper

from segen.contract_env_data.contract_info import sGuard_train_g_8_19



contract_data_root_path=contracts_data_path
result_path= f'{RL_dir}results/'



# ==================================
# August 24th, 2024
# train on the 20 contracts from the small dataset
# 8:20

contract_data_in_json_file='rl_sGuard_contracts_data_for_env_construction_8_19_2024_16_in_integer.json'
contracts_info=sGuard_train_g_8_19[0:1]
contracts_info=["0x99b9f9bC8eb415334aF4cd35e46b5967f7989168.solDIGIGO"]

env_name='ContractEnv_55'
iteration=100000
flag_model=7
goal_indicator=2
mode='train'
dataset="sGuard"
myTrain=TrainWrapper(env_name,contracts_info,contract_data_root_path,result_path,iterations=iteration,flag_write_record=True,goal_indicator=goal_indicator,num_svar=16,flag_model=flag_model,mode=mode,contract_data_in_json=contract_data_in_json_file)
time_name=int(time.time())
model_dir = f"{result_path}models/{env_name}_model{flag_model}_{dataset}_{num_svar}_{time_name}/"
log_dir = f"{result_path}logs/{env_name}_model{flag_model}_{dataset}_{num_svar}_{time_name}/"
myTrain.train(models_dir=model_dir, logdir=log_dir)

"""
tensorboard --logdir "path to the log files"
"""

