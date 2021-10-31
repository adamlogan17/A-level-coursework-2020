import re
import datetime

def date_check(data):
    '''This checks if the date provided is in the past, an actual date and that it is in the past'''
    date_format = '%d/%m/%Y'
    today = datetime.datetime.today() # stores todays date and time the script was run. 
    try:
      date_obj = datetime.datetime.strptime(data, date_format)
    except ValueError:
        return False
    if date_obj<today:
        return True
    else:
        return False
        
      
def range_check(data, lwr_bndry, uppr_bndry):
    '''Chacks if the data is within the range specified'''
    if data <= uppr_bndry and data >= lwr_bndry: 
        return True
    else:
        return False

def length_check(data,lngth):
    '''Checks if the data is the correct length'''
    data = str(data)
    if len(data) == lngth:
        return True
    else:
        return False

def frmt_check(data,frmt):
    '''Chacks if the data matches the format provided'''
    if re.match(frmt, data): 
        return True
    else:
        return False

def digit(data):
    '''Checks if the data is made up of digits'''
    data = str(data)
    if data.isdigit() == True:
        return True
    else:
        return False

def aplha(data):
    '''Checks if the data is made up of alphabetic characters'''
    if data.isalpha() == True:
        return True
    else:
        return False

def prsnc_check(data):
    '''Checks if data is blank''' 
    data = str(data)
    if data != "": 
        return True
    else:
        return False

def lookup_check(data,data_to_compare):
    '''Checks if data is within a list'''
    if data in data_to_compare:
        return True
    else:
        return False


