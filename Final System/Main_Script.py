import tkinter as tk

from tkinter import messagebox

import sys

from main_screen_classes import *

import sqlite3

from library import *

from val_function import *

import os

import pickle

import shutil

        
def backup_periodic_pickle(file_to_backup,drctory_of_backup):
    '''This function will check when the previous backup occured and if it was over a month
       ago it will update this and then carry out the backup'''
    
    today = datetime.today() # stores todays date and time the script was run. 
    current_date = today.strftime("%d-%m-%Y") # the date is in the format 'd-m-y' and not 'd/m/y' because windows will not allow file names to contian the character '/'.
    # The line below currently is set to day for testing. to change to month change d to m. 
    current_month = today.strftime("%m") # only stores the month.
    current_month = int(current_month) # converted to int so it can be compared to 'previous_backup_month'.

    try:
        previous_backup_month= pickle.load(open("backup.p", "rb" ))
        previous_backup_month=int(previous_backup_month) # converted to int so I can add 1 to it. 
    except FileNotFoundError:
        pickle.dump(current_month,open("backup.p", "wb" )) # if the pickle file does not already exist it will create a pickle with the current date. 
        backup(current_date,file_to_backup,drctory_of_backup)

    previous_backup_month = pickle.load(open("backup.p", "rb" ))
    if previous_backup_month==12 and current_month != 12: # The reason for this is because there is no 13th month
        previous_backup_month = 0 # This is because on the next line it adds 1 to previous month
    if current_month >= previous_backup_month+1:
        pickle.dump(current_month,open("backup.p", "wb" )) # stores the current month in a pickle file called 'backup.p' in the same directory where the script is saved. 
        backup(current_date,file_to_backup,drctory_of_backup) # calls backup function.
        

class LoginScreen:
    def __init__(self, top=None):
        '''This class populates the login screen'''
        top.title("Login")

        top.resizable(False, False)
        
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font11 = "-family Arial -size 11 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        font12 = "-family Arial -size 10 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        font13 = "-family Arial -size 7 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("318x394+523+170")
        top.configure(background="#d9d9d9")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.031, rely=0.051, height=24, width=301)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font11)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Welcome to the deversorium login screen''')

        self.Label2 = tk.Label(top)
        self.Label2.place(relx=0.031, rely=0.152, height=22, width=57)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font12)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Position:''')

        self.Entry1 = tk.Entry(top)
        self.Entry1.place(relx=0.031, rely=0.406,height=20, relwidth=0.925)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.031, rely=0.228, relheight=0.063
                , relwidth=0.928)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(background="#d9d9d9")

        self.TSeparator1 = ttk.Separator(top)
        self.TSeparator1.place(relx=0.22, rely=0.178, relwidth=0.786)

        self.Label2_1 = tk.Label(top)
        self.Label2_1.place(relx=0.031, rely=0.33, height=22, width=67)
        self.Label2_1.configure(activebackground="#f9f9f9")
        self.Label2_1.configure(activeforeground="black")
        self.Label2_1.configure(background="#d9d9d9")
        self.Label2_1.configure(disabledforeground="#a3a3a3")
        self.Label2_1.configure(font="-family {Arial} -size 10")
        self.Label2_1.configure(foreground="#000000")
        self.Label2_1.configure(highlightbackground="#d9d9d9")
        self.Label2_1.configure(highlightcolor="black")
        self.Label2_1.configure(text='''Username:''')

        self.TSeparator1_2 = ttk.Separator(top)
        self.TSeparator1_2.place(relx=0.252, rely=0.355, relwidth=0.786)

        self.Label2_2 = tk.Label(top)
        self.Label2_2.place(relx=0.031, rely=0.482, height=22, width=67)
        self.Label2_2.configure(activebackground="#f9f9f9")
        self.Label2_2.configure(activeforeground="black")
        self.Label2_2.configure(background="#d9d9d9")
        self.Label2_2.configure(disabledforeground="#a3a3a3")
        self.Label2_2.configure(font="-family {Arial} -size 10")
        self.Label2_2.configure(foreground="#000000")
        self.Label2_2.configure(highlightbackground="#d9d9d9")
        self.Label2_2.configure(highlightcolor="black")
        self.Label2_2.configure(text='''Password:''')

        self.TSeparator1_3 = ttk.Separator(top)
        self.TSeparator1_3.place(relx=0.252, rely=0.508, relwidth=0.786)

        self.Entry1_4 = tk.Entry(top)
        self.Entry1_4.place(relx=0.031, rely=0.558,height=20, relwidth=0.925)
        self.Entry1_4.configure(background="white")
        self.Entry1_4.configure(disabledforeground="#a3a3a3")
        self.Entry1_4.configure(foreground="#000000")
        self.Entry1_4.configure(highlightbackground="#d9d9d9")
        self.Entry1_4.configure(highlightcolor="black")
        self.Entry1_4.configure(insertbackground="black")
        self.Entry1_4.configure(selectbackground="#c4c4c4")
        self.Entry1_4.configure(selectforeground="black")
        self.Entry1_4.configure(show="*")

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=0.252, rely=0.66, height=26, width=147)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font12)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Log In''')
        self.Button1.configure(command=lambda: self.login(var,self.Entry1,self.Entry1_4,top))

        self.Button1_5 = tk.Button(top)
        self.Button1_5.place(relx=0.786, rely=0.914, height=26, width=57)
        self.Button1_5.configure(activebackground="#ececec")
        self.Button1_5.configure(activeforeground="#000000")
        self.Button1_5.configure(background="#d9d9d9")
        self.Button1_5.configure(disabledforeground="#a3a3a3")
        self.Button1_5.configure(font="-family {Arial} -size 10")
        self.Button1_5.configure(foreground="#000000")
        self.Button1_5.configure(highlightbackground="#d9d9d9")
        self.Button1_5.configure(highlightcolor="black")
        self.Button1_5.configure(pady="0")
        self.Button1_5.configure(text='''Quit''')
        self.Button1_5.configure(command=quit_command)

        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.031, rely=0.787, height=18, width=218)
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font=font13)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(text='''If you do not have an account you can create one''')

        self.Button1_6 = tk.Button(top)
        self.Button1_6.place(relx=0.708, rely=0.791, height=13, width=22)
        self.Button1_6.configure(activebackground="#ececec")
        self.Button1_6.configure(activeforeground="#000000")
        self.Button1_6.configure(background="#d9d9d9")
        self.Button1_6.configure(disabledforeground="#a3a3a3")
        self.Button1_6.configure(font=font13)
        self.Button1_6.configure(foreground="#000000")
        self.Button1_6.configure(highlightbackground="#d9d9d9")
        self.Button1_6.configure(highlightcolor="black")
        self.Button1_6.configure(pady="0")
        self.Button1_6.configure(borderwidth='0')
        self.Button1_6.configure(text='''here''')
        self.Button1_6.configure(fg = 'blue')
        self.Button1_6.configure(cursor = 'hand2')
        self.Button1_6.configure(command=lambda: self.create_account(var,top))

        var = tk.StringVar(self.Frame1)
        positions = ["Customer","Manager","Cleaner","Accountant","Receptionist"]
        field_to_search_menu = tk.OptionMenu(self.Frame1, var, *positions)
        field_to_search_menu.configure(anchor='w')
        field_to_search_menu.configure(cursor="hand2")
        field_to_search_menu.configure(background="#d9d9d9")
        field_to_search_menu.pack(fill = tk.BOTH)
        var.set(positions[0])

        top.bind('<Return>', lambda key_pressed:self.login(var,self.Entry1,self.Entry1_4,top))

    def login(self,position,username,password,top):
        '''This function checks if the login detials that are given are valid'''
        valid = False
        position = position.get()
        username = username.get()
        password = password.get()

        font = "-family Arial -size 8 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"

        font_for_mang = "-family Arial -size 7 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"

        if position == "Customer":
            with sqlite3.connect(db_name) as db:
                cursor=db.cursor()
                cursor.execute("select * from Customer")
                customer_records=cursor.fetchall() # gets all records form table.
                db.commit()
                encryption = encrypt(password)
                for record in customer_records:
                    if record[14] == username and record[15] == encryption:
                        valid = True
                        clear_frame_or_window(top)
                        message = """This is the home screen of the hotel Management system:
-To quit simply select the quit button at the bottom left
-If you wish to return to this page at any time simply select the 'Home' button at the bottom left.
-To book a holiday just hit the 'Book' button
    -Select a room and hit the 'book' button below the table
    -In this screen you can search for a room
        -To search for a room select the search button
                -A pop-up window will appear and will prompt you for the 'ID' of the record you would like to search
        -There is an advanced search option allows you to search by any field
                -A pop-up window will appear and will prompt you to choose a field and to enter in a search term
-To retrieve your record hit the 'Request Record' button
        -To edit a record just select the record and hit edit
                -A pop-up window should appear and simply type the changes you would like to make
To view bookings hit the 'Check Booking' button
        -To edit a record just select the record and hit edit
                -A pop-up window should appear and simply type the changes you would like to make
		-When editing a booking DO NOT CHANGE THE CUSTOMERID
			-This links the booking with you and therefore if you change it then the booking is no 
			 longer made with you
		-'RoomID' is used instead of room number and therefore if you would like to change room please 
		 contact a member of staff to receive this information
		-If you would like to cancel the booking contact a member of staff
"""
                        cust = CustomerMainScreen(top,message, record)
                        cust.welcome_message(message,font)
                        break
        else:
            with sqlite3.connect(db_name) as db:
                cursor=db.cursor()
                cursor.execute("select * from Staff")
                staff_records=cursor.fetchall() # gets all records form table.
                db.commit()
                for record in staff_records:
                    encryption = encrypt(password)
                    if record[8] == username and record[9] == encryption and record[10] == position:
                        staff_records = record
                        valid = True
                        break
            if valid == True and position == "Manager":
                clear_frame_or_window(top)
                message ="""This is the home screen of the hotel Management system:
-To quit simply select the quit button at the bottom left.
-If you wish to return to this page at any time simply select the 'Home' button at the bottom left.
-To view the database in its entirety please hit the 'Database' button to the left. This will display the database with
 each tab being a table in the database.
    -In this screen you can add, edit, delete and search for each record
        -To delete a record just select the record and hit the edit button
        -To edit a record just select the record and hit edit
                -A pop-up window should appear and simply type the changes you would like to make
                -When editing the 'Staff' table do NOT use a comma in the SALARY field
        -To add a record hit the add button
                -A pop-up window should appear and simply type the record you wish to add
        -To search for a record select the search button
                -A pop-up window will appear and will prompt you for the 'ID' of the record you would like to search
        -There is an advanced search option allows you to search by any field
                -A pop-up window will appear and will prompt you to choose a field and to enter in a search term.
                -A new tab will open and with the search results. 
-When the tape chart button is selected this will show a chart of when the rooms are occupied.
-The 'Month graph' button will display a graph of number of bookings per months.
    -This is based of how many check-ins there are per month.
-The 'Room graph' button will display the number of guests per room.
-The 'Report' button will produce a report which contain:
    -The 2 graphs described above.
    -The date which the report was created. 
-More information on backups can be found when the 'Backup' button is pressed.
-To return to this screen please press 'Home'."""
                mang = ManagementMainScreen(top,message, staff_records)
                mang.welcome_message(message,font_for_mang)

            if valid == True and position == "Cleaner":
                    clear_frame_or_window(top)
                    message ="""This is the home screen of the hotel Management system:
-To quit simply select the quit button at the bottom left
-If you wish to return to this page at any time simply select the 'Home' button at the bottom left.
-To view the Room table hit the 'Room Table' button
    -In this screen you can search for a record
        -To search for a record select the search button
                -A pop-up window will appear and will prompt you for the 'ID' of the record you would like to search
        -There is an advanced search option allows you to search by any field
                -A pop-up window will appear and will prompt you to choose a field and to enter in a search term
-To retrieve your record hit the 'Request Record' button
        -To edit a record just select the record and hit edit
                -A pop-up window should appear and simply type the changes you would like to make
                -When editing the record do NOT use a comma in the SALARY field"""
                    cleaner = CleanerMainScreen(top,message, staff_records)
                    cleaner.welcome_message(message,font)

            if valid == True and position == "Receptionist":
                    clear_frame_or_window(top)
                    message ="""This is the home screen of the hotel Management system:
-To quit simply select the quit button at the bottom left
-If you wish to return to this page at any time simply select the 'Home' button at the bottom left.
-To view the database please hit the 'Check Tables' button to the left. This will display a Customer table,
 Room table and the Booking table (only access to the search and advanced search buttons)
    -In this screen you can add, edit, delete and search for each record
        -To delete a record just select the record and hit the edit button
        -To edit a record just select the record and hit edit
                -A pop-up window should appear and simply type the changes you would like to make
        -To add a record hit the add button
                -A pop-up window should appear and simply type the record you wish to add
        -To search for a record select the search button
                -A pop-up window will appear and will prompt you for the 'ID' of the record you would like to search
        -There is an advanced search option allows you to search by any field
                -A pop-up window will appear and will prompt you to choose a field and to enter in a search term
-The 'Tape Chart' button displays a chart showing the bookings within a particular month
	-Type in a year, select a month and hit 'Go' to display bookings for the time selected
-To retrieve your record hit the 'Request Record' button
        -To edit a record just select the record and hit edit
                -A pop-up window should appear and simply type the changes you would like to make
                -When editing the record do NOT use a comma in the SALARY field"""
                    recp = ReceptionistMainScreen(top,message, staff_records)
                    recp.welcome_message(message,font)

            if valid == True and position == "Accountant":
                    clear_frame_or_window(top)
                    message ="""This is the home screen of the hotel Management system:
-To quit simply select the quit button at the bottom left
-If you wish to return to this page at any time simply select the 'Home' button at the bottom left.
-To view the Bill table hit the 'Bill Table' button
    -In this screen you can search for a record
        -To search for a record select the search button
                -A pop-up window will appear and will prompt you for the 'ID' of the record you would like to search
        -There is an advanced search option allows you to search by any field
                -A pop-up window will appear and will prompt you to choose a field and to enter in a search term
-The 'Salary' button displays the average salary of each position in the hotel
-To retrieve your record hit the 'Request Record' button
        -To edit a record just select the record and hit edit
                -A pop-up window should appear and simply type the changes you would like to make
                -When editing the record do NOT use a comma in the SALARY field"""
                    accountant = AccountantsMainScreen(top,message, staff_records)
                    accountant.welcome_message(message,font)

        if valid == False:
            messagebox.showwarning("Login","Sorry, Your username or password is incorrect")
                        
    def create_account(self,position,top):
        '''This function will create a window that allows the user to creat an account'''
        position = position.get()
        if position != "Customer":
            messagebox.showwarning("Warning","As you are not a customer you cannot create an account.\nAsk your manager to create an account for you")
        else:
            top.geometry("") # This re-sets the size of the screen so it can fit the new entry widgets
            top.title("Creating an account")
            clear_frame_or_window(top)
            fields = retrn_field_names("Customer","Hotel_Management_System.db")
            fields = fields[1:]
            entry_widgets = create_entry(top,fields)
            frame=tk.Frame(top)
            frame.pack()
            add_button_new_window=tk.Button(frame,text="Add",command=lambda:adding_to_cust(entry_widgets,fields,top))
            add_button_new_window.configure(cursor='hand2')
            add_button_new_window.pack(pady=5,side=tk.LEFT)
            close_button=tk.Button(frame,text="Close",command=lambda: (clear_frame_or_window(top),LoginScreen(top)),cursor="hand2")
            close_button.pack(padx=5,side=tk.RIGHT)
            top.bind('<Return>', lambda key_pressed:adding_to_cust(entry_widgets,fields,top))
            
            ## The for loop below is to change all the widgets background to match that of the background of the 'top'
            for widget in top.winfo_children(): # itearates through a list of all the tk widgets in the window.
                if 'Frame' == widget.winfo_class():
                    for widget_in_frame in widget.winfo_children():
                        widget_in_frame.configure(background="#d9d9d9")
                        if 'Frame' == widget_in_frame.winfo_class():
                            for widget_in_frame2 in widget_in_frame.winfo_children():
                                if 'Entry' != widget_in_frame2.winfo_class():
                                    widget_in_frame2.configure(background="#d9d9d9")
                widget.configure(background="#d9d9d9")

def adding_to_cust(data,fields,top):
    '''This adds a record to the customer table and therefore creating an account'''
    data = get_entry_widgets_automatic(data)
    data.insert(0,0)
    valid = validate(fields, data,"Customer")
    data.pop(0)
    data[14] = encrypt(data[14])
    data[6] = encrypt(data[6])
    data[7] = encrypt(data[7])
    data[8] = encrypt(data[8])
    fields=create_string(fields)
    if valid==True:
        add_item(None,data,fields,"Hotel_Management_System.db","Customer","CustomerID")
        clear_frame_or_window(top)
        LoginScreen(top)
                

if __name__ == '__main__':
    root = tk.Tk()

    ## The try and except block below is to prevent the program crashing in an event to the system being unable to send an email
    try:
        reminder_email()
    except:
        pass
    
    ### The following 3 lines need to be run no matter what user uses the system as this backs-up the system.
    db_name = "Hotel_Management_System.db"
    drctory_of_backup = os.getcwd()
    backup_periodic_pickle(db_name,drctory_of_backup)

    LoginScreen(root)
    
    root.mainloop()
