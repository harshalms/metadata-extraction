import re
import docx2txt
import os
import numpy as np
import datetime

def extract_amount(data):
    pattern='(Rs|\$|RM|Php|P)\.?\s?([0-9],?\s*)+\.?([0-9]*)?(\/-)?'
    matches = re.finditer(pattern, data) 
    response = []
    for match in matches:
        start, end = match.start(), match.end()
        value = data[start : end]
        result = ([start, end], data[start:end], get_value(value))
        response.append(result)
    #print(response)
    return response
    

def get_value(value):
    pat = '([0-9],?\s*)+\.?([0-9]*)'
    v = re.search(pat, value)
    value = value[v.start() : v.end()]
    value = value.replace(" ", "")
    value = value.replace(",", "")
    return float(value)


def get_all_patern(date_list):
    day,month_number,year=date_list
    all_pattern=[]
    special_day=str(day)
    if day<10:
        day="0"+str(day)
    else:
        day=str(day)
    if month_number<10:
        month_number='0'+str(month_number)
    else:
        month_number=str(month_number)
    year=str(year)
    month=[]
    month_3_letter=[]
    for i in range(1,13):
        temp_month=datetime.date(2008, i, 1).strftime('%B')
        month.append(temp_month)
        month_3_letter.append(temp_month[:3])

    s=day+"/"+month_number+"/"+year
    p=day+"."+month_number+"."+year
    all_pattern.append(s)
    all_pattern.append(p)

    s=day+"-"+month_number+"-"+year
    all_pattern.append(s)
    s=day+" "+month[int(month_number)-1]+" "+year
    all_pattern.append(s)
    s=day+" "+month_3_letter[int(month_number)-1]+" "+year
    all_pattern.append(s)
    s=day+'/'+month[int(month_number)-1]+"/"+year
    all_pattern.append(s)
    s=day+'/'+month_3_letter[int(month_number)-1]+"/"+year
    all_pattern.append(s)
    s=day+'-'+month[int(month_number)-1]+"-"+year
    all_pattern.append(s)
    s=day+'-'+month_3_letter[int(month_number)-1]+"-"+year
    all_pattern.append(s)


    # month first
    s=month_number+"-"+day+"-"+year
    all_pattern.append(s)
    s=month[int(month_number)-1]+" "+day+" "+year
    all_pattern.append(s)
    s=month_3_letter[int(month_number)-1]+" "+day+" "+year
    all_pattern.append(s)
    s=month[int(month_number)-1]+"/"+day+"/"+year
    all_pattern.append(s)
    s=month_3_letter[int(month_number)-1]+"/"+day+"/"+year
    all_pattern.append(s)
    s=month[int(month_number)-1]+'-'+day+"-"+year
    all_pattern.append(s)
    s=month_3_letter[int(month_number)-1]+'-'+day+"-"+year
    all_pattern.append(s)
    s=special_day+'th'+' day'+' of '+month[int(month_number)-1]+" "+year

    all_pattern.append(s)
    s=special_day+'th '+month[int(month_number)-1]+" "+year
    all_pattern.append(s)

    s=day+'th'+' day'+' of '+month[int(month_number)-1]+" "+year

    all_pattern.append(s)
    s=day+'th '+month[int(month_number)-1]+" "+year
    all_pattern.append(s)
    
    return all_pattern