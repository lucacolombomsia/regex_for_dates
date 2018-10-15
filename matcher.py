from support import match_all, compute_performance, labels_sorter


def execute_system(input_file, output_file, labels_file, evaluation_file):
    '''Function to launch the execution of the program.

    While this function does not return any value, it creates/updates 2 text files.
    It first creates a text file with all dates that were found in the input text.
    It then creates a text file with the count of true positive, false negative and false positives
    together with precision, recall and F1 score. These values are all computed using
    perfect match.

    Args:
        input_file (str): File name of file containing the text you want to scan for dates
        output_file (str): File name of file where the matched expressions will be written
        labels_file (str): File name of file containing the ground truth, ie the dates that a perfect system would pick up
        evaluation_file (str): File name of file  where the performance evaluation will be written

    This function does not return any value.'''

    #read in the input file
    with open(input_file, 'r') as f:
        text_input = f.read()
    
    #find all the strings that match the specified regular expressions
    #we give an empty list as input and values are added to that originally empty list
    #the function the returns a list with all the expressions that matched the regular expressions
    #regex have been defined in the support.py script
    output_list = match_all(text_input, [])
    #sorting the output list makes the manual comparison of output file and ground truth
    #easier and faster
    #this is very useful during the development of the program
    #when new regex are developped by trial and error (ie to catch dates that were missed)
    output_list.sort()
    
    #write the final output in the output file
    with open(output_file, 'w') as file:
        for x in output_list:
            file.write(x + '\n')
    
    #read in the ground truth
    #this will be used to programmatically compute the performance of the program
    #notice that only perfect match evaluation is done programmatically
    #partial match evaluation should be done manually        
    with open(labels_file, 'r') as f:
        labels = f.read().splitlines()
    
    #compare output and ground truths to produce evaluation file
    compute_performance(labels, output_list, evaluation_file)

    
def main():
    #sorting the labels allows for a quicker visual comparison of ground truth
    #and output from the program
    #these function help in the development of the program, but running them is
    #definitely not a requirement for the program to work
    # labels_sorter('labels.txt')
    # labels_sorter('labels2.txt')
    # labels_sorter('labels3.txt')
    # labels_sorter('labels4.txt')
    # labels_sorter('labels5.txt')
    
    #these functions run the program on the specified input file and write the matching
    #strings into the specified output file
    #labels (ie ground truth) need to be provided for the evaluation of the system performance
    #the performance will be written to a file in the specified location
    #if you want to run this on a new text file, add a call to this function with the
    #necessary parameters; note that you would have to create a text file with the ground
    #truth so that the system performance can be evaluated against it
    execute_system('input.txt', 'output.txt', 'labels.txt', 'system-evaluation.txt')
    execute_system('input2.txt', 'output2.txt', 'labels2.txt', 'system-evaluation2.txt')
    execute_system('input3.txt', 'output3.txt', 'labels3.txt', 'system-evaluation3.txt')
    execute_system('input4.txt', 'output4.txt', 'labels4.txt', 'system-evaluation4.txt')
    execute_system('input5.txt', 'output5.txt', 'labels5.txt', 'system-evaluation5.txt')


if __name__ == "__main__":
    main()