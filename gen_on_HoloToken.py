from segen.contract_env_data.contract_info import small_dataset_train_g_8_19, sGuard_test_g_8_19
from segen.gen_utils import get_env, refine_sequences, get_top_k_sequences, remove_contract_name_from_function_name, \
    retrieve_model
from segen.prediction import evaluate_general, my_model_prediction
from segen.config import RL_dir,contracts_data_path


root_model_dir= f'{RL_dir}train_results/models/'

small_dataset_data_file="rl_small_dataset_contracts_data_for_env_construction_8_19_2024_8_in_integer.json"
models_folder_and_file_name={
    "HoloToken":["ContractEnv_55_model7_small_dataset_8_20_1724125326_HoloToken","17380000"],
    "small_dataset":["ContractEnv_55_model7_small_dataset_8_1724161007","43100000"]
}

# models_folder_and_file_name={
#     "sGuard_dataset":["ContractEnv_55_model7_sGuard_16_1724508857","414180000"],
# }
# sGuard_data_file="rl_sGuard_contracts_data_for_env_construction_8_19_2024_16_in_integer.json"


def evaluate( data, model_dir, model_file_prefix,contract_data_file_path,contract_data_file_name):
    solidity_name = data['solidity_name']
    contract_name = data['contract_name']

    if 'solc_version' in data.keys():
        solc_version = data['solc_version']
    else:
        solc_version = '0.4.25'
    top_k = data['top_k']
    target_functions = data['target_functions']
    start_functions = data['start_functions']
    if isinstance(top_k, str):
        top_k = int(top_k)

    results = {}
    env = get_env(solidity_name, contract_name, solc_version=solc_version, start_functions=start_functions,
                  target_functions=target_functions,
                  num_svar=8,
                  root_path_to_result_file=contract_data_file_path,
                  data_json_file_name=contract_data_file_name
                 )
    if env is None:
        print(
            f'Fail to construct environment (possible reasons: the contract is an unseen contract, fail to compile the contract)')
        return {}

    test_rewards = evaluate_general(model_dir, env, model_file_prefix, 5)

    return test_rewards

def generate_sequences(data, model_dir, model_file_prefix,contract_data_file_path,contract_data_file_name):

    solidity_name=data['solidity_name']
    contract_name=data['contract_name']

    if 'solc_version' in data.keys():
        solc_version=data['solc_version']
    else:
        solc_version='0.4.25'

    top_k=data['top_k']
    target_functions=data['target_functions']
    start_functions=data['start_functions']
    if isinstance(top_k,str):
        top_k=int(top_k)

    results={}
    env = get_env(solidity_name, contract_name, solc_version=solc_version, start_functions=start_functions,
                  target_functions=target_functions,
                  num_svar=8,
                  root_path_to_result_file=contract_data_file_path,
                  data_json_file_name=contract_data_file_name,
                  mode="test"
                 )
    if env is None:
        print(f'Fail to construct environment (possible reasons: the contract is an unseen contract, fail to compile the contract)')
        return {}

    results={}
    for target in env.conEnvData_wsa["target_functions_in_integer"]:
        env.goal = target
        goal_name=env.conEnvData_wsa["function_data"][str(target)]["name"]
        results[goal_name]=[]

    model=retrieve_model(f"{model_dir}/{model_file_prefix}.zip")
    for target in env.conEnvData_wsa["target_functions_in_integer"]:
        env.goal = target
        goal_name = env.conEnvData_wsa["function_data"][str(target)][
            "name"]
        print(f'\ntarget : {target} : {goal_name}')
        predict_results=my_model_prediction(model, env, 5)
        clean_sequence=remove_contract_name_from_function_name(predict_results,contract_name)
        results[goal_name]+=clean_sequence

    for k in results.keys():
        results[k]=refine_sequences(get_top_k_sequences(results[k], top_k=top_k))

    return results


def generate_sequences_HoloToken():
    # =======================
    # for small dataset
    data = {"solidity_name": "HoloToken.sol",
            "contract_name": "HoloToken",
            "solc_version": "0.4.18",
            "start_functions": ['setDestroyer', 'setMinter', 'transferOwnership', 'decreaseApproval',
                                'increaseApproval'],
            "target_functions": ['transferFrom', 'mint', 'burn', 'transfer', 'approve', 'finishMinting',
                                 'decreaseApproval'],
            'top_k': 2,
            }
    print(f'\n======= 5 Episodes for each target ========')
    result = generate_sequences(data,
                      root_model_dir + models_folder_and_file_name['HoloToken'][0],
                      models_folder_and_file_name['HoloToken'][1],
                      contracts_data_path,
                      small_dataset_data_file,
                      )
    print(f'\n======= Generated Sequences ========')
    for target, sequences in result.items():
        print (f'{target} ----')
        for item in sequences:
            print(f'\t{item}')

if __name__ == '__main__':
    generate_sequences_HoloToken()


