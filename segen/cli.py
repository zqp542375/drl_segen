import argparse
import os

import segen.config
from segen.config import contracts_data_path, max_func_value_element, max_svar_value
from segen.train_interface import TrainWrapper
import ast
import json
import time

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_list_of_lists(value):
    try:
        # Parse the string representation of the list of lists into an actual list of lists
        return ast.literal_eval(value)
    except (ValueError, SyntaxError) as e:
        raise argparse.ArgumentTypeError(f"Invalid value for list of lists: {value}")

def main():

    """
        contracts_info=sGuard_train
        # contracts_info=contracts_test_1[4:5]
        env_idx=2
        iteration=100000
        flag_model=6
        goal_indicator=0
        mode='train'
        maskable=False
        myTrain=TrainWrapper(env_names[env_idx], contracts_info, contract_data_root_path, result_path, iterations=iteration, flag_write_record=True, goal_indicator=goal_indicator, flag_maskable=maskable, flag_model=flag_model, mode=mode)

        myTrain.train()

    """


    parser = argparse.ArgumentParser(description='Description of your program',add_help=True)

    # Add options
    parser.add_argument('-env',"--environment-name", type=str, default='ContractEnv_33',
                        help='the name of the environment')
    parser.add_argument(
        "--contract-info-list",
        type=parse_list_of_lists,
        default=[],
        help="Provide the contracts to train or test.",
    )
    parser.add_argument(
        "--contract-info-list-json",
        default="",
        type=str,
        help="Provide the path and name of the json file containing the contract info.",
    )

    parser.add_argument(
        "--contract-info-list-json-key",
        type=str,
        default="contracts_train_1",
        help="The key to the data in the json file containing contract info.",
    )


    parser.add_argument('--iteration', default=1000,type=int,
                        help='set how many iterations to train the model')

    parser.add_argument('--goal-rewarding-indicator', default=0,type=int,
                        help='select a method to reward when a goal is reached')

    parser.add_argument('--flag-maskable', default=False, action="store_true",
                        help='indicate whether to apply maskable PPO.')

    parser.add_argument('--flag-model', default=1,type=int,
                        help='select the model for training available in the environment')

    parser.add_argument('--mode', choices=['train', 'test', 'predict'],
                        default='train',
                        help='determine how to deal with the model')

    parser.add_argument('--contract-data-in-json-file', type=str,default='contracts_data_small_set_4_15_24_in_integer.json',
                        help='specify the json file containing the contract data for environment construction.')


    parser.add_argument('--model-path', type=str,
                        help='indicate the path where the model is saved')

    parser.add_argument('--contract-data-path', type=str, default=contracts_data_path,
                        help='indicate the path where the json file is available that contains the contract data')

    parser.add_argument('--result-path', type=str, default="./",
                        help='indicate the path to save models and logs')


    parser.add_argument('--max-svar-value', default=5740,type=int,
                        help='the max integer value to denote a state variable.')
    parser.add_argument('--max-func-value-element', default=70, type=int,
                        help='the max integer value of an element in function vectors.')
    # Parse arguments
    args = parser.parse_args()
    segen.config.max_svar_value=args.max_svar_value
    segen.config.max_func_value_element=args.max_func_value_element
    segen.config.RL_dir="./"
    print(segen.config.max_svar_value)
    print(segen.config.max_func_value_element)

    if args.environment_name in ['ContractEnv_33','ContractEnv_55']:
        contract_info=args.contract_info_list
        key1=""
        key2=""
        if len(args.contract_info_list)==0:
            if len(args.contract_info_list_json)==0:
                print("need to provide the information about the contracts to be trained or tested.")
                return
            else:
                with open(args.contract_info_list_json, 'r') as file:
                    data = json.load(file)
                    if "," in args.contract_info_list_json_key:
                        items=args.contract_info_list_json_key.split(f',')
                        key1=items[0]
                        key2=items[1]
                    else:
                        key1=args.contract_info_list_json_key
                        key2=""

                    if key1 in data.keys():
                        contract_info=data[key1]
                        if isinstance(contract_info,dict):
                            if key2 in contract_info.keys():
                                contract_info=contract_info[key2]
                            else:
                                print("need to provide the correct group key to access the info in the json file.")
                                return
                    else:
                        print("need to provide the key to access the info in the json file.")
                        return

        myTrain = TrainWrapper(args.environment_name, contract_info, args.contract_data_path, args.result_path,
                               iterations=args.iteration, goal_indicator=args.goal_rewarding_indicator, flag_maskable=args.flag_maskable,
                               flag_write_record=False, flag_model=args.flag_model, mode=args.mode,contract_data_in_json=args.contract_data_in_json_file)
        if args.mode in ['train']:
            if len(key2)>0:
                time_name=int(time.time())
                model_dir=f"{args.result_path}models/{args.environment_name}_{key2}_{time_name}/"
                log_dir=f"{args.result_path}logs/{args.environment_name}_{key2}_{time_name}/"
            elif len(key1)>0:
                time_name = int(time.time())
                model_dir = f"{args.result_path}models/{args.environment_name}_{key1}_{time_name}/"
                log_dir = f"{args.result_path}logs/{args.environment_name}_{key1}_{time_name}/"
            else:
                model_dir=""
                log_dir=""

            myTrain.train(models_dir=model_dir,logdir=log_dir)
        elif args.mode in ['test']:
            myTrain.test(which_iteration=args.iteration,models_dir=args.model_path)
        else:
            pass

    else:
        print(f'the given environment is not handled yet:{args.dataset}')
        exit()



