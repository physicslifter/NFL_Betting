#%%
sample_line = "13:12 - 1st), DET 64.0%"
sample_line = "7:33 - 3rd) , SEA 91.2%"
first_part, second_part = '', ''
in_first_part = True
for i in sample_line:
    if in_first_part == True:
        if i != ",":
            first_part += i
        else:
            in_first_part = False
    else:
        if i != ' ':
            second_part += i
    
at_colon = False  
minute = ''
second = '' 
quarter = 0     
on_second = False
for i in first_part:
    if at_colon == False:
        print(i, at_colon)
        if i == ':':
            at_colon = True
            on_second = True
        else:
            minute += i
    else:
        
        if on_second == True:
            if i != ' ':
                second += i
            else:
                on_second = False
        else:
            if i == '1':
                quarter = 1
            elif i == '2':
                quarter = 2
            elif i == '3':
                quarter = 3
            elif i == '4':
                quarter = 4
                    
minute = int(minute)
second = int(second)

def try_val(v):
    try:
        val = int(v)
    except:
        val = v
        
    return val

on_decimal = False
favored_team = ''
perc_main_val = ''
dec_val = ''
for i in second_part:
    if i == ' ':
        pass
    else:
        if type(try_val(i)) == str:
            if i == '.':
                on_decimal = True
            elif i == '%':
                pass
            else:
                favored_team += i
        else:
            if on_decimal == False:
                perc_main_val += i
            else:
                dec_val += i
                
dec_val = int(dec_val)
perc_main_val = int(perc_main_val)
win_prob = perc_main_val + dec_val/10
        
            
            

            
print(f'minute: {minute}, second: {second}, quarter: {quarter}')
# %%
def clean_datastring(string):
    sample_line = string
    first_part, second_part = '', ''
    in_first_part = True
    for i in sample_line:
        if in_first_part == True:
            if i != ",":
                first_part += i
            else:
                in_first_part = False
        else:
            if i != ' ':
                second_part += i
    
    at_colon = False  
    minute = ''
    second = '' 
    quarter = 0     
    on_second = False
    for i in first_part:
        if at_colon == False:
            if i == ':':
                at_colon = True
                on_second = True
            else:
                minute += i
        else:
        
            if on_second == True:
                if i != ' ':
                    second += i
                else:
                    on_second = False
            else:
                if i == '1':
                    quarter = 1
                elif i == '2':
                    quarter = 2
                elif i == '3':
                    quarter = 3
                elif i == '4':
                    quarter = 4
                    
    minute = int(minute)
    second = int(second)

    def try_val(v):
        try:
            val = int(v)
        except:
            val = v
        
        return val

    on_decimal = False
    favored_team = ''
    perc_main_val = ''
    dec_val = ''
    for i in second_part:
        if i == ' ':
            pass
        else:
            if type(try_val(i)) == str:
                if i == '.':
                    on_decimal = True
                elif i == '%':
                    pass
                else:
                    favored_team += i
            else:
                if on_decimal == False:
                    perc_main_val += i
                else:
                    dec_val += i
    #import pdb; pdb.set_trace()
    if dec_val != '':
        dec_val = int(dec_val)
        perc_main_val = int(perc_main_val)
        win_prob = perc_main_val + dec_val/10
    else:
        win_prob = int(perc_main_val)
    
    return minute, second, quarter, favored_team, win_prob
# %%
'''
Now here read in the data from the csv, clean each line and write to a new csv
'''
import csv
import numpy as np

def clean_file(filename):
    orig_name = filename
    split_name = filename.split('.')
    new_name = split_name[0]+'_CLEAN.csv'
    data = []
    with open(orig_name, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        for i, line in enumerate(reader):
            cleaned = clean_datastring(line[0])
            data.append(cleaned)
    np.savetxt(new_name,
           data,
           delimiter = ", ",
           fmt ='% s')
    

data = []
with open('SEA_DET.csv', "r") as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):
        print(line[0])
        cleaned = clean_datastring(line[0])
        print(cleaned)
        data.append(cleaned)
        print('--')
# %%
'''
now we need to:
1. convert quarter/minute/second to single usable value
2. figure out which team is the home team from web scrolling
3. Figure out how to use favored team and win pct to convert those two to single value
    a. or can do a pair of values, one for each team
4. Either approach I use, I need to figure a way to save which team is the home team and which team is initially favored
5. So write something that finds the home team on the webpage
'''