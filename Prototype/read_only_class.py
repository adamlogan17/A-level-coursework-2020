import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

import sqlite3

from library import *

def make_booking(db_name,ents,booking_fields,room,primary_key):
    """This subroutine will get all the data entered through the entry widgets and will call the subroutine which adds the booking
       to the table. This also will 'set-up' the message of the email."""
    
    """db_name needs to be a string, ents needs to be an array of instances of entry widgets, booking_fields needs to be an array of the fields in the booking table,
       room needs to be the record which was seleceted and primary_key is the primary_key of the booking table."""
    
    tview=None # This allows 'add_item' to be called without an error.
    data = get_entry_widgets_automatic(ents) # gets the data entered in through the entry widgets.
    
    ## converts the following to a tring so it can be used in the 'add_item' subroutine.
    add_data = create_string(data) 
    booking_fields=create_string(booking_fields)
    
    add_item(tview,add_data,booking_fields,db_name,"Booking",primary_key) # calls 'add_item'

    room_number=room[1] # gets the room number of the room that was selected. 
    sender = "js3155237@gmail.com" 
    reciever = "lukea496@gmail.com"
    subject = "Booking Confirmation"
    password_of_sender = "Python123!"

    ## This is the message of the email written in html.
    body = ("""
    <html>
        <body>
            <p>Hello, This email is just to confirm the detials of your booking</p>
            <p>Number of guests = %s</p>
            <p>Check in date = %s</p>
            <p>Check out date = %s</p>
            <p>Room Number = %s</p>
            <p>Holiday Type = %s</p>
            <p>Price = %s</p>
            <p>Date of boooking = %s</p>
            <p>Offer code = %s</p>
            <p>Thank you for booking your holiday with us. We can't wait to see you.</p>
            <p>If all of the above fields are empty please try booking again</p>
            <p>Yours Sincerly,</p>
            <p>Hotel</p>
        </body>
    </html>
    """ % (data[0],data[1],data[2],str(room_number),data[4],data[5],data[6],data[7]))# formats the string to enter the data of the booking. 

    email(sender,reciever,body,subject,password_of_sender) # calls 'email' which sends the email with the relevant information.

def insert_record_button(tview,ents,fields,db_name,table,primary_key_name,record,root,option): 
    """This gets the data drom the entry widegts when a button is pressed."""
    data = get_entry_widgets_automatic(ents)
    data = create_string(data)
    fields=create_string(fields)
    if option==1: # When option is 1 that means the data needs to be added to the database.
        add_item(tview,data,fields,db_name,table,primary_key_name)
    if option==2: # When option is 2 a record needs to be edited into the database. 
        edit_item(tview,data,table,db_name,primary_key_name,fields,record)
    root.destroy() # Destroys the 'pop-up' window.

def search_button_pressed(db_name,table,field_name_to_search,root,ent,tview):
    """Gets the data in the entry widgets and destroys the 'pop-up' window"""
    search_item=str(ent.get())
    search(db_name,table,field_name_to_search,search_item,tview)
    root.destroy()




class ReadOnlyPermission:
    def __init__(self, top=None,table=None,nb=None):
        '''This will populate a window with a search button and allows for the creation of a treeview.'''

        font9 = "-family Arial -size 12 -weight normal -slant roman "  \
            "-underline 1 -overstrike 0"

        self.Treeview_Frame = tk.Frame(top)
        self.Treeview_Frame.place(relx=0.017, rely=0.022, relheight=0.678, relwidth=0.975)
        self.Treeview_Frame.configure(relief='groove')
        self.Treeview_Frame.configure(borderwidth="2")
        self.Treeview_Frame.configure(relief="groove")
        self.Treeview_Frame.configure(background="#d9d9d9")

        self.Search_Button = tk.Button(top)
        self.Search_Button.place(relx=0.333, rely=0.756, height=34, width=67)
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
        self.Search_Button.configure(command=lambda: self.create_search_entry("Hotel_Management_System.db",nb,table))

    def create_treeview(self,db_name,table): # db_name needs to be a string. table needs to be a string.
        """This will create a treeview for a particular table in a database and populate it."""
        column_names = retrn_field_names(table,db_name) # gets the field names from the table.
        
        ## creating the tview.
        tview=ttk.Treeview(self.Treeview_Frame)
        columns = []
        for i in range(len(column_names)):
            slot = "SLOT_{0}".format(i)
            columns.append(slot) # This is used to give the columns headings.
            tview["columns"]=(columns)
            tview["show"]="headings" #This hides column 0.
            tview.column(slot)
            
        for i in range(len(columns)):
            tview.heading("SLOT_{0}".format(i),text=column_names[i]) # Will name each column by their respective field name. 

        ## creating both the horizontal scroll bar and vertical scroll bar.
        vsb=ttk.Scrollbar(self.Treeview_Frame, orient="vertical", command=tview.yview)
        vsb.pack(side="right",fill="y")

        hsb=ttk.Scrollbar(self.Treeview_Frame, orient="horizontal", command=tview.xview)
        hsb.pack(side="bottom",fill="x")

        tview.configure(yscrollcommand=vsb.set)
        tview.configure(xscrollcommand=hsb.set)

        refresh(tview,db_name,table) # Will populate the treeview.
        tview.pack()

    def create_search_entry(self,db_name,nb,table): # db_name needs to be a string. nb can be an instance of a notebook or None. table needs to be a string or None only if nb has been passed an instance of a notebook.
        """This creates a new window with an entry widget and a search button."""
        root=tk.Tk()
        if nb != None:
            table = nb.tab(nb.index("current"),"text") # This will return the table name ny getting the name of the tab. from 'https://stackoverflow.com/questions/14000944/finding-the-currently-selected-tab-of-ttk-notebook'
        fields = retrn_field_names(table,db_name)
        field_to_search = fields[0] # This is the field which will be used to search through. Change the number in the '[]' to select a different field.
        tview=get_tview(self.Treeview_Frame)
        field_to_search_label=tk.Label(root,text=field_to_search) 
        field_to_search_label.pack()
        ent = tk.Entry(root)
        ent.pack(padx=5) # leaves a gap of '5' both left and right of the entry widget.
        search_button_new_window=tk.Button(root,text="Search",command=lambda: search_button_pressed(db_name,table,field_to_search,root,ent,tview))
        search_button_new_window.pack()


        

class BookHoliday(ReadOnlyPermission):
    def __init__(self, top=None,table=None):
        '''This will populate a window with everything that the 'ReadOnlyPermission' class has and and a book button.'''

        font9 = "-family Arial -size 12 -weight normal -slant roman "  \
            "-underline 1 -overstrike 0"

        super().__init__(top,table,None)

        self.Book_Hol_Button = tk.Button(top)
        self.Book_Hol_Button.place(relx=0.533, rely=0.756, height=34, width=67)
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

    def book_pressed(self,db_name): # db_name needs to be a string.
        """This will populate a new window with the entry widgets for the booking table."""
        root=tk.Tk()
        tview=get_tview(self.Treeview_Frame)
        room=get_record1(tview)
        booking_fields = retrn_field_names("Booking",db_name)
        primary_key = booking_fields[0]
        booking_fields = booking_fields[1:] # deletes the first element in the list (the primary key).
        ents=create_entry(root, booking_fields) # creates the entry widgets. 
        book_button=tk.Button(root,text="Book",command=lambda:make_booking(db_name,ents,booking_fields,room,primary_key))
        book_button.pack()
        try:
            insert_into_entry([ents[3]],[room[0]]) # this will insert the primary key of the room table into the respective entry widget.
        except TypeError: # if a room is not selected this error will occur. 
            root.destroy()
            tk.messagebox.showwarning("Error","You have not selected a room.")




class ReadAndWritePermission(ReadOnlyPermission):
    def __init__(self, top=None,nb=None):
        '''This will populate the window with a delete,edit and add button.'''

        font9 = "-family Arial -size 12 -weight normal -slant roman "  \
            "-underline 1 -overstrike 0"

        super().__init__(top,None,nb)
        
        self.Edit_Button = tk.Button(top)
        self.Edit_Button.place(relx=0.733, rely=0.756, height=34, width=67)
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
        self.Edit_Button.configure(command= lambda: self.create_entry_window("Hotel_Management_System.db",nb,2))

        self.Delete_Button = tk.Button(top)
        self.Delete_Button.place(relx=0.533, rely=0.756, height=34, width=67)
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
        self.Delete_Button.configure(command= lambda: self.create_entry_window("Hotel_Management_System.db",nb,3))

        self.Add_Button = tk.Button(top)
        self.Add_Button.place(relx=0.133, rely=0.756, height=34, width=67)
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
        self.Add_Button.configure(command= lambda: self.create_entry_window("Hotel_Management_System.db",nb,1))

    def create_entry_window(self,db_name,nb,option): # db_name needs to be a string. nb needs to be an instance of a Notebook. option needs to be either a 1,2 or 3. 
        """This will populate a new window with an entry widget for each field and either an add or delete button."""
        record=None
        
        table_name = nb.tab(nb.index("current"),"text") # Gets the name of the table by getting the title of the tab. From 'https://stackoverflow.com/questions/14000944/finding-the-currently-selected-tab-of-ttk-notebook'
        fields = retrn_field_names(table_name,db_name)
        primary_key_name = fields[0]
        fields = fields[1:]

        tview=get_tview(self.Treeview_Frame)

        if option==1:
            root = tk.Tk()
            entry_widgets = create_entry(root,fields)
            add_button_new_window=tk.Button(root,text="Add",command=lambda:insert_record_button(tview,entry_widgets,fields,db_name,table_name,primary_key_name,record,root,1))
            add_button_new_window.pack()
            
        if option==2 and tview!=None: # an error will occur if tview is None and it is passed to 'edit_item' through 'inser_record_button' and therefore it cannot be None.
            root = tk.Tk()
            entry_widgets = create_entry(root,fields)
            record=get_record1(tview) # contians the primary key.
            entry_record = record[1:] # does not contian the primary key.

            insert_into_entry(entry_widgets,entry_record)
            edit_button_new_window=tk.Button(root,text="Edit",command=lambda:insert_record_button(tview,entry_widgets,fields,db_name,table_name,primary_key_name,record,root,2))
            edit_button_new_window.pack()
            
        if option==3:
            delete_item(tview,fields,db_name,table_name,primary_key_name)

    
if __name__ == '__main__':
    root = tk.Tk()
    top = ReadAndWritePermission(root)
    top.create_treeview("Hotel_Management_System.db","Booking")

