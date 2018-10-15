import re

'''
We need to hardcode:
- months (fully spelled out and 3 letters abbreviations)
- days
- numbers from 01 to 31, ie days of the months with fixed lenght of 2 (leading 0 for numbers less than 10)
- numbers from 01 to 12 (same as above, but for months)
- numbers from 1 to 31 (this allows to avoid matching non-existing dates like January 35th)
- numbers from 1 to 12 (this allows to avoid matching non-existing hours like 33pm)
- holidays

Instead of having lists of these values, we store them as a long string, separated by
a pipe '|' because yhe pipe is the logical operator OR in regular expressions
'''
months_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December',
              'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'Jun.', 'Jul.',
              'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
months = '|'.join(months_list)
days_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
days = '|'.join(days_list)
nums_2digits = ['0'+str(x) for x in range(1,10)] + [str(x) for x in range(10,32)]
days_nums_2digits = '|'.join(nums_2digits)
months_nums = '|'.join(nums_2digits[0:12])
days_nums = '|'.join([str(x) for x in range(31,0,-1)]) #this needs to be backwards!!
hours_nums = '|'.join([str(x) for x in range(12,0,-1)]) #this needs to be backwards!!
holidays_list = ['New Year’s Day', 'Birthday of Martin Luther King, Jr.', 'Washington’s Birthday',
            'Memorial Day', 'Independence Day', 'Labor Day', 'Columbus Day', 'Veterans Day',
            'Thanksgiving Day', 'Christmas Day']
holidays = '|'.join(holidays_list)

   

def match_dow(text, output):
    #this picks up expressions of the type 'Monday' or 'late Monday afternoon'
    #to avoid double counting, we need to make sure we do not pick up expression if it would be
    #picked up by another function
    #we use negative lookahead to fix this issue
    #example: the function does not pick up expressions followed by a time like 'Wednesday, 2pm'
    match = re.finditer(r'((early |late )?(%s)( afternoon| morning| evening| night)?(?!, (%s))(?!, (%s)(am|pm|a.m.|p.m.))(?! (%s)(am|pm|a.m.|p.m.)))' %(days, months, hours_nums, hours_nums), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_dow_the_dom(text, output):
    #this picks up expressions of the type 'Monday the 1st' and 'Monday the 1'
    match = re.finditer(r'((%s)( the (%s)(th|st|nd|rd)?))' %(days, days_nums), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_days_with_time(text, output):
    #this picks up expressions of the type 'Tuesday, 8pm' or 'Monday 6 a.m.' or '11 pm EST'
    #we use negative lookbehind to avoid overlap with another regex defined below
    #this does not match anything that is preceded by ':'
    #if not, when we have 11:10 am, the regex would pick up '10 am'
    match = re.finditer(r'((?<!\d:)((%s) )?((%s), )?(%s)( )?(am|pm|a.m.|p.m.)( EST| ET| CST| CT| PST| PT| MST| MT)?)' %(days, days, hours_nums), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_dates_slashes(text, output):
    #this picks up expressions of the type '01/01/2017'
    #I have made a first attempt at matching only valid month numbers and days numbers
    #12/35/2017 would be discarded
    #however, 2/30/2017 would be matched, even if the 30th of Feb. does not exist
    #a further improvement of this regex would validate all dates
    #picking up only dates that can be successfully parsed would be one possible approach
    #I did not pursue this because beyond the scope of the assignment
    match = re.finditer(r'((%s)/(%s)/\d{4})' %(months_nums,days_nums_2digits), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_month_day(text, output):
    #this picks up expressions of the type 'August 24th, 2014' or 'Monday, September 3rd'
    #also picks up exact time in expressions like 'August 28, 2018 10:10 am ET'
    match = re.finditer(r'(((%s), )?(%s) \d+(th|st|nd|rd)?(, \d{4})?( )?((%s))?(:\d+)?( )?(am|pm|a.m.|p.m.)?( EST| ET| CST| CT| PST| PT| MST| MT)?)' %(days, months,hours_nums), text)
    for x in match:
        output.append(x.group(0).strip())
    return output


def match_day_of_month(text, output):
    #this picks up expressions of the type 'the 4th of July'
    match = re.finditer(r'(the (%s)(th|st|nd|rd)? of (%s))' %(days_nums, months), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_months(text, output):
    #this picks up expressions of the type 'late January'
    #need to watch out for double counting!!
    #use positive lookbehind and only match if expression preceded by 'in' or 'since'
    match = re.finditer(r'(((?<=in )|(?<=since ))(late |early )?(%s))' % (months), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_years(text, output):
    #this picks up '2018' from expressions of the type 'in 2018' and 'in 2017 and 2018'
    match = re.finditer(r'((?<=in )|(?<=the )|(?<=since )|(?<=in \d{4} and ))\d{4}', text)
    for x in match:
        output.append(x.group(0))
    return output


def match_hours(text, output):
    #this picks up expressions of the type '4:50 pm'
    #need to make sure this does not double count hours that are part of a long
    #string that also contains a date
    #use negative lookbehind to stop double counting
    match = re.finditer(r'((?<!\d )(%s):\d+( )?(am|pm|a.m.|p.m.)( EST| ET| CST| CT| PST| PT| MST| MT)?)' % (hours_nums), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_holidays(text, output):
    #this picks up holidays
    #holidays are defined in the list at the top of this script
    match = re.finditer(r'((%s))' %(holidays), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_all(text, output):
    #this is a function that calls all previously defined regex matchers
    #notice that all 'matching' functions take a list as input, add the expressions they
    #matched to that list and then return the list
    #the best way to use match_all is to give it an empty list in the 'output' parameter
    #it will return the list with all matched strings from all the matching functions
    output = match_dow(text, output)
    output = match_dow_the_dom(text, output)
    output = match_days_with_time(text, output)
    output = match_dates_slashes(text, output)
    output = match_month_day(text, output)
    output = match_day_of_month(text, output)
    output = match_months(text, output)
    output = match_years(text, output)
    output = match_hours(text, output)
    output = match_holidays(text, output)
    return output


def compute_performance(labels, output_list, evaluation_file):
    #function to compute performance of the program using perfect match
    #it computes true positives, false positives and false negatives
    #it then uses TP, FP and FN to compute precision, recall and F1 score
    #it then writes all this information in a file names as per the evaluation_file parameter
    TP = 0
    FP = 0
    FN = 0
    for truth in labels:
        if truth in output_list:
            TP += 1
        else:
            FN += 1
            
    for prediction in output_list:
        if prediction not in labels:
            FP += 1
            
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    F1 = 2*precision*recall / (precision+recall)
    
    with open(evaluation_file, 'w') as file:
        file.write('True Positives: {}\n'.format(TP))
        file.write('False Positives: {}\n'.format(FP))
        file.write('False Negatives: {}\n'.format(FN))
        file.write('Precision: {}\n'.format(precision))
        file.write('Recall: {}\n'.format(recall))
        file.write('F1 score: {}\n'.format(F1))
  

def labels_sorter(file_name):
    #sort labels in the file with ground truth
    #this function is only useful during the development of the program
    #once labels have been sorted, opening output and ground truth side by side in a
    #text editor allows to immediately see what expressions have been matched and
    #what have not
    with open(file_name, 'r') as f:
        text_input = f.read().splitlines()
        
    text_input.sort()

    with open(file_name, 'w') as output:
        for x in text_input:
            output.write(x + '\n')