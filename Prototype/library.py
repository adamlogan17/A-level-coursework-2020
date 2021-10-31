import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

import smtplib # Used to send email. 
from email.mime.multipart import MIMEMultipart # Used to create the message of the email. 
from email.mime.text import MIMEText # Used to create the message of the email. 

import sqlite3

def get_record(tview): # tview needs to be an instance of a treeview. 
    """This will return the data in a selected record.
       This works if MORE than one record can be selected. (use for delation of multiple records)."""
    focused=tview.selection() # this returns a list of the index values of the string. 
    records=[]
    if focused != "": # This prevents an error if nothing has been selected.
        for i in focused:
            index_value=str(i)[1:]# This disreagrds the first character of a string.
            index_value=int(index_value,16)# This changes the hex number into decimal.
            for child in tview.get_children():
                x=str(child)[1:]
                x=int(x,16)
                if x==index_value:
                    record = tview.item(child)["values"] # gets the data stored in the specific row in the tveiw. 
            records.append(record)
        return records # returns a 2d array.

def delete_item(tview,fields,db_name,table,primary_key_name):
    """This will delete a selected record."""
    ## Changes these to string values as they need to be strings. 
    primary_key_name=str(primary_key_name)
    fields=str(fields)
    table=str(table)
    db_name=str(db_name)

    records=get_record(tview) # can delete multiple records.
    for record in records: # iterates through the records that need to be deleted.
        primary_key=record[0] # gets the primary_key of the record that needs to be deleted. 
        
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute("select * from {1} where {2}={0}".format(str(primary_key),table,primary_key_name)) # gets the record to be deleted to show the user.  
            record=cursor.fetchone()
            if messagebox.askyesno("Delete","Are you sure you want to delete {0}?".format(record)): # Asks the user if they are sure. 
                sql="delete from {1} where {2}={0}".format(str(primary_key),table,primary_key_name)
                cursor.execute(sql)
        refresh(tview,db_name,table) # will re-populate the tview to show changes.


def edit_item(tview,data,table,db_name,primary_key_name,fields,record):
    """This will edit a selected item."""
    fields=create_lst(fields)
    sql_code_for_fields=""

    ## The for loop below will generate a '=?' for every field in the table to insert into the sql command. 
    for i in range(len(fields)):
        sql_code_without_coma=fields[i]+"=?"
        sql_code_for_fields=sql_code_for_fields+sql_code_without_coma
    ## The try and excepy block below is to check when the loop is one before the last iteration. This will stop a ',' character being added to the end of the string. 
        try:
            rogue_value=fields[i+1] 
            sql_code_for_fields=sql_code_for_fields+","
        except: # if any error occurs it will go to the next iteration. 
            next
            
    primary_key=record[0] # The reason it is here is because it needs to have the original index value (i.e before the record is editied).
    with sqlite3.connect(db_name) as db:
        cursor=db.cursor()
        cursor.execute("select * from {1} where {2}={0}".format(str(primary_key),table,primary_key_name)) # Gets the record before it is edited. 
        record=cursor.fetchone()
        edited_record=str(primary_key),data
        if messagebox.askyesno("Edit","Are you sure you want to edit {0} to {1}?".format(record,edited_record)): # Asks the user if they are sure. 
            sql="update {2} set {1} where {3}={0}".format(str(primary_key),sql_code_for_fields,table,primary_key_name) # Edits the record. 
            data=create_lst(data) # Turns data (which is a string) into a list. 
            cursor.execute(sql,data)
            db.commit()
    refresh(tview,db_name,table) # Will re-populate the tview to show changes.


## This works if ONLY one record can be selected. (use for editing a single record)
def get_record1(tview): # This will return the data in a selected record.
    """This subroutine will return 1 record which is selected within the tview."""
    focused=tview.focus()
    if focused != "": #T his prevents an error if nothing has been selected.
        index_value=str(focused)[1:]#T his disreagrds the first character of a string.
        index_value=int(index_value,16)#T his changes the hex number into decimal.
        for child in tview.get_children():
            x=str(child)[1:]
            x=int(x,16)
            if x==index_value:
                return tview.item(child)["values"]
    else:
        None


def insert_into_entry(ents,data): # ents and data must have the same number of elements.
    """Will insert the data into the entry widgets."""
    for i in range(len(ents)):
        ents[i].insert(0,data[i])

def get_tview(root):
    """This will return the instance of a treeview within a window."""
    for widget in root.winfo_children():
        temp_widget=str(widget)
        if "treeview" in temp_widget:
            tview=widget
            break
        else:
            tview=None
    return tview

def query_maker(fields):
    """This will create a '?' for every element within field."""
    fields=create_lst(fields)
    sql_code_for_fields=""
    for i in range(len(fields)):
        sql_code_without_coma="?"
        sql_code_for_fields=sql_code_for_fields+sql_code_without_coma
        if len(fields)-1 != i:
            sql_code_for_fields=sql_code_for_fields+","
    return sql_code_for_fields
    
def create_lst(data):
    """This will create a list when given a string. If data is "a,b,c,d" then it will return ["a","b","c","d"]."""
    lst_of_data=[]
    element_of_lst_of_data=""
    
    for i in data: #This for loop is so more than 1 field can be inserted in 1 entry box.
        if i==",":
            lst_of_data.append(element_of_lst_of_data)
            element_of_lst_of_data=""
        else:
            element_of_lst_of_data=element_of_lst_of_data+i
    lst_of_data.append(element_of_lst_of_data)
    return lst_of_data

def add_item(tview,data,fields,db_name,table,primary_key_name): 
    """This will add an item to the end of the table.
       If the database is NOT linked to a tview the 'tview will be None'.""" 
    primary_key_name=str(primary_key_name)
    fields=str(fields)
    table=str(table)
    db_name=str(db_name)
    data=create_lst(data)
    
    with sqlite3.connect(db_name) as db:
        cursor=db.cursor()
        question_marks = query_maker(fields)
        sql="insert into {0} ({1}) values ({2})".format(table,fields,question_marks)
        cursor.execute(sql,data)
        db.commit()

    if tview != None: # If it is adding to a database that is not linked to a treeview, tview will be equal to none.  
        # What is happening here is that the record has already been added. If the user clicks 'no' in the message box this will delete the added record. 
        with sqlite3.connect(db_name) as db:
            cursor=db.cursor()
            # The code below is to get the primary key of the item to be added. The reason for this is so the record can be displayed in the message box. 
            cursor.execute("select * from {0}".format(table))
            table_contents=cursor.fetchall()
            maximum=0 
            for record in table_contents:
                if record[0]>maximum:
                    maximum=record[0]
            primary_key=maximum # The maximum value is the primary key of the record to be added. 
            cursor.execute("select * from {2} where {1}={0}".format(str(primary_key),primary_key_name,table))
            record=cursor.fetchone()
            if not messagebox.askyesno("Add","Are you sure you want to add {0}?".format(record)):
                cursor.execute("delete from {2} where {1}={0}".format(str(primary_key),primary_key_name,table))
                db.commit()

    
            refresh(tview,db_name,table) # An error will occur here if there is no tview linked. This is the reason for the 'if tview != None'.


def refresh(tview,db_name,table):
    """This will first delete all the records in the treeview and then add all the records in the table to the treeview."""
    table=str(table)
    db_name=str(db_name)
    tview.delete(*tview.get_children())
    with sqlite3.connect(db_name) as db:
        cursor=db.cursor()
        cursor.execute("select * from {0}".format(table))
        records=cursor.fetchall()

    for record in records:
        tview.insert("","end",values=record)
        
def create_string(data):
    """Takes a list (all elements need to be a string) as input and returns a string.
       e.g. input=["a","b","c"] and output="a,b,c"""
    lst_as_string = ""
    for i in range(len(data)):
        data[i] = str(data[i])
        if i != len(data):
            lst_as_string = lst_as_string+","+data[i]
    lst_as_string = lst_as_string[1:]
    return lst_as_string

def get_entry_widgets_automatic(ents):
    """This will return a list of data that is contained in each of the entry widgets in the list of entry widgets."""
    data=[]
    for ent in ents:
        single_ent=ent.get()
        data.append(single_ent)
    return data

def create_entry(root, fields):
    """This will create an entry widget for every element in fields.
       It will also create a label with the text of the elements in fields."""
    entries = []
    for field in fields:
        row = tk.Frame(root) # all the entry widgets will be in this frame
        row.pack(padx=5)
        lab = tk.Label(row, width=15, text=field, anchor='w')
        ent = tk.Entry(row)
        lab.pack()
        ent.pack()
        entries.append(ent)
    return entries

def retrn_field_names(table,db_name):
    """Returns a list of the field names in a table."""
    lst_of_field_names=[]
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA TABLE_INFO ({0})".format(table)) # This gets the field names, the data types and other stuff
        lst_of_fields_and_other_stuff=cursor.fetchall()
        lst_of_fields_and_other_stuff
        for i in lst_of_fields_and_other_stuff:
            field_name=i[1] #The reason for this is because the field names are stored in element 1 in ecah tuple in the list. 
            lst_of_field_names.append(field_name)
        return lst_of_field_names

def search(db_name,table,field_name_to_search,search_item,tview):
    """Searches a table for a value.
       The record will be highlighted in the tview."""
    with sqlite3.connect(db_name) as db:
        cursor=db.cursor()
        cursor.execute("select * from {1} where {2}={0}".format(search_item,table,field_name_to_search))#This is for the dialogue box.
        record=cursor.fetchone() # gets searched record.
        cursor.execute("select * from {0}".format(table))
        records=cursor.fetchall() # gets all records form table.
        db.commit()

    if record==None:
        messagebox.showwarning("Search","This record does not exist")
    else:
        for i in records: # allows the position of the record in the tview to be found.
            if i == record:
                position_in_tview = records.index(record)
                
        ## The 3 lines below will highlight a searched ID and move the scrollbar to that record.
        child_id = tview.get_children()[position_in_tview] # item is the index of the search item in the records list. 'child_id' stores the postion of the searched item in the tview. The result will be 'I0[index of list]'. 
        tview.selection_set(child_id) # this will highlight the row. 
        tview.see(child_id) # this will move the tview to that row.

def email(sender,receiver,body,subject,password_of_sender):
    """Sends an email to the receiver."""
    server = smtplib.SMTP('smtp.gmail.com', 587) # This is the server being used to send the emails. To find the name of the server simple google 'gmail smtp server' for gmail and 'outlook smtp server' for outlook. The second parameter used is the port used and is usually '587' for all emails.

    server.starttls() # This encrpyts the email.

    server.login("js3155237@gmail.com", password_of_sender) # Logs in to the server. The first parameter is the username and the second is the password.

    ## creating the message.
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    msg.attach(MIMEText(body,"html")) # this will link the body variable to the IMEMultiplart() object. The 'html' is used as the body will be in html. This can be changed to 'plain' if just text needs to be entered. 

    message = msg.as_string()
    
    server.sendmail(sender, receiver, message) # The first parameter is the sender, the second is the receiver and the thirs is the message itself.

    server.quit() # Ends the session.    



