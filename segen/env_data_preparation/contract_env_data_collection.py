import ast


class EnvDataCollection02():
    """
    prepare for the data needed to create environments
        static analysis data
        arg1 (a list of files): file containing the data resulted from the symbolic execution  
        

    """

    def __init__(self, solidity_file_name:str,contract_name:str, files_of_se_data:list):
        
        self.solidity_file_name=solidity_file_name
        self.contract_name=contract_name
        
        
        
        
        self.file_paths_for_se_data=files_of_se_data       
        
        self.targets = []
        self.start_functions=[]
        self.functions_in_sequences = [] # get the function appearing in sequences
        self.function_sequence_writes = {}
        
        
        
        self.state_variables = []
        self.state_variables_in_integer=[]
        
        self.function_reads_writes = {}
        self.function_sequence_writes = {}
        self.function_reads_writes_in_integer={}
        
        


        




    def init(self):
        self.get_execution_data( self.file_paths_for_se_data)

        self.get_functions_in_sequences()

            

    def get_execution_data(self, file_paths: [str]):
        def get_key_from_list(data_list: list) -> str:
            if len(data_list) == 0:
                return ''
            else:
                key = data_list[0]
                for item in data_list[1:]:
                    key += "#" + item
                return key

        for file_path in file_paths:
            flag_reads = False
            flag_writes = False
            flag_start_function= False
            with open(file_path) as file:
                for line in file:
                    line = line.strip()
                    if len(line) == 0: continue
                    # print(f'{line}')
                    if ":writes at the last depth:" in line:
                        items = line.split(":")
                        seq = ast.literal_eval(items[0])
                        
                        seq_=[func.split(f'(')[0] if '(' in func else func for func in seq]
                        
                        writes = ast.literal_eval(items[-1])
                        seq_key=get_key_from_list(seq_)
                        
                        writes_int=[int(ele) for ele in writes  if len(ele)>0]
                        if seq_key not in self.function_sequence_writes.keys():
                            self.function_sequence_writes[seq_key] =writes_int
                        else:
                            for w in writes_int:
                                if w not in self.function_sequence_writes[seq_key]:
                                    self.function_sequence_writes[seq_key].append(w)
                        if flag_start_function:
                            if seq_[0] not in self.start_functions:
                                self.start_functions.append(seq_[0])
                        
                        continue
                    else:
                        if "targets:[" in line:
                            targets=ast.literal_eval(
                                line.split('targets:')[-1])
                            for t in targets:
                                t_= t.split(f'(')[0] if '(' in t else t
                                if t_ not in self.targets:
                                    self.targets.append(t_)
                            continue
    
                        elif "Function Reads: State variables read in conditions" in line:
                            flag_reads = True
                            flag_writes = False
                            continue
                        elif "Function Writes: State variables written" in line:
                            flag_reads = False
                            flag_writes = True
                            continue
                        elif "iteration:3" in line:
                            flag_reads = flag_writes = False
                            flag_start_function=True
                            continue
                        elif "iteration:4" in line:
                           
                            flag_start_function=False
                            continue
                    if "=====================" in line: continue
                    # get the state variables read in conditions
                    if flag_reads:
                        items = line.split(':')
                        reads = ast.literal_eval(items[-1])
                        reads = [int(read) for read in reads]
                        if items[0] not in self.function_reads_writes.keys():
                            self.function_reads_writes[items[0]] = {'reads': reads}
                        else:
                            for read in reads:
                                if read not in self.function_reads_writes[items[0]][
                                    'reads']:
                                    self.function_reads_writes[items[0]][
                                        'reads'].append(read)
                    # get the state variables written
                    if flag_writes:
                        items = line.split(':')
                        writes = ast.literal_eval(items[-1])
                        writes = [int(write) for write in writes]
                        if items[0] not in self.function_reads_writes.keys():
                            self.function_reads_writes[items[0]] = {
                                'writes': writes}
                        else:
                            if 'writes' not in self.function_reads_writes[
                                items[0]].keys():
                                self.function_reads_writes[items[0]][
                                    'writes'] = writes
                            else:
                                for write in writes:
                                    if write not in \
                                        self.function_reads_writes[items[0]][
                                            'writes']:
                                        self.function_reads_writes[items[0]][
                                            'writes'].append(write)
                                        
        print(f'start function: {self.start_functions}')
        print(f'target function: {self.targets}')
        # for func, value in self.function_sequence_writes.items():
        #     print(f'{func}:{value}')



    def get_functions_in_sequences(self):
        def get_seq_from_key(key: str):
            if '#' in key:
                return key.split("#")
            else:
                return [key]

        for key in self.function_sequence_writes.keys():
            key_seq = get_seq_from_key(key)
            for func in key_seq:
                if func not in self.functions_in_sequences:
                    self.functions_in_sequences.append(func)

    def receive_data_from_static_analysis(self,static_analysis_data:dict):
        self.state_variables=static_analysis_data['contract_svar'][f'{self.solidity_file_name}{self.contract_name}']
        self.state_variables_in_integer=static_analysis_data['contract_svar_in_int'][f'{self.solidity_file_name}{self.contract_name}']
        self.function_reads_writes=static_analysis_data['contract_function_r_w'][f'{self.solidity_file_name}{self.contract_name}']
        self.function_reads_writes_in_integer=static_analysis_data['contract_function_r_w_in_int'][f'{self.solidity_file_name}{self.contract_name}']
        print(f'\n function reads and writes from static analysis')
        for k,v in self.function_reads_writes.items():
            print(f'{k}:{v}')
        print(f'\n function reads and writes(integers) from static analysis')
        for k,v in self.function_reads_writes_in_integer.items():
            print(f'{k}:{v}')
    