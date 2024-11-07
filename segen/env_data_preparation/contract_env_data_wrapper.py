# Append the directory to your python path using sys
from segen.env_data_preparation.contract_env_data_collection import EnvDataCollection02

from copy import (
       deepcopy,
)

def order_a_list_of_vector(vector_list:list)->list:
    """
    example vector_list:
        list_of_lists_a = [
          ['a' , [3, 1, 4]],
          ['b' ,  [1, 5, 9]],
          ['c' ,  [2, 6, 5]],
          ['e' ,  [3, 5, 8]]
        ]
    """
    # Define a custom sorting key based on the sum of elements
    def custom_sort(sublist):
        # sort  based on the second element of the sublist
        v=''
        for e in sublist[1]:
            v+=f'{e}'
        return int(v)

    # Use the sorted function with the custom sorting key
    sorted_list_of_lists = sorted(vector_list, key=custom_sort)
    return  sorted_list_of_lists


class CollectContractEnvData_wsa():
    """
    use the static analysis data to collect the required data

     
    """
    def __init__(self, envDataCollected: EnvDataCollection02,
                 num_state_var: int = 8, num_reads: int = 3,
                 num_writes: int = 3):
        
        self.envDataCollected = envDataCollected    
        self.num_state_var = num_state_var
        self.num_reads = num_reads
        self.num_writes = num_writes          

        
        self.state_variables_in_integer= sorted(self.envDataCollected.state_variables_in_integer)
        self.selected_svar=[]
        

        self.function_data = {}  # the keys, names, and vectors of functions
        self.function_value=[]
        self.function_value_n0=[]


           
    def get_functions_r_w_in_index(self):
        """
        use the indices to represent the state variables read/written by each function
        
        """
        
     
        if len(self.state_variables_in_integer)>self.num_state_var:
            self.selected_svar=self.state_variables_in_integer[0:self.num_state_var]
        else:
            self.selected_svar=self.state_variables_in_integer+[0]*(self.num_state_var-len(self.state_variables_in_integer))

        func_read_write_in_index={}
        
        for func in self.envDataCollected.function_reads_writes_in_integer.keys():
            r_w_info= self.envDataCollected.function_reads_writes_in_integer[func]

            read_int = []
            if "reads" in r_w_info.keys():
                read_int =deepcopy(r_w_info["reads"])
               
            write_int = []
            if "writes" in r_w_info.keys():
                write_int =deepcopy( r_w_info["writes"]  )             
               
            if len(read_int)==0 and len(write_int)==0:
              continue
          
            if len(read_int) > self.num_reads:
                read_int=sorted(read_int,reverse=False)
                read_int = read_int[0:self.num_reads]
            elif len(read_int) < self.num_reads:                
                read_int += [-1] * (self.num_reads - len(read_int))


            if len(write_int) > self.num_writes:
                write_int=sorted(write_int,reverse=False)
                write_int = write_int[0:self.num_writes]
            elif len(write_int) < self.num_writes:
                write_int += [-1] * (self.num_writes - len(write_int))

  
            read_indices=[ 1 if svar in read_int else 0 for svar in self.selected_svar]
            write_indices=[ 1 if svar in write_int else 0 for svar in self.selected_svar]
            func_read_write_in_index[func]={"reads":read_indices, 'writes':write_indices}           
            
            
            # if func in ['BHT.contTransfer(address,uint256)','BHE.contTransfer(address,uint256)']:
            #     print(f'---------------')
            #     print(f'self.selected_svar:{self.selected_svar}')
            #     print(f'read_int:{read_int}')
            #     print(f'read_indices:{read_indices}')                
            #     print(f'write_indices:{write_indices}')
            
        return func_read_write_in_index
            

  
    
    def collect_function_data(self):
        func_read_write_in_index_vector=self.get_functions_r_w_in_index()
            
        # combine read vectors and write vectors        
        func_rw_in_index={key:[e1*2+e2 for e1,e2 in zip(value['reads'],value['writes'])] for key,value in func_read_write_in_index_vector.items()}
        
        self.function_value=[0]*self.num_state_var
        for k,value in func_rw_in_index.items():
            # print(f'\t{value}:{k}')
            self.function_value=[e1+e2 for e1,e2 in zip(self.function_value,value)]  
        
        
        # print(f'self.function_value:{self.function_value}')
       
        self.function_value_n0=[0]*self.num_state_var
        for k,value in func_rw_in_index.items():
            if k not in ['constructor','constructor()']:
                # print(f'\t{value}:{k}')
                self.function_value_n0=[e1+e2 for e1,e2 in zip(self.function_value_n0,value)]  
        
        # print(f'self.function_value_n0:{self.function_value_n0}')
        # func_rw_data=[[key, value] for key,value in func_rw_in_index.items()]
        # sorted_func_rw_data=sort_lists(func_rw_data,index=1)
        

        for name, comb_rw_vector_in_index in func_rw_in_index.items():           
            
                
            reads=self.envDataCollected.function_reads_writes_in_integer[name]['reads']
            writes=self.envDataCollected.function_reads_writes_in_integer[name]['writes']
            
            reads=sorted(reads,reverse=False)
            writes=sorted(writes,reverse=False)
            # from comb_rw_in_idx_new to get reads and writes and the last element used to distinguish functions with the same presentation

                    
            reads_=reads[0:3] if len(reads)>=3 else reads+[0]*(3-len(reads))
            writes_=writes[0:3] if len(writes)>=3 else writes+[0]*(3-len(writes))

            func_rw_in_concate=reads_+writes_
            
            if '(' in name:
                pure_name=name.split('(')[0]
            else:
                pure_name=name
            if '.' in pure_name:
                pure_name=pure_name.split('.')[-1]
           
            if name=='constructor':
                
               self.function_data[name] = {'name': name, 
                                               "pure_name":pure_name, 
                                               "reads":reads,
                                               "writes":writes,
                                               "vector_in_index_rw":comb_rw_vector_in_index, #old: comb_rw_vector_in_index,
                                               "vector_rw_in_concate":func_rw_in_concate
                                               }
               
            else:
            
                self.function_data[name] = {'name': name, 
                                                "pure_name":pure_name, 
                                                "reads":reads,
                                                "writes":writes,
                                                "vector_in_index_rw":comb_rw_vector_in_index, 
                                                "vector_rw_in_concate": func_rw_in_concate
                                                }
           
                
                
        if 'constructor' not in self.function_data.keys():
            self.function_data['constructor'] = {'name': "constructor()", 
                                            "pure_name":"constructor", 
                                            "reads":[],
                                            "writes":[],
                                            "vector_in_index_rw":[0]*self.num_state_var, 
                                            "vector_rw_in_concate":[0]*(self.num_reads+self.num_writes)
                                            }
            
    
         
        

    def obtain_contract_data(self):
        self.collect_function_data()
        data={
            "state_variable": self.envDataCollected.state_variables,         
            "state_variables_in_integer":self.state_variables_in_integer,
            "state_variables_selected":self.selected_svar, # select 8 state variables
            "function_value":self.function_value,
            "function_value_n0":self.function_value_n0,
            "function_data":self.function_data,
            "function_sequences":self.envDataCollected.function_sequence_writes,
            "functions_in_sequences":self.envDataCollected.functions_in_sequences,
            "target_functions":self.envDataCollected.targets,
            "start_functions":self.envDataCollected.start_functions
            }
            
        return data
           



        
