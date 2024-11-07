
from stable_baselines3 import PPO
import random

from segen.env_data_preparation.contract_env_data_preparation import  collect_env_data_for_seq_gen
from segen.envs.contract_env_discrete_action_space_05_5 import ContractEnv_55
from segen.utils import get_key_from_list, get_seq_from_key


def get_env(solidity_name: str, contract_name: str, solc_version:str="0.4.25", start_functions:list=[],target_functions:list=[],env_name:str="ContractEnv_55",flag_model:int=7, goal_indicator:int=2, num_svar:int=16,mode:str="predict",root_path_to_result_file:str="",data_json_file_name:str=""):


    conDynamics, conEnvData_wsa = collect_env_data_for_seq_gen(solidity_name,contract_name,solc_version=solc_version, root_path_to_result_file=root_path_to_result_file, data_json_file_name=data_json_file_name, start_functions=start_functions,target_functions=target_functions)
    if len(conEnvData_wsa)==0:
        return None
    if env_name in ["ContractEnv_55"]:
        env = ContractEnv_55(conDynamics, conEnvData_wsa, flag_model=flag_model,goal_indicator=goal_indicator,num_state_svar=num_svar,
                             mode=mode)

    env.contract_name = contract_name
    env.solidity_name = solidity_name
    return env

def retrieve_model(model_path:str):
    model = PPO.load(model_path)
    return model

def remove_repeated_sequences(sequences):
    seen = set()
    unique_sequences = []
    for seq in sequences:
        # Convert the sequence to a tuple to make it hashable
        seq_tuple = tuple(seq)
        if seq_tuple not in seen:
            seen.add(seq_tuple)
            unique_sequences.append(seq)
    return unique_sequences

def get_top_k_sequences(sequences:list, top_k:int=2):
    unique_sequences=remove_repeated_sequences(sequences)
    seq_counts=[[get_key_from_list(seq),sequences.count(seq)] for seq in unique_sequences]
    seq_counts.sort(key=lambda x:x[1], reverse=True)
    unique_sequences.sort(key=len,reverse=False)
    if len(seq_counts)>top_k:
        if top_k>=2:
            if len(get_seq_from_key(seq_counts[0][0]))==4 and len(get_seq_from_key(seq_counts[1][0]))==4:
                for key, _ in seq_counts[top_k:]:
                    if len(get_seq_from_key(key))==2:
                        return [get_seq_from_key(key) for key, _ in seq_counts[0:top_k-1]]+[get_seq_from_key(key)]
            # check if [a,a] exits
            special_seq=[]
            for key,_ in seq_counts:
                seq=get_seq_from_key(key)
                if len(seq)==2:
                    if len(list(set(seq)))==1:
                        special_seq.append(seq)
            if len(special_seq)>=top_k:
                return special_seq[0:top_k]
            else:
                if len(special_seq)==1:
                    return special_seq+[get_seq_from_key(key) for key, _ in seq_counts[0:top_k-1]]
                else:
                    return [get_seq_from_key(key) for key,_ in seq_counts[0:top_k]]

        return [get_seq_from_key(key) for key,_ in seq_counts[0:top_k]]
    else:
        return [get_seq_from_key(key) for key,_ in seq_counts]




def refine_sequences(sequences:list)->list:
    kept=[]
    for seq in sequences:
        if len(seq) - len(set(seq)) >=2 or (len(seq) - len(set(seq))==1 and len(seq)==4):
            seq_=[]
            for ftn in seq[0:-1]:
                if ftn not in seq_:
                    seq_.append(ftn)
            seq_.append(seq[-1])
            if seq_ not in kept:
                kept.append(seq_)

        else:
            if seq not in kept:
                kept.append(seq)
    return kept

def remove_contract_name_from_function_name(sequences: list, contract_name: str):
    temp = [[func.split(f'{contract_name}.')[-1] if f'{contract_name}.' in func else func for func in seq] for seq
            in sequences]
    return [[func.split(f'.')[-1] if '.' in func else func for func in seq] for seq in temp]


if __name__=="__main__":
    seq=[[1,2,3,4],[2,3,4,5],[2,3,4,5],[1,2,3,4],[2,3],[2,3,4]]
    print(get_top_k_sequences(seq,top_k=3))