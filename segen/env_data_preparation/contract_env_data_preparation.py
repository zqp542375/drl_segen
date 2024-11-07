
from segen.env_data_preparation.contract_dynamics import ContractDynamics

from segen.utils import load_a_json_file
import os



def list_files(directory,extenion:str=".txt"):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extenion):
                files.append(os.path.join(root, filename))
    return files

def get_key_from_list(data:list)->str:
    if len(data)==0: return ""
    if len(data)==1: return f'{data[0]}'
    key=f'{data[0]}'
    for item in data[1:]:
        key+=f'#{item}'
    return key

def get_seq_from_key(key: str) -> list:
    if '#' not in key:
        return [key]
    else:
        return key.split('#')

def collect_env_data(contract_info:str,root_path_to_result_file:str,data_json_file_name:str):
    
    
    contracts_data=load_a_json_file(f'{root_path_to_result_file}{data_json_file_name}')
    
    data=contracts_data[contract_info]
    
    sequences=data["function_sequences_in_integer"]
    left_s=[]
    for s in sequences:
        if s not in left_s:
            left_s.append(s)
   
    conDynamics=ContractDynamics(left_s,data["sequence_writes"],goals=data["target_functions_in_integer"])
        
    return conDynamics,data
    



def collect_env_data_for_seq_gen(solidity_name:str,contract_name:str, solc_version:str="0.4.25",root_path_to_result_file:str="",data_json_file_name:str="", start_functions:list=[],target_functions:list=[]):
    contracts_data = load_a_json_file(
        f'{root_path_to_result_file}{data_json_file_name}')

    contract_key = f'{solidity_name}{contract_name}'
    data = {}
    if contract_key in contracts_data.keys():
        # contracts in training or testing (have both static rw data and valid sequences collected)
        data = contracts_data[contract_key]
    else:
        # # assume that the data for a contract is collected and saved in a json data file
        # # contracts not in either training or testing sets (have static rw data)
        # rw_data_and_seq = parepare_rw_data_and_or_sequences(solidity_name, contract_name,
        #                           solc_version=solc_version,
        #                           target_functions=target_functions,
        #                           start_functions=start_functions)
        # if len(rw_data_and_seq)==0:
        #     data={}
        # else:
        #     data=contract_data_mapping_function_to_integer(contracts_data,rw_data_and_seq)
        pass
    if len(data)>0:
        sequences=data["function_sequences_in_integer"]
        left_s=[]
        for s in sequences:
            if s not in left_s:
                left_s.append(s)
        conDynamics=ContractDynamics(left_s,data["sequence_writes"],goals=data["target_functions_in_integer"])

        return conDynamics, data
    else:
        return None,{}



