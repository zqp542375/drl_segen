
# # for small dataset
max_svar_value=80
max_func_value_element=30

# # for sGuard dataset
# max_svar_value=5740
# max_func_value_element=70

import os
import sys

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f'Project root: {get_project_root()}/')
sys.path.append(get_project_root())
# RL_dir=f'{get_project_root()}/'
RL_dir="./"
contracts_data_path=f'{RL_dir}segen/contract_env_data/'
result_path=f'{RL_dir}train_results/'
output_path=result_path
seq_len_limit=4
contract_solidity_path=f'{RL_dir}datasets/'