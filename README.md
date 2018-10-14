# Temporal named entity recognizer

*MSiA 490: Text Analytics*   
**Developer: Luca Colombo**  

This program is a simple temporal named entity recognizer built using regular expressions. The program recognizes simple date expressions of two types:
1. Fixed dates (including exact time if mentioned in the expression)
2. American Federal Holidays

It is not designed to capture dates relative to a particular day ("the day before yesterday"), dates relative to temporal focus ("3 days later"), absolute dates with imprecise reference ("in the beginning of the 80s"), relative dates with special forms (seasons), basic duration ("during 3 years"), duration as interval ("from February, 11 to October, 27"), relative duration ("for a year") and temporal atom ("three days").

## Suggested steps to run the program 

1. Clone the repository.
2. (optional) Find an article you want to scan for dates and store it in the same directory.
3. (optional) Manually create a text file with all the dates that the system should recognize; this will be the ground truth.
4. Open `matcher.py`. The program is currently set up to run on the 5 news articles that are included in this repo. If you followed steps 2 and 3 and want to run the program on a new text, then update the `main()` function by adding a new line as follows

    ```
    execute_system(input_file, output_file, ground_truth_file, evaluation_file)
    ```
   where `input_file` is the file name of the file you created in point 2, `output_file` is the file name of the file where the matched dates will be store, `ground_truth_file` is the file name of the file you created in point 3 and `evaluation_file` is the file name of the file where the matching performance (using perfect match) will be stored

5. Run `matcher.py` either from the command line (`python matcher.py`) or using an IDE (for example, Spyder).
6. An output file and an evaluation file will be created with the names you specified in point 4.