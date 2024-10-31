import math

class Structure:
    def __init__(self, data_table, threshold):
        self.data_table = data_table
        self.candidate_list = []     
        self.wall_list = []
        self.below_threshold_elements_list = [] # It contains all the subitemsets with the support < 1 -> used for the check 
        self.threshold = threshold
        self.iteration = 1
        
        
    def print_data_table(self):
        # formatting data printing
        last_key = next(reversed(self.data_table))
        multiplier = math.ceil(len(str(last_key))/4)
        remainder = len(str(last_key)) % 4
        if remainder == 0: multiplier += 1
        
        tabs = '\t' * multiplier
        
        print(f'ID{tabs}ITEMSET')
        
        for key, value in self.data_table.items():
            print(f'{key}{tabs}{value}')
        print()
            

    def start_algorithm(self):
        while True:
            check_exist = self.find_candidates_and_walls()
            if not check_exist:
                break
        
    
    def find_candidates_and_walls(self):
        if self.iteration == 1:
            #generate first candidates
            candidates_dic = {}

            # supper calculation
            for value in self.data_table.values():
                for element in value:
                    if element not in candidates_dic.keys():
                        candidates_dic[element] = 1
                    else:
                        candidates_dic[element] += 1
                        
            # sort the dictionary in descendent mode
            candidates_dic = {k: v for k, v in sorted(candidates_dic.copy().items(), key=lambda item: item[1])}
            candidates_dic = {k: candidates_dic[k] for k in reversed(candidates_dic)}
            self.candidate_list.append(candidates_dic.copy())
            self.insert_discarded_values(candidates_dic)
            candidates_dic_filtered_all = self.filtering_second(candidates_dic)
            self.wall_list.append(candidates_dic_filtered_all.copy())
                
        else:
            combination_dic = self.create_combination()
            combination_dic_first_filtered = self.filtering_first(combination_dic)
            self.candidate_list.append(combination_dic_first_filtered.copy())
            self.insert_discarded_values(combination_dic_first_filtered)
            combination_dic_filtered_all = self.filtering_second(combination_dic_first_filtered.copy())
            self.wall_list.append(combination_dic_filtered_all.copy())
        
        if len(self.wall_list[-1]) != 0:
            print(f'below: {self.below_threshold_elements_list}')
            print(f'candidate_list: {self.candidate_list[-1]}')
            print(f'wall_list: {self.wall_list[-1]}')
            print()
            
            self.iteration += 1
            return True
        
        return False
        
        
            
    
    # filtering based on the supports of the previous itemsets
    def filtering_first(self, candidates_dic):
        for tuple1 in list(candidates_dic.keys()).copy():
            for tuple2 in self.below_threshold_elements_list:
                check = all(element in tuple1 for element in tuple2)
                if check:
                    try: 
                        del candidates_dic[tuple1]
                    except:
                        candidates_dic = {}
        return candidates_dic
    
                    
    # filtering based on the supports of the new itemsets
    def filtering_second(self, candidates_dic):
        for element in list(candidates_dic.keys()).copy():
            if candidates_dic[element] <= self.threshold:
                del candidates_dic[element]
        
        return candidates_dic
        
    
    
    # It works with key as a String/tuple
    def insert_discarded_values(self, candidates_dic):
        for key in candidates_dic.keys():
            if candidates_dic[key] <= self.threshold:
                if str(type(key)) !=  "<class 'tuple'>":
                    tuple = (key)
                else:
                    tuple = key
                self.below_threshold_elements_list.append(tuple)
                
    
    def create_combination(self):
        wall_list = {}
        combination_dic = {}
        
        for key in self.wall_list[-1].keys():
            wall_list[key] = self.wall_list[-1][key]
            
        for pivot_itemset in wall_list.keys():
            for scroll_itemset in wall_list.keys():
                if pivot_itemset == scroll_itemset:
                    continue
                
                # check if the 2 tuples are different by only 1 element
                count = 0
                for element1 in pivot_itemset:
                    if element1 not in scroll_itemset:
                        count += 1
                
                if count == 1:
                    new_tuple = tuple(set(pivot_itemset) | set(scroll_itemset))
                    check = any(set(new_tuple) == set(tuple) for tuple in combination_dic.keys())
                    if not check:
                        support = 0
                        # create the support of the new_tuple
                        for root_itemset in self.data_table.values():
                            check = all(element in root_itemset for element in new_tuple)
                            if check:
                                support += 1

                            combination_dic[new_tuple] = support
                            
        return combination_dic
                        
                
                
        
        
        
            
        
    