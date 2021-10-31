import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

import sqlite3

from library import *

from val_function import *

from datetime import datetime


root = None

def retrn_table_names(db_name): # Needs to be a string. db_name needs to be the directory of the database including the file extension '.db'. This will only work if it is a db.
    '''This will return all the table names of a database as a list'''
    lst_of_tables=[]
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select name from sqlite_master")
        lst_of_tables_in_tuple=cursor.fetchall()
        for table_name in lst_of_tables_in_tuple: # iterates through the tuple to only get the names of the tables and nothing else.
            lst_of_tables.append(table_name[0])
        return lst_of_tables # returns the names of the tables in a list.


def make_booking(db_name,ents,room,primary_key,extra_info,reciever):
    '''This will get the data from the entered in form the pop-up window
       and process this data to add to the database'''
    tview=None
    data = get_entry_widgets_automatic(ents)
    check_in = datetime.strptime(data[1],"%d/%m/%Y")
    check_out = datetime.strptime(data[2],"%d/%m/%Y")
    nights_stayed = (check_out - check_in).days
    extra_info[3] =  str(nights_stayed * float(extra_info[3]))
    
    if data[3] == 'All inclusive':
        extra_info[3] = str(float(extra_info[3]) + 150)
    elif data[3] == 'Full-Board':
        extra_info[3] = str(float(extra_info[3]) + 100)
    elif data[3] == 'Half-Board':
        extra_info[3] = str(float(extra_info[3]) + 50)

    data.insert(3,extra_info[0])
    data.insert(5,extra_info[3])
    data.insert(6,extra_info[1])
    data.insert(8,extra_info[2])

    add_data = create_string(data)
    
    booking_fields = retrn_field_names("Booking",db_name)
    booking_fields = booking_fields[1:]

    valid = validate(booking_fields,data,"Booking")
    
    booking_fields=create_string(booking_fields)

    if valid == True:
        add_item(tview,add_data,booking_fields,db_name,"Booking",primary_key)
        room_number=room[1]
        booking_email(data)


def encrypt_data(fields, data):
    '''This taked a record and will encrypt ONLY the fields that
       require encryption'''
    for field in fields:
        field_index = fields.index(field)
        data[field_index] = str(data[field_index])
        if field == "CVC_code":
            data[field_index] = encrypt(data[field_index])
        elif field == "Password":
            data[field_index] = encrypt(data[field_index])
        elif field == "Card_Number":
            data[field_index] = encrypt(data[field_index])
        elif field == "Expiry_Date":
            data[field_index] = encrypt(data[field_index])
    return data

def decrypt_data(fields, data):
    '''This taked a record and will encrypt ONLY the fields that
       require encryption'''
    for field in fields:
        field_index = fields.index(field)
        data[field_index] = str(data[field_index])
        if field == "CVC_code":
            data[field_index] = decrypt(data[field_index])
        elif field == "Password":
            data[field_index] = decrypt(data[field_index])
        elif field == "Card_Number":
            data[field_index] = decrypt(data[field_index])
        elif field == "Expiry_Date":
            data[field_index] = decrypt(data[field_index])
    return data

def insert_record_button(tview,ents,fields,db_name,table,primary_key_name,record,root,option,clss):
    '''This will process the data before adding the data to the database'''
    data = get_entry_widgets_automatic(ents)
    if record == None:
        record = [None]
    data.insert(0,record[0])
    valid = validate(fields, data,table)
    data.pop(0)
    data = encrypt_data(fields, data)
    string_data = create_string(data)
    fields=create_string(fields)
    if valid==True:
        if option==1:
            add_item(tview,string_data,fields,db_name,table,primary_key_name)
        if option==2:
            edit_item(tview,string_data,table,db_name,primary_key_name,fields,record,clss)
        root.destroy()

    if table == "Booking":
        booking_email(data)

def booking_email(data):
    '''This will first process the booking made and then send the confimation email to the user'''
    with sqlite3.connect("Hotel_Management_System.db") as db:
        cursor = db.cursor()
        cursor.execute("select * from Booking where CustomerID = {0}".format(data[8])) 
        records=cursor.fetchall()

        cursor.execute("select email,first_name from Customer where CustomerID = {0}".format(data[8]))
        customer_data = cursor.fetchone()

        cursor.execute("select room_number from Room where RoomID = {0}".format(data[3]))
        room_number = cursor.fetchone()
        db.commit()

    reciever = customer_data[0]
    frst_name = customer_data[1]
    room_number = room_number[0]

    ## The following code is to check if the data has been successfully enetered into the database.
    for record in records:
        record = list(record)
        
        for i in range(len(record)):
            record[i] = str(record[i])
            
        if record[1:] == data:
            added = True
            record_from_database = data
            break
        else:
            added = False

    if added == True:
        sender = "hoteltestemail1030@gmail.com"
        subject = "Booking Confirmation"
        password_of_sender = "Hotel123!"

        body = ("""
        <html>
            <body>
                <p>Hello %s, This email is just to confirm the detials of your booking</p>
                <p>Number of guests = %s</p>
                <p>Check in date = %s</p>
                <p>Check out date = %s</p>
                <p>Room Number = %s</p>
                <p>Holiday Type = %s</p>
                <p>Price = %s</p>
                <p>Offer Code = %s</p>
                <p>Date of booking = %s</p>
                <p>Thank you for booking your holiday with us. We can't wait to see you.</p>
                <p>If all of the above fields are empty please try booking again</p>
                <p>Yours Sincerly,</p>
                <p>Hotel</p>
            </body>
        </html>
        """ % (frst_name,record_from_database[0],record_from_database[1],record_from_database[2],str(room_number),record_from_database[4],record_from_database[5],record_from_database[7],record_from_database[6]))
        try:
            email(sender,reciever,body,subject,password_of_sender)
        except TimeoutError:
            messagebox.showerror("Time out error","The confimeation email has not been able to send.\nThe booking has still been made.")
        root.destroy()

    
def search_button_pressed(db_name,table,field_name_to_search,root,ent,tview,nb,clss):
    '''This processes the data before searching for the record in the database'''
    search_item=str(ent.get())
    if nb != None:
        field_name_to_search = field_name_to_search.get()
        field_name_to_search = add_underscore(field_name_to_search)
    field_name_to_search = add_underscore(field_name_to_search)
    search(db_name,table,field_name_to_search,search_item,tview,nb,clss)
    root.destroy()




class ReadOnlyPermission:
    def __init__(self, top=None,nb=None,table=None):
        '''This will populate a window with a search button and allows for the creation of a treeview'''

        font9 = "-family Arial -size 12 -weight normal -slant roman "  \
            "-underline 1 -overstrike 0"

        font3 = "-family Arial -size 8 -weight normal -slant roman "  \
            "-underline 1 -overstrike 0"

        self.Treeview_Frame = tk.Frame(top)
        self.Treeview_Frame.place(relx=0.017, rely=0.022, relheight=0.678, relwidth=0.975)
        self.Treeview_Frame.configure(relief='groove')
        self.Treeview_Frame.configure(borderwidth="2")
        self.Treeview_Frame.configure(relief="groove")
        self.Treeview_Frame.configure(background="#d9d9d9")

        self.Search_Button = tk.Button(top)
        self.Search_Button.place(relx=0.383, rely=0.756, height=34, width=67)
        self.Search_Button.configure(activebackground="#ececec")
        self.Search_Button.configure(activeforeground="#000000")
        self.Search_Button.configure(background="#d9d9d9")
        self.Search_Button.configure(disabledforeground="#a3a3a3")
        self.Search_Button.configure(font=font9)
        self.Search_Button.configure(foreground="#000000")
        self.Search_Button.configure(highlightbackground="#d9d9d9")
        self.Search_Button.configure(highlightcolor="black")
        self.Search_Button.configure(pady="0")
        self.Search_Button.configure(text='''Search''')
        self.Search_Button.configure(command=lambda: self.create_search_entry("Hotel_Management_System.db",nb,1,top,table))
        self.Search_Button.configure(cursor='hand2')

        self.Advanced_Search_Button = tk.Button(top)
        self.Advanced_Search_Button.place(relx=0.533, rely=0.756, height=34, width=67)
        self.Advanced_Search_Button.configure(activebackground="#ececec")
        self.Advanced_Search_Button.configure(activeforeground="#000000")
        self.Advanced_Search_Button.configure(background="#d9d9d9")
        self.Advanced_Search_Button.configure(disabledforeground="#a3a3a3")
        self.Advanced_Search_Button.configure(font=font3)
        self.Advanced_Search_Button.configure(foreground="#000000")
        self.Advanced_Search_Button.configure(highlightbackground="#d9d9d9")
        self.Advanced_Search_Button.configure(highlightcolor="black")
        self.Advanced_Search_Button.configure(pady="0")
        self.Advanced_Search_Button.configure(text='''Advanced\nSearch''')
        self.Advanced_Search_Button.configure(command=lambda: self.create_search_entry("Hotel_Management_System.db",nb,2,top,table))
        self.Advanced_Search_Button.configure(cursor='hand2')

    def create_treeview(self,db_name,table): # db_name needs to be a string. table needs to be a string
        '''This will create a treeview for a particular table in a database and populate the treeview'''
        column_names = retrn_field_names(table,db_name) # gets the field names from the table

        with sqlite3.connect(db_name) as db:
            cursor=db.cursor()
            cursor.execute("select * from {0}".format(table))
            records=cursor.fetchall()
            
        if self.__class__.__name__ == "BookHoliday" and table == "Room":
            column_names.remove("RoomID")
            column_names.remove("Room_TypeID")
            column_names.remove("Staff_RoomID")
            
            for record in records:
                lst_record = list(record) # Converts record into list as you cannot use .pop() on tuples
                lst_record.pop(0) # Removes RoomID
                lst_record.pop(2) # Removes Room_TypeID
                lst_record.pop(7) # Removes Staff_RoomID
                lst_record = tuple(lst_record) # converts the record to be added into records back into tuple
                ## Next 2 lines replace the old record with the new record
                records.insert(records.index(record),lst_record) 
                records.remove(record)
        
        make_tview(column_names,records,self.Treeview_Frame)

    def create_search_entry(self,db_name,nb,option,top,table): # db_name needs to be a string. nb can be an instance of a notebook or None. table needs to be a string or None only if nb has been passed an instance of a notebook.
        '''This creates a new window with an entry widget and a search button'''
        global root

        try:
            root.destroy()
        except:
            pass
        
        root=tk.Tk()
        root.resizable(False, False)

        if table == None:
            table = nb.tab(nb.index("current"),"text") # This will return the table name getting the name of the tab. from 'https://stackoverflow.com/questions/14000944/finding-the-currently-selected-tab-of-ttk-notebook'    

        if nb.tab(nb.index("current"),"text") == "Adv search":
            nb.forget(nb.index("current"))

        table=add_underscore(table)
        root.title("Searching the {0} table".format(table))

        fields = retrn_field_names(table,db_name)
        for i in range(len(fields)):
            fields[i] = create_space(fields[i])
            
        primary_key_name = fields[0] # change this depending on the field to search.
        tview=get_tview(self.Treeview_Frame)
        
        if option==1:
            field_to_search_label=tk.Label(root,text=primary_key_name)
            field_to_search_label.pack()
            nb = None
            comnd = lambda: search_button_pressed(db_name,table,primary_key_name,root,ent,tview,nb,self)
            root.bind('<Return>', lambda key_pressed:search_button_pressed(db_name,table,primary_key_name,root,ent,tview,nb,self)) 

        if option==2:
            var = tk.StringVar(root)
            field_to_search_menu = tk.OptionMenu(root, var, *fields)
            field_to_search_menu.configure(cursor="hand2")
            field_to_search_menu.pack()
            var.set(fields[0])
            comnd = lambda: search_button_pressed(db_name,table,var,root,ent,tview,nb,self)
            root.bind('<Return>', lambda key_pressed:search_button_pressed(db_name,table,var,root,ent,tview,nb,self)) 
            
        ent = tk.Entry(root)
        ent.pack(padx=5)
        frame=tk.Frame(root)
        frame.pack()
        search_button_new_window=tk.Button(frame,text="Search",command= comnd)
        search_button_new_window.configure(cursor='hand2')
        search_button_new_window.pack(pady=5,side=tk.LEFT)
        close_button=tk.Button(frame,text="Close",command=root.destroy,cursor="hand2")
        close_button.pack(padx=5,side=tk.RIGHT)
        


        

class BookHoliday(ReadOnlyPermission):
    def __init__(self, top=None,nb=None,table=None, users_record=None):
        '''This will populate a window with everything that the 'ReadOnlyPermission' class has and and a book button'''

        font9 = "-family Arial -size 12 -weight normal -slant roman "  \
            "-underline 1 -overstrike 0"

        super().__init__(top,nb,table)

        self.users_record = users_record

        self.Book_Hol_Button = tk.Button(top)
        self.Book_Hol_Button.place(relx=0.233, rely=0.756, height=34, width=67)
        self.Book_Hol_Button.configure(activebackground="#ececec")
        self.Book_Hol_Button.configure(activeforeground="#000000")
        self.Book_Hol_Button.configure(background="#d9d9d9")
        self.Book_Hol_Button.configure(disabledforeground="#a3a3a3")
        self.Book_Hol_Button.configure(font=font9)
        self.Book_Hol_Button.configure(foreground="#000000")
        self.Book_Hol_Button.configure(highlightbackground="#d9d9d9")
        self.Book_Hol_Button.configure(highlightcolor="black")
        self.Book_Hol_Button.configure(pady="0")
        self.Book_Hol_Button.configure(text='''Book''')
        self.Book_Hol_Button.configure(command=lambda: self.book_pressed("Hotel_Management_System.db"))
        self.Book_Hol_Button.configure(cursor='hand2')

    def book_pressed(self,db_name): # db_name needs to be a string.
        '''This will populate a new window with the entry widgets for the booking table'''
        global root

        try:
            root.destroy()
        except:
            pass

        root=tk.Tk()
        root.title("Booking a holiday")
        tview=get_tview(self.Treeview_Frame)
        room=get_record1(tview)
        
        booking_fields = retrn_field_names("Booking",db_name)
        booking_fields.remove("RoomID")
        booking_fields.remove("Date_of_booking")
        booking_fields.remove("CustomerID")
        booking_fields.remove("Price")

        today = datetime.today()
        today = datetime.strftime(today,"%d/%m/%Y")
        extra_info = [room[0],today,self.users_record[0],room[2]]
        
        primary_key = booking_fields[0]
        booking_fields = booking_fields[1:] # deletes the first element in the list (the primary key).
        ents=create_entry(root, booking_fields) # creates the entry widgets.
        frame=tk.Frame(root)
        frame.pack()

        email = self.users_record[14]
        book_button=tk.Button(frame,text="Book",command=lambda:make_booking(db_name,ents,room,primary_key,extra_info,email))
        book_button.pack(side=tk.LEFT)
        close_button=tk.Button(frame,text="Close",command=root.destroy,cursor="hand2")
        close_button.pack(padx=5,side=tk.RIGHT)

        if room == None:
            root.destroy()
            tk.messagebox.showwarning("Error","You have not selected a room.")




class ReadAndWritePermission(ReadOnlyPermission):
    def __init__(self, top=None,nb=None,table=None):
        '''This will populate the window with a delete,edit and add button'''

        font9 = "-family Arial -size 12 -weight normal -slant roman "  \
            "-underline 1 -overstrike 0"

        super().__init__(top,nb,table)

        self.Edit_Button = tk.Button(top)
        self.Edit_Button.place(relx=0.683, rely=0.756, height=34, width=67)
        self.Edit_Button.configure(activebackground="#ececec")
        self.Edit_Button.configure(activeforeground="#000000")
        self.Edit_Button.configure(background="#d9d9d9")
        self.Edit_Button.configure(disabledforeground="#a3a3a3")
        self.Edit_Button.configure(font=font9)
        self.Edit_Button.configure(foreground="#000000")
        self.Edit_Button.configure(highlightbackground="#d9d9d9")
        self.Edit_Button.configure(highlightcolor="black")
        self.Edit_Button.configure(pady="0")
        self.Edit_Button.configure(text='''Edit''')
        self.Edit_Button.configure(command= lambda: self.create_entry_window("Hotel_Management_System.db",nb,2,table))
        self.Edit_Button.configure(cursor='hand2')

        self.Delete_Button = tk.Button(top)
        self.Delete_Button.place(relx=0.233, rely=0.756, height=34, width=67)
        self.Delete_Button.configure(activebackground="#ececec")
        self.Delete_Button.configure(activeforeground="#000000")
        self.Delete_Button.configure(background="#d9d9d9")
        self.Delete_Button.configure(disabledforeground="#a3a3a3")
        self.Delete_Button.configure(font=font9)
        self.Delete_Button.configure(foreground="#000000")
        self.Delete_Button.configure(highlightbackground="#d9d9d9")
        self.Delete_Button.configure(highlightcolor="black")
        self.Delete_Button.configure(pady="0")
        self.Delete_Button.configure(text='''Delete''')
        self.Delete_Button.configure(command= lambda: self.create_entry_window("Hotel_Management_System.db",nb,3,table))
        self.Delete_Button.configure(cursor='hand2')

        self.Add_Button = tk.Button(top)
        self.Add_Button.place(relx=0.083, rely=0.756, height=34, width=67)
        self.Add_Button.configure(activebackground="#ececec")
        self.Add_Button.configure(activeforeground="#000000")
        self.Add_Button.configure(background="#d9d9d9")
        self.Add_Button.configure(disabledforeground="#a3a3a3")
        self.Add_Button.configure(font=font9)
        self.Add_Button.configure(foreground="#000000")
        self.Add_Button.configure(highlightbackground="#d9d9d9")
        self.Add_Button.configure(highlightcolor="black")
        self.Add_Button.configure(pady="0")
        self.Add_Button.configure(text='''Add''')
        self.Add_Button.configure(command= lambda: self.create_entry_window("Hotel_Management_System.db",nb,1,table))
        self.Add_Button.configure(cursor='hand2')

    def create_entry_window(self,db_name,nb,option,table_name): # db_name needs to be a string. nb needs to be an instance of a Notebook. option needs to be either a 1,2 or 3. 
        '''This will populate a new window with an entry widget for each field and either an add or delete button'''
        global root

        try:
            root.destroy()
        except:
            pass
        
        record=None

        table_name=add_underscore(table_name)
        
        if table_name == None:
            table_name = nb.tab(nb.index("current"),"text") # Gets the name of the table by getting the title of the tab. From 'https://stackoverflow.com/questions/14000944/finding-the-currently-selected-tab-of-ttk-notebook'

        if nb.tab(nb.index("current"),"text") == "Adv search":
            nb.forget(nb.index("current"))

        table_name=add_underscore(table_name)       
        fields = retrn_field_names(table_name,db_name)
        primary_key_name = fields[0]
        fields = fields[1:]

        tview=get_tview(self.Treeview_Frame)
        try:
            record=get_record1(tview) # contians the primary key. This gets the selected record from the tview for edit. 
        except:
            pass
        
        if option==1:
            root = tk.Tk()
            root.resizable(False, False)
            root.title("Adding to the {0} table".format(table_name))
            entry_widgets = create_entry(root,fields)
            frame=tk.Frame(root)
            frame.pack()
            add_button_new_window=tk.Button(frame,text="Add",command=lambda:insert_record_button(tview,entry_widgets,fields,db_name,table_name,primary_key_name,record,root,1,self))
            add_button_new_window.configure(cursor='hand2')
            add_button_new_window.pack(pady=5,side=tk.LEFT)
            close_button=tk.Button(frame,text="Close",command=root.destroy,cursor="hand2")
            close_button.pack(padx=5,side=tk.RIGHT)
            root.bind('<Return>', lambda key_pressed:insert_record_button(tview,entry_widgets,fields,db_name,table_name,primary_key_name,record,root,1,self))
            
            
        if option==2 and tview!=None: # an error will occur if tview is None and it is passed to 'edit_item' through 'insert_record_button' and therefore it cannot be None.
            if record == None:
                tk.messagebox.showerror("Error","To edit a record one must be selected from the table")
            else:
                root = tk.Tk()
                root.resizable(False, False)
                root.title("Editing the {0} table".format(table_name))
                entry_widgets = create_entry(root,fields)
                entry_record = record[1:] # does not contian the primary key.

                entry_record = decrypt_data(fields, entry_record)
                
                frame=tk.Frame(root)
                frame.pack()
                insert_into_entry(entry_widgets,entry_record)
                edit_button_new_window=tk.Button(frame,text="Edit",command=lambda:insert_record_button(tview,entry_widgets,fields,db_name,table_name,primary_key_name,record,root,2,self))
                edit_button_new_window.configure(cursor='hand2')
                edit_button_new_window.pack(pady=5,side=tk.LEFT)
                close_button=tk.Button(frame,text="Close",command=root.destroy,cursor="hand2")
                close_button.pack(padx=5,side=tk.RIGHT)
                root.bind('<Return>', lambda key_pressed:insert_record_button(tview,entry_widgets,fields,db_name,table_name,primary_key_name,record,root,2,self))

        if option==3:
            delete_item(tview,fields,db_name,table_name,primary_key_name)

class RequestRecord(ReadAndWritePermission):
    def __init__(self, top=None,nb=None,table=None,users_record=None):
        '''This will populate the window with a edit button'''

        font9 = "-family Arial -size 12 -weight normal -slant roman "  \
            "-underline 1 -overstrike 0"

        super().__init__(top,nb,table)

        self.top = top

        self.users_record = users_record

        ## destroying all private attributes
        self.Add_Button.destroy()
        self.Delete_Button.destroy()
        self.Search_Button.destroy()
        self.Advanced_Search_Button.destroy()

        self.Edit_Button.place(relx=0.383, rely=0.756, height=34, width=67)

    def record_tview(self,db_name,table):
        '''This will populate the treeview with only the users_reocrd'''
        column_names = retrn_field_names(table,db_name)
        if type(self.users_record) == list:
            for i in range(len(self.users_record)):
                self.users_record[i] = list(self.users_record[i])
        else:
            self.users_record = [self.users_record]
            self.users_record[0] = list(self.users_record[0])
        make_tview(column_names,self.users_record,self.Treeview_Frame)
    

