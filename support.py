import re

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
    #this picks up expressions of the type 'Monday'
    #to avoid double counting, need to make sure we do not pick up DOW if it would be
    #picked up by another function
    #example: t does not pick up expressions followed by a time like 'Wednesday, 2pm'
    match = re.finditer(r'((early |late )?(%s)( afternoon| morning| evening| night)?(?!, (%s))(?!, (%s)(am|pm|a.m.|p.m.))(?! (%s)(am|pm|a.m.|p.m.)))' %(days, months, hours_nums, hours_nums), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_dow_the_dom(text, output):
    #this picks up expressions of the type 'Monday the 1st' and 'Monday the 1'
    #it does not pick up expressions that are followed by a time like 'Wednesday, 2pm'
    match = re.finditer(r'((%s)( the (%s)(th|st|nd|rd)?))' %(days, days_nums), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_days_with_time(text, output):
    #this picks up expressions of the type 'Tuesday, 8pm'
    match = re.finditer(r'((?<!\d:)((%s) )?((%s), )?(%s)( )?(am|pm|a.m.|p.m.)( EST| ET| CST| CT| PST| PT| MST| MT)?)' %(days, days, hours_nums), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_dates_slashes(text, output):
    #this picks up expressions of the type '01/01/2017'
    match = re.finditer(r'((%s)/(%s)/\d{4})' %(months_nums,days_nums_2digits), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_month_day(text, output):
    #this picks up expressions of the type 'August 24th, 2014' or 'Monday, September 3rd'
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
    match = re.finditer(r'(((?<=in )|(?<=since ))(late |early )?(%s))' % (months), text)
    for x in match:
        output.append(x.group(0))
    return output


def match_years(text, output):
    #match = re.finditer(r'(?<!, )(?<!/)\d{4}', text)
    match = re.finditer(r'((?<=in )|(?<=the )|(?<=since )|(?<=in \d{4} and ))\d{4}', text)
    for x in match:
        output.append(x.group(0))
    return output


def match_hours(text, output):
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
    with open(file_name, 'r') as f:
        text_input = f.read().splitlines()
        
    text_input.sort()

    with open(file_name, 'w') as output:
        for x in text_input:
            output.write(x + '\n')