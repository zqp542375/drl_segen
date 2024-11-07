from segen.contract_env_data.contract_info import small_dataset_train_g_8_19, small_dataset_test_g_8_19
from gen_on_HoloToken import generate_sequences
from segen.config import RL_dir,contracts_data_path
root_model_dir= f'{RL_dir}train_results/models/'

small_dataset_data_file="rl_small_dataset_contracts_data_for_env_construction_8_19_2024_8_in_integer.json"
models_folder_and_file_name={
    "small_dataset":["ContractEnv_55_model7_small_dataset_8_1724161007","43100000"]
}

def generate_sequences_small_dataset():
    for item in small_dataset_test_g_8_19:
        if '.sol' in item:
            items=item.split('.sol')
            solidity_name=items[0]+".sol"
            contract_name=items[1]
            data = {"solidity_name": solidity_name,
                    "contract_name": contract_name,
                    "solc_version":" ",
                    "start_functions":[],
                    "target_functions":[],
                    'top_k':2,
                    "flag_whole":True}

            print(f'\n======= 5 Episodes for each target in contract {item}========')
            result = generate_sequences(data,
                                        root_model_dir + models_folder_and_file_name['small_dataset'][0],
                                        models_folder_and_file_name['small_dataset'][1],
                                        contracts_data_path,
                                        small_dataset_data_file,
                                        )
            print(f'\n======= Generated Sequences ========')
            for target, sequences in result.items():
                print(f'{target} ----')
                for item in sequences:
                    print(f'\t{item}')


if __name__ == '__main__':
    generate_sequences_small_dataset()