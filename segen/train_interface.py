# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 20:23:55 2024

@author: SERC
"""

import time


from segen.train_and_eval import PPO_mlpPolicy_train_RanomEnv,evaluate_model

from segen.env_data_preparation.contract_env_data_preparation import collect_env_data

from segen.envs.contract_env_discrete_action_space_05_5 import ContractEnv_55



class TrainWrapper():
    def __init__(self, env:str, contract_names:list, contract_data_file_root:str, result_path:str, iterations:int=60, flag_write_record:bool=False, goal_indicator:int=0, num_svar:int=16, flag_model:int=1, mode:str= "train", contract_data_in_json:str=""):
        self.env_str=env
        self.contract_names=contract_names
        
        self.contract_data_file_root=contract_data_file_root
        self.iterations=iterations
        self.flag_write_record=flag_write_record
        self.goal_indicator=goal_indicator

        self.flag_maskable=False
        self.num_svar=num_svar
        self.flag_model=flag_model
        self.mode=mode
        
        self.models_dir=''
        self.logdir=''
        self.result_path=result_path
        self.contract_data_in_json_file=contract_data_in_json

        
    def train(self,models_dir:str="",logdir:str=''):
        print(f'==== {self.env_str} ====')
        envs=[self.get_env(name) for name in self.contract_names]
        # remove contracts who does not have targets
        envs=[env for env in envs if len(env.goals)>0]
        
        # train
        # project_path=RL_dir+"explore_small_discrete_action_space/"
        if len(models_dir)>0 and len(logdir)>0:
            self.models_dir=models_dir
            self.logdir=logdir
        else:
            name=int(time.time())
            self.models_dir = f"{self.result_path}models/{name}/"
            self.logdir = f"{self.result_path}logs/{name}/"


        PPO_mlpPolicy_train_RanomEnv(envs, self.models_dir, self.logdir, iterations=self.iterations)


    def test(self, which_iteration:int=0,models_dir:str=""):
        envs=[self.get_env(name) for name in self.contract_names]
        # remove contracts who does not have targets
        envs=[env for env in envs if len(env.goals)>0]
        if which_iteration<0: print('"which_iteration" must not be negatiave')
        if which_iteration==0:
            iteration=self.iterations
        else:
            iteration=which_iteration
        if len(models_dir)==0:
            model_dir=self.models_dir
        else:
            model_dir=models_dir

        evaluate_model(model_dir, envs, f'{iteration}0000')


    def traning_log_address(self):
        return self.logdir

        
    def get_env(self, contract_info:str):
        print(f'\n==== Get environment for contract  {contract_info} ====')
        if '.sol' in contract_info:
            items=contract_info.split(f'.sol')
            solidity_name=f'{items[0]}.sol'
            contract_name=items[1]
        else:
            solidity_name=''
            contract_name=contract_info
        env=None

        if self.env_str in ['ContractEnv_55']:
            conDynamics,conEnvData_wsa=collect_env_data(contract_info,self.contract_data_file_root,self.contract_data_in_json_file)
            env=ContractEnv_55(conDynamics,conEnvData_wsa,flag_model=self.flag_model,mode=self.mode,num_state_svar=self.num_svar)
            env.contract_name=contract_name
            env.solidity_name=solidity_name
        return env
            
    def get_envs(self)->list:
        envs=[self.get_env(name) for name in self.contract_names]
        return [env for env in envs if env is not None and len(env.goals)>0]

