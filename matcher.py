from support import match_all, compute_performance, labels_sorter


def execute_system(input_file, output_file, labels_file, evaluation_file):
    #read in the input file
    with open(input_file, 'r') as f:
        text_input = f.read()
    
    #find all the strings that match the specified regular expressions
    output_list = match_all(text_input, [])
    output_list.sort()
    
    with open(output_file, 'w') as file:
        for x in output_list:
            file.write(x + '\n')
            
    with open(labels_file, 'r') as f:
        labels = f.read().splitlines()
        
    compute_performance(labels, output_list, evaluation_file)

    
def main():
    #labels_sorter('labels.txt')
    #labels_sorter('labels2.txt')
    #labels_sorter('labels3.txt')
    #labels_sorter('labels4.txt')
    #labels_sorter('labels5.txt')
    
    execute_system('input.txt', 'output.txt', 'labels.txt', 'system-evaluation.txt')
    execute_system('input2.txt', 'output2.txt', 'labels2.txt', 'system-evaluation2.txt')
    execute_system('input3.txt', 'output3.txt', 'labels3.txt', 'system-evaluation3.txt')
    execute_system('input4.txt', 'output4.txt', 'labels4.txt', 'system-evaluation4.txt')
    execute_system('input5.txt', 'output5.txt', 'labels5.txt', 'system-evaluation5.txt')


if __name__ == "__main__":
    main()