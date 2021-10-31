from validation import *
import sqlite3
from tkinter import messagebox
from library import *
from datetime import datetime


def exist_in_table(field, data,table,db_name,record,option):
    '''Checks if the data already exists in the table given'''
    result = True
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select {0} from {1}".format(field,table)) #This gets the field names, the data types and other stuff
        records=cursor.fetchall()

    try:
        if option == 1:
            with sqlite3.connect(db_name) as db:
                cursor = db.cursor()
                cursor.execute("select * from {0}".format(table)) #This gets the field names, the data types and other stuff
                full_records=cursor.fetchall()
            record = tuple(record)
            for i in full_records:
                if i[0] == record[0]:
                    records.pop(full_records.index(i))
            if (data,) in records:
                result = False
        elif (int(data),) not in records: # A ValueError will occur here if 'data' is not a number and if this is the case the data is not valid/
            result = False
    except ValueError:
        result = False
    return result
            
def validate(fields, data, table):
    '''Validates the data given, this function checks each field and uses the correct
       validation technique coresponding to the field and returns the specific fields
       which are not valid'''
    valid = []
    data_match_fields = data[1:]
    for field in fields:
        result = None
        if table == "Customer":
            data_to_check = data_match_fields[fields.index(field)]
            if field == "Telephone_number":
                result = length_check(data_to_check,11)
            elif field == "First_name" or field == "Surname":
                result = aplha(data_to_check)
            elif field == "Address":
                result = frmt_check(data_to_check,"^\d+\s[A-z]+\s[A-z]+$")
            elif field == "Postcode":
                result = frmt_check(data_to_check,"^(([A-Z][A-Z]{0,1})([0-9][A-Z0-9]{0,1})) {0,}(([0-9])([A-Z]{2}))$")
            elif field == "Payment_Type":
                result = lookup_check(data_to_check,["Visa","MaterCard"])
            elif field == "Card_Number":
                result = digit(data_to_check)
            elif field == "CVC_code":
                result = digit(data_to_check)
            elif field == "DOB":
                result = date_check(data_to_check)
            elif field == "City":
                result = prsnc_check(data_to_check)
            elif field == "Allergies":
                result = lookup_check(data_to_check,["N\A","Milk","Eggs", "Nuts","Fish","Shellfish","Fruit","Soy"])
            elif field == "Expiry_Date":
                result = frmt_check(data_to_check,"([0-9][0-2]|[0-9])-([0-9][0-9])$")
            elif field == "Email":
                result = frmt_check(data_to_check,"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
            elif field == "Password":
                result = frmt_check(data_to_check,"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$")
            elif field == "Username":
                result = exist_in_table("Username",data_to_check,"Customer","Hotel_Management_System.db",data,1)
            else:
                result = False
        
        elif table == "Staff":
            data_to_check = data_match_fields[fields.index(field)]
            if field == "Password":
                result = frmt_check(data_to_check,"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$")
            elif field == "Username":
                result = exist_in_table("Username",data_to_check,"Staff","Hotel_Management_System.db",data,1)
            else:
                result = True
                
        valid.append(result)
        
    if table == "Booking":
        result = True
        
        with sqlite3.connect("Hotel_Management_System.db") as db:
            cursor = db.cursor()
            cursor.execute("select Check_In,Check_Out from Booking where RoomID = {0}".format(data[3]))
            dates=cursor.fetchall()
            db.commit()

        try:
            check_in = datetime.strptime(data[1],"%d/%m/%Y")
            check_out = datetime.strptime(data[2],"%d/%m/%Y")
        except ValueError:
            check_in = datetime.strptime(data[2],"%d/%m/%Y")
            check_out = datetime.strptime(data[3],"%d/%m/%Y")            
        
        for date in dates:
            prev_check_in = datetime.strptime(date[0],"%d/%m/%Y")
            prev_check_out = datetime.strptime(date[1],"%d/%m/%Y")
                
            if prev_check_in < check_in < prev_check_out:
                result = False
            if prev_check_in < check_out < prev_check_out:
                result = False
            if check_in > check_out:
                result = False
        if result == False:
            messagebox.showwarning("Error","This room has already been booked at this time.\nPlease select a different time or room")

        return result
    
    else:
        check_valid = True
        invalid_fields = []
        for i in valid:
            if i == False:
                invalid_fields.append(fields[valid.index(i)])
                valid[valid.index(i)] = True
                check_valid = False
        if check_valid == False:
            messagebox.showwarning("Error","The following fields are invalid {0}.".format(",".join(invalid_fields)))
        return check_valid


