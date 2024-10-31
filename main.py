from structure import Structure


def read_input():
    with open('input.txt', 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines.copy()]
        return lines
    
def build_dictionary(lines):
    
    dictionary = {}
    
    itemset_ID = 0
    for line in lines:
        list = tuple(line.split(','))
        dictionary[itemset_ID] = list
        itemset_ID += 1
        
    return dictionary


if __name__ == '__main__':
    while True:
        threshold = input("Insert the Threshold: ")
        try:
            threshold = int(threshold)
            break
        except:
            print("Invalid Output")
            continue
    
    lines = read_input()
    data = build_dictionary(lines)
    struc = Structure(data, threshold)
    struc.print_data_table()
    struc.start_algorithm()
    # struc.output_walls()