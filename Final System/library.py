import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

import smtplib # Used to send email. 
from email.mime.multipart import MIMEMultipart # Used to create the message of the email. 
from email.mime.text import MIMEText # Used to create the message of the email. 

import sqlite3

import permission_classes

import matplotlib.pyplot as plt

import numpy as np

from tkcalendar import DateEntry

import matplotlib.ticker as ticker

from datetime import datetime

import os

import shutil

from datetime import datetime, timedelta, time

def reminder_email():
    '''This will check for any bookings which are 1 week away (7 days) and send
       a reminder email to them with the details of the booking'''
    with sqlite3.connect("Hotel_Management_System.db") as db:
        cursor = db.cursor()
        cursor.execute("select * from Booking") 
        records=cursor.fetchall()
        db.commit()

    today = datetime.today()
    week_from_today = datetime.combine(today, time.min)  + timedelta(days=7)

    for record in records:
        data = list(record)
        check_in = datetime.strptime(data[2],"%d/%m/%Y")
        if check_in == week_from_today:
            with sqlite3.connect("Hotel_Management_System.db") as db:
                cursor = db.cursor()
                cursor.execute("select room_number from Room where RoomID = {0}".format(data[4]))
                room_number = cursor.fetchone()
                cursor.execute("select email from Customer where CustomerID = {0}".format(data[9]))
                reciever = cursor.fetchone()
                db.commit()
            room_number = room_number[0]
            reciever = reciever[0]
                
            sender = "hoteltestemail1030@gmail.com"
            subject = "Booking Confirmation"
            password_of_sender = "Hotel123!"

            body = ("""
            <html>
                <body>
                    <p>Hello,
                       This is a reminder that you have a booking with us next week.
                       The details are as follows:</p>
                    <p>Number of guests = %s</p>
                    <p>Check in date = %s</p>
                    <p>Check out date = %s</p>
                    <p>Room Number = %s</p>
                    <p>Holiday Type = %s</p>
                    <p>Price = %s</p>
                    <p>Date of booking = %s</p>
                    <p>Offer code = %s</p>
                    <p>Thank you for booking your holiday with us. We can't wait to see you.</p>
                    <p>Yours Sincerely,</p>
                    <p>Hotel</p>
                </body>
            </html>
            """ % (data[1],data[2],data[3],str(room_number),data[5],data[6],data[7],data[8]))
            try:
                email(sender,reciever,body,subject,password_of_sender)
            except TimeoutError:
                pass

def clear_frame_or_window(window): # window is either a frame or tk.Tk().
    '''This clears the window'''
    for widget in window.winfo_children(): # itearates through a list of all the tk widgets in the window.
        widget.destroy()

def make_tview(column_names,data,root):
        '''This will create a treeview for a particular table in a database and populate it'''
        
        ## creating the tview.
        tview=ttk.Treeview(root)
        columns = []
        for i in range(len(column_names)):
            slot = "SLOT_{0}".format(i)
            columns.append(slot) # This is used to give the columns headings.
            tview["columns"]=(columns)
            tview["show"]="headings" #This hides column 0.
            tview.column(slot)
            
        for i in range(len(columns)):
            tview.heading("SLOT_{0}".format(i),text=create_space(column_names[i])) # Will name each column by their respective field name. 

        ## creating both the horizontal scroll bar and vertical scroll bar.
        vsb=ttk.Scrollbar(root, orient="vertical", command=tview.yview)
        vsb.configure(cursor='arrow')
        vsb.pack(side="right",fill="y")

        hsb=ttk.Scrollbar(root, orient="horizontal", command=tview.xview)
        hsb.configure(cursor='arrow')
        hsb.pack(side="bottom",fill="x")

        tview.configure(yscrollcommand=vsb.set)
        tview.configure(xscrollcommand=hsb.set)

        root.configure(cursor='pencil')

        tview.delete(*tview.get_children())

        for i in data:
            tview.insert("","end",values=i)
        tview.pack()
        
def get_record(tview): # tview needs to be an instance of a treeview. 
    '''This will return the data in a selected record.
       This works if MORE than one record can be selected. (used for delation of multiple records)'''
    focused=tview.selection() # this returns a list of the index values of the string. 
    records=[]
    if focused != "": # This prevents an error if nothing has been selected.
        for i in focused:
            index_value=str(i)[1:]# This disreagrds the first character of a string.
            index_value=int(index_value,16)# This changes the hex number into decimal.
            for child in tview.get_children():
                tview_index=str(child)[1:]
                tview_index=int(tview_index,16)
                if tview_index==index_value:
                    record = tview.item(child)["values"] # gets the data stored in the specific row in the tveiw. 
            records.append(record)
        return records # returns a 2d array.

def delete_item(tview,fields,db_name,table,primary_key_name):
    '''This will delete a selected record'''
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
            if messagebox.askyesno("Delete","Are you sure you want to delete {0}?".format(record)): # asks the user if they are sure. 
                sql="delete from {1} where {2}={0}".format(str(primary_key),table,primary_key_name)
                cursor.execute(sql)
        refresh(tview,db_name,table) # will re-populate the tview to show changes.


def edit_item(tview,data,table,db_name,primary_key_name,fields,record,clss):
    '''This will edit a selected item'''
    fields=create_lst(fields)
    sql_code_for_fields=""
    for i in range(len(fields)):
        sql_code_without_coma=fields[i]+"=?"
        sql_code_for_fields=sql_code_for_fields+sql_code_without_coma
        try:
            rogue_value=fields[i+1]
            sql_code_for_fields=sql_code_for_fields+","
        except:
            next
            
    primary_key=record[0] # The reason it is here is because it needs to have the original index value (i.e before the record is editied).
    
    with sqlite3.connect(db_name) as db:
        cursor=db.cursor()
        cursor.execute("select * from {1} where {2}={0}".format(str(primary_key),table,primary_key_name))#This is for the dialogue box.
        record=cursor.fetchone()
        edited_record=str(primary_key),data
        if messagebox.askyesno("Edit","Are you sure you want to edit {0} to {1}?".format(record,edited_record)):
            sql="update {2} set {1} where {3}={0}".format(str(primary_key),sql_code_for_fields,table,primary_key_name)
            data=create_lst(data)
            cursor.execute(sql,data)
        db.commit()

    if clss.__class__.__name__ == "RequestRecord":
        with sqlite3.connect(db_name) as db:
                cursor=db.cursor()
                cursor.execute("select * from {1} where {2}={0}".format(str(primary_key),table,primary_key_name))
                new_record=cursor.fetchall()
        record = list(record)
        new_record = list(new_record[0])
        clss.users_record.remove(record)
        clss.users_record.append(new_record)
        fields.insert(0,primary_key_name)
        clear_frame_or_window(clss.Treeview_Frame)
        clss.users_record.sort(key=lambda x:x[0])
        make_tview(fields,clss.users_record,clss.Treeview_Frame)
    else:
        refresh(tview,db_name,table)

def get_record1(tview):
    '''This will return the data in a selected record,
       This works if ONLY one record can be selected. (used for editing a single record)'''
    focused=tview.focus()
    if focused != "": #This prevents an error if nothing has been selected.
        index_value=str(focused)[1:]#This disreagrds the first character of a string.
        index_value=int(index_value,16)#This changes the hex number into decimal.
        for child in tview.get_children():
            tview_index=str(child)[1:]
            tview_index=int(tview_index,16)
            if tview_index==index_value:
                return tview.item(child)["values"]
    else:
        None


def insert_into_entry(ents,data): # ents and data must have the same number of elements.
    '''This will insert the data given into the entry widgets given'''
    for i in range(len(ents)):
        data[i] = str(data[i])
        try:
                ents[i].delete(0,tk.END)
                ents[i].insert(0,data[i])
        except AttributeError:
                ents[i].set(data[i])

def get_tview(root):
    '''This will return the return the tview widget within the 'root' given'''
    for widget in root.winfo_children():
        temp_widget=str(widget)
        if "treeview" in temp_widget:
            tview=widget
            break
        else:
            tview=None
    return tview

def query_maker(fields):
    '''This will create a '?' character for every element within fields'''
    fields=create_lst(fields)
    sql_code_for_fields=""
    for i in range(len(fields)):
        sql_code_without_coma="?"
        sql_code_for_fields=sql_code_for_fields+sql_code_without_coma
        if len(fields)-1 != i:
            sql_code_for_fields=sql_code_for_fields+","
    return sql_code_for_fields
    
def create_lst(data):
    '''This will create a list when given a string. If data is "a,b,c,d" then it will return ["a","b","c","d"]'''
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
    '''This will add an item to the end of the table. If the database is NOT linked to a tview the 'tview will be None' '''
    primary_key_name=str(primary_key_name)
    fields=str(fields)
    table=str(table)
    db_name=str(db_name)
    check_if_string = type(data) is str
    if check_if_string == True:
        data=create_lst(data)
    
    with sqlite3.connect(db_name) as db:
        cursor=db.cursor()
        question_marks = query_maker(fields)
        sql="insert into {0} ({1}) values ({2})".format(table,fields,question_marks)
        cursor.execute(sql,data)
        db.commit()

    
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
        if tview != None: # If it is adding to a database that is not linked to a treeview, tview will be equal to none.  
            refresh(tview,db_name,table) # An error will occur here if there is no tview linked. This is the reason for the 'if tview != None'.

        
def create_string(data):
    '''Takes a list (all elements need to be a string) as input and returns a string e.g. input=["a","b","c"] and output="a,b,c" '''
    lst_as_string = ""
    for i in range(len(data)):
        data[i] = str(data[i])
        if i != len(data):
            lst_as_string = lst_as_string+","+data[i]
    lst_as_string = lst_as_string[1:]
    return lst_as_string

def get_entry_widgets_automatic(ents):
    '''This will get thar data in the entry widgets provided'''
    data=[]
    for ent in ents:
        single_ent=ent.get()
        data.append(single_ent)
    return data

def create_drp_dwn(root, options):
    '''This will create a drop down menu with the options given'''
    var = tk.StringVar(root)
    drp_dwn_lst = tk.OptionMenu(root, var, *options)
    drp_dwn_lst.configure(cursor="hand2")
    drp_dwn_lst.pack()
    var.set(options[0])
    return var

def create_entry(root, fields):
    '''This will create an entry widget for every element in fields,
       it will also create a label with the text of the elements in fields'''
    mstr_frame=tk.Frame(root) # all the entry widgets will be in this frame
    counter=0 # counts how many groups of 5 there are (used to calculate the correct row and column the entry widgets should be placed in).
    entries = []
    for field in fields:
        row = tk.Frame(mstr_frame) 
        if fields.index(field)%5==0 and fields.index(field)!=0:
            counter=counter+1
        row.grid(row=fields.index(field)-(counter*5),column=counter,padx=5)            
        lab = tk.Label(row, width=15, text=create_space(field)+":", anchor='w')
        lab.pack()
        if field == "Check_in" or field == "Check_out" or field == "DOB":
                ent = DateEntry(row,locale="en_UK")
                ent.pack()
                entries.append(ent)
        elif field == "Allergies":
                options = ["N\A","Milk","Eggs", "Nuts","Fish","Shellfish","Fruit","Soy"]
                drp_dwn = create_drp_dwn(row, options)
                entries.append(drp_dwn)
        elif field == "Holiday_Type":
                options =  ["All inclusive", "Half-board","Full-board","Room Only"]
                drp_dwn = create_drp_dwn(row, options)
                entries.append(drp_dwn)
        elif field == "View":
                options = ["Ocean view","City view","Garden view"]
                drp_dwn = create_drp_dwn(row, options)
                entries.append(drp_dwn)
        elif field == "Job":
                options = ["Manager","Cleaner","Accountant","Receptionist"]
                drp_dwn = create_drp_dwn(row, options)
                entries.append(drp_dwn)
        elif field == "Payment_Type":
                options = ["Visa","MasterCard"]
                drp_dwn = create_drp_dwn(row, options)
                entries.append(drp_dwn)
        else:
                ent = tk.Entry(row)
                ent.pack()
                entries.append(ent)
    mstr_frame.pack()
    return entries

def refresh(tview,db_name,table):
    '''This will first delete all the records in the treeview and then add all then records in a table to the treeview'''
    table=str(table)
    db_name=str(db_name)
    tview.delete(*tview.get_children())
    with sqlite3.connect(db_name) as db:
        cursor=db.cursor()
        cursor.execute("select * from {0}".format(table))
        records=cursor.fetchall()

    for record in records:
        tview.insert("","end",values=record)

def retrn_field_names(table,db_name):
    '''This will return a list of the field names of the table provided'''
    lst_of_field_names=[]
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA TABLE_INFO ({0})".format(table)) # This gets the field names, the data types and other info
        lst_of_fields_and_other_info=cursor.fetchall()
        for i in lst_of_fields_and_other_info:
            field_name=i[1] # The reason for this is because the field names are stored in element 1 in ecah tuple in the list. 
            lst_of_field_names.append(field_name)
        return lst_of_field_names

def search(db_name,table,field_name_to_search,search_item,tview,nb,clss):
    '''This will search for a record(s) within a table and display the record(s) in a tview'''
    with sqlite3.connect(db_name) as db:
        cursor=db.cursor()
        cursor.execute("select * from {1} where {2}='{0}'".format(search_item,table,field_name_to_search))#This is for the dialogue box.
        record=cursor.fetchall() # gets searched record.
        cursor.execute("select * from {0}".format(table))
        records=cursor.fetchall() # gets all records form table.
        db.commit()
        
    if record==None or record==[]:
        messagebox.showwarning("Search","Sorry, We have nothing of this criterie")
    else:
        if nb==None:
            for i in records: # allows the position of the record in the tview to be found.
                if i == record[0]:
                    position_in_tview = records.index(record[0])
                    
            ## The 3 lines below will highlight a searched ID and move 
            child_id = tview.get_children()[position_in_tview] # item is the index of the search item in the records list. 'child_id' stores the postion of the searched item in the tview. The result will be 'I0[index of list]'. 
            tview.selection_set(child_id) # this will highlight the row. 
            tview.see(child_id) # this will move the tview to that row.
        else:
                for i in nb.tabs():
                        name_of_tab = nb.tab(nb.index(i),"text")
                        if "Adv search"==name_of_tab:
                                nb.forget(i)

                adv_search_win=tk.Frame(nb,background="#d9d9d9")
                
                if clss.__class__.__name__ == "ReadAndWritePermission":
                        adv_clss = permission_classes.ReadAndWritePermission(adv_search_win,nb,table)

                if clss.__class__.__name__ == "ReadOnlyPermission":
                        adv_clss = permission_classes.ReadOnlyPermission(adv_search_win,nb,table)

                if clss.__class__.__name__ == "BookHoliday":
                        adv_clss = permission_classes.BookHoliday(adv_search_win,nb,table)

                clse_frm = tk.Frame(adv_search_win)
                cls_button=tk.Button(clse_frm,text="close",command=lambda:nb.forget(adv_search_win),background="#d9d9d9")
                cls_button.pack(anchor=tk.SE)
                clse_frm.pack(anchor=tk.SE,side="bottom")
                make_tview(retrn_field_names(table,db_name),record,adv_clss.Treeview_Frame)
                nb.add(adv_search_win,text="Adv search",underline=0)
                nb.select(adv_search_win)
            

def email(sender,reciever,body,subject,password_of_sender):
    '''This will send an email with message provided, using the gmail servers'''
    server = smtplib.SMTP('smtp.gmail.com', 587) # This is the server being used to send the emails. To find the name of the server simple google 'gmail smtp server' for gmail and 'outlook smtp server' for outlook. The second parameter used is the port used and is usually '587' for all emails.

    server.starttls() # This encrpyts the email.

    server.login(sender, password_of_sender) # Logs in to the server. The first parameter is the username and the second is the password.

    ## creating the message.
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = reciever
    msg["Subject"] = subject

    msg.attach(MIMEText(body,"html")) # this will link the body variable to the IMEMultiplart() object. The 'html' is used as the body will be in html. This can be changed to 'plain' if just text needs to be entered. 

    message = msg.as_string()
    
    server.sendmail(sender, reciever, message) # The first parameter is the sender, the second is the receiver and the thirs is the message itself.

    server.quit() # Ends the session.

def bar_chart(xaxis,yaxis):
    '''This will create a bar chart and will return an image, this image is saved within the
       same dircetory of the program'''
    y_pos = np.arange(len(xaxis)) # This is used to control the maximum value on the y-axis

    plt.bar(y_pos, yaxis, align='center', alpha=0.5)
    plt.xticks(y_pos, xaxis)
    plt.ylabel('Bookings')
    plt.title('Number of bookings per Room')

    plt.savefig('bar chart.png',transparent=True)
    plt.close()
    return 'bar chart.png'
    
def pie_chart(labels,sizes):
    '''This will create a pie chart and will return an image, this image is saved within the
       same dircetory of the program'''
    explode=[]
    mx_val = 0
    for i in sizes:
        if i > mx_val:
            mx_val=i
            idx = sizes.index(i)
        explode.append(0)

    explode[idx]=0.1

    # Plots data
    plt.pie(sizes, explode=explode, labels=labels,
    autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
        
    plt.savefig('pie chart.png',transparent=True)
    plt.close()
    return 'pie chart.png'

def gantt_chart(data, xlim): # xlim is a list that stores the lowest value at the first index and the highest value at the second index
    '''This will create a gantt chart and will return an image, this image is saved within the
       same dircetory of the program'''
    yticks = []
    yticklabels = []

    for i in data:
        yticks.append((i*10) + 5)
        yticklabels.append(i)
    yticks.sort()
    yticklabels.sort()

    ## This for loop is required as 'gnt.set_yticklabels' will only accept a list of strings
    for i in range(len(yticklabels)):
        yticklabels[i] = str(yticklabels[i])

    ## Declaring a figure "gnt"  
    fig, gnt = plt.subplots()
    
    ## Setting labels for x-axis and y-axis 
    gnt.set_xlabel('Days') 
    gnt.set_ylabel('Room')

    gnt.set_xlim(xlim)
    gnt.set_xticks(range(xlim[0],xlim[1]+1))

    gnt.xaxis.set_major_locator(ticker.MultipleLocator(5))
    gnt.xaxis.set_minor_locator(ticker.MultipleLocator(1))
      
    ## Setting ticks on y-axis 
    gnt.set_yticks(yticks) 
    ## Labelling tickes of y-axis 
    gnt.set_yticklabels(yticklabels) 
    
    ## Declaring a bar in schedule
    for key, value in data.items():
        gnt.broken_barh(value, (key*10,9), facecolors =('tab:orange'))
    
    plt.savefig("gantt_chart.png",transparent=True)
    plt.close()

    return "gantt_chart.png"

def create_space(data):
    '''This will replace a '_' with a ' ' e.g. 'hello_world' will change to 'hello world' '''
    new_data = ""
    for i in data:
        if i == "_":
            i = " "
        new_data = new_data+i
    return new_data

def add_underscore(data):
    '''This will replace a ' ' with a '_' e.g. 'hello world' will change to 'hello_world' '''
    if data != None:
            new_data = ""
            for i in data:
                if i == " ":
                    i = "_"
                new_data = new_data+i
            return new_data
    else:
            return data

def encrypt(data):
    '''This will encrypt the data using a ceaser cypher, 'data' needs to be a string'''
    key=2478
    encrypted_data=""
    for i in data:
        i=ord(i)
        unicode_value=i+key
        encrypted_data=chr(unicode_value)+encrypted_data
    return encrypted_data

def decrypt(data):
    '''This decrypts the data'''
    key=2478
    encrypted_data=""
    for i in data:
        i=ord(i)
        unicode_value=i-key
        encrypted_data= chr(unicode_value)+encrypted_data
    return encrypted_data


def backup(current_date,file_to_backup,drctory_of_backup):
    '''This will create a folder called 'backup' and copy the file to this folder,
       the date of the backup will included at the end of the file name'''
    if drctory_of_backup[-7:] != "/backup":
        drctory_of_backup = drctory_of_backup+"/backup"
    try:
        os.mkdir(drctory_of_backup) # creates the folder 'backup' in the directory that is given.
    except FileExistsError:
        next

    file_to_backup_name = file_to_backup
    for i in file_to_backup_name:
        if i == "/":
            file_to_backup_name = file_to_backup_name[file_to_backup_name.index(i)+1:]
    file_to_backup_name = file_to_backup_name[:-3]

    new_file_name = drctory_of_backup + "/"  + file_to_backup_name  + " "  + str(current_date) +  ".db"

    files_in_directory = os.listdir(drctory_of_backup)
    
    shutil.copyfile(file_to_backup,
                    new_file_name) 

    ## the following code is to remove a file when there is 4 files in the directory. 
    nmber_of_files = len(files_in_directory)
    min_date = datetime(9999,12,31) ## yyyy/mm/dd
    min_file = ""
    if nmber_of_files == 4:
        for file in files_in_directory:
            date = file[-13:]
            date = datetime(int(date[6:10]),int(date[3:5]),int(date[:2]))
            if date < min_date:
                min_date = date
                min_file = file
        file_to_remove = (drctory_of_backup+"/"+"{0}").format(min_file) 
        os.remove(file_to_remove)

def get_av_salary(position):
    '''This will calculate the average salary of the 'position' given usning the data from
       the database'''
    total_salary = 0
    with sqlite3.connect("Hotel_Management_system.db") as db:
        cursor=db.cursor()
        cursor.execute("select Salary from Staff where Job = '{0}'".format(position))
        salaries=cursor.fetchall()
        db.commit()
    for salary in salaries:
        try:
            total_salary = total_salary+salary[0]
        except TypeError:
            pass
    try:
        average = total_salary/len(salaries)
    except ZeroDivisionError:
        average = 0
    return average




