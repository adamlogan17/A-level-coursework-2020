import sys

import tkinter as tk

from tkinter import messagebox

import tkinter.ttk as ttk

from read_only_class import *

def clear_frame_or_window(window): # window is either a frame or tk.Tk().
    """This clears the window."""
    for widget in window.winfo_children(): # itearates through a list of all the tk widgets in the window.
        widget.destroy()

def retrn_table_names(db_name): # Needs to be a string. db_name needs to be the directory of the database including the file extension '.db'. This will only work if it is a db.
    """This will return all the table names of a database as a list."""
    lst_of_tables=[]
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select name from sqlite_master")
        lst_of_tables_in_tuple=cursor.fetchall()
        for table_name in lst_of_tables_in_tuple: # iterates through the tuple to only get the names of the tables and nothing else.
            lst_of_tables.append(table_name[0])
        return lst_of_tables # returns the names of the tables in a list.
    
class MainMenu:
    def __init__(self, top=None):
        '''This class poipulates the template of all the other classes.'''
        
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font14 = "-family Arial -size 10 -weight bold -slant roman "  \
            "-underline 1 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("684x450+283+165")
        top.title("Hotel Management System")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.TSeparator1 = ttk.Separator(top)
        self.TSeparator1.place(relx=0.132, rely=-0.044, relheight=1.711)
        self.TSeparator1.configure(orient="vertical")

        self.TSeparator2 = ttk.Separator(top)
        self.TSeparator2.place(relx=-0.058, rely=0.244, relwidth=2.047)

        self.ImageTFrame1 = ttk.Frame(top)
        self.ImageTFrame1.place(relx=-0.029, rely=-0.044, relheight=0.278
                , relwidth=0.154)
        self.ImageTFrame1.configure(borderwidth="2")

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Quit_Button = tk.Button(top)
        self.Quit_Button.place(relx=0.015, rely=0.911, height=31, width=71)
        self.Quit_Button.configure(activebackground="#ececec")
        self.Quit_Button.configure(activeforeground="#000000")
        self.Quit_Button.configure(background="#d9d9d9")
        self.Quit_Button.configure(disabledforeground="#a3a3a3")
        self.Quit_Button.configure(font=font14)
        self.Quit_Button.configure(foreground="#000000")
        self.Quit_Button.configure(highlightbackground="#d9d9d9")
        self.Quit_Button.configure(highlightcolor="black")
        self.Quit_Button.configure(pady="0")
        self.Quit_Button.configure(text='''Quit''')
        self.Quit_Button.configure(command=lambda:quit_command(self))

        self.Welcome_Label = tk.Label(top)
        self.Welcome_Label.place(relx=0.146, rely=0.022, height=100, width=550)
        self.Welcome_Label.configure(activebackground="#f9f9f9")
        self.Welcome_Label.configure(activeforeground="black")
        self.Welcome_Label.configure(background="#d9d9d9")
        self.Welcome_Label.configure(disabledforeground="#a3a3a3")
        self.Welcome_Label.configure(font="-family {Arial} -size 20")
        self.Welcome_Label.configure(foreground="#000000")
        self.Welcome_Label.configure(highlightbackground="#d9d9d9")
        self.Welcome_Label.configure(highlightcolor="black")
        self.Welcome_Label.configure(text='''Welcome to Deversorium''')
        self.Welcome_Label.configure(justify='center')

        self.Main_Frame = tk.Frame(top)
        self.Main_Frame.place(relx=0.142, rely=0.254, relheight=0.734
                , relwidth=0.850)
        self.Main_Frame.configure(borderwidth="2")
        self.Main_Frame.configure(background="#d9d9d9")

        def quit_command(self):
            """This will display a quit message box and if
               the user clicks yes then it will destroy the window."""
            if messagebox.askyesno("Quit","Are you sure you want to QUIT?"):
                return top.destroy()

    def get_table(self,db_name,table):
        """This method will display a table with read only permissions."""
        clear_frame_or_window(self.Main_Frame)
        read_only = ReadOnlyPermission(self.Main_Frame,table)
        read_only.create_treeview(db_name,table)
            
    def welcome_message(self,message):
        """This will display a message in the main frame."""
        label = tk.Label(self.Main_Frame,text=message,background="#d9d9d9")
        label.pack()

class ManagementMainScreen(MainMenu):
    def __init__(self,top=None):
        """This class populates the management main screen."""

        super().__init__(top) # calling parent class. 

        font11 = "-family Arial -size 8 -weight normal -slant roman "  \
            "-underline 1 -overstrike 0"
        font12 = "-family Arial -size 9 -weight normal -slant roman "  \
            "-underline 1 -overstrike 0"
        font13 = "-family Arial -size 10 -weight normal -slant roman "  \
            "-underline 1 -overstrike 0"

        ## private attribute. (destroy in all subclasses)
        self._Month_Graph_Button = tk.Button(top)
        self._Month_Graph_Button.place(relx=0.015, rely=0.444, height=31, width=71)
        self._Month_Graph_Button.configure(activebackground="#ececec")
        self._Month_Graph_Button.configure(activeforeground="#000000")
        self._Month_Graph_Button.configure(background="#d9d9d9")
        self._Month_Graph_Button.configure(disabledforeground="#a3a3a3")
        self._Month_Graph_Button.configure(font=font11)
        self._Month_Graph_Button.configure(foreground="#000000")
        self._Month_Graph_Button.configure(highlightbackground="#d9d9d9")
        self._Month_Graph_Button.configure(highlightcolor="#000000")
        self._Month_Graph_Button.configure(pady="0")
        self._Month_Graph_Button.configure(text='''Month graph''')

        ## private attribute. (destroy in all subclasses)
        self._Room_Graph_Button = tk.Button(top)
        self._Room_Graph_Button.place(relx=0.015, rely=0.533, height=31, width=71)
        self._Room_Graph_Button.configure(activebackground="#ececec")
        self._Room_Graph_Button.configure(activeforeground="#000000")
        self._Room_Graph_Button.configure(background="#d9d9d9")
        self._Room_Graph_Button.configure(disabledforeground="#a3a3a3")
        self._Room_Graph_Button.configure(font=font11)
        self._Room_Graph_Button.configure(foreground="#000000")
        self._Room_Graph_Button.configure(highlightbackground="#d9d9d9")
        self._Room_Graph_Button.configure(highlightcolor="black")
        self._Room_Graph_Button.configure(pady="0")
        self._Room_Graph_Button.configure(text='''Room graph''')

        self.Tape_Chart_Button = tk.Button(top)
        self.Tape_Chart_Button.place(relx=0.015, rely=0.356, height=31, width=71)
        self.Tape_Chart_Button.configure(activebackground="#ececec")
        self.Tape_Chart_Button.configure(activeforeground="#000000")
        self.Tape_Chart_Button.configure(background="#d9d9d9")
        self.Tape_Chart_Button.configure(disabledforeground="#a3a3a3")
        self.Tape_Chart_Button.configure(font=font12)
        self.Tape_Chart_Button.configure(foreground="#000000")
        self.Tape_Chart_Button.configure(highlightbackground="#d9d9d9")
        self.Tape_Chart_Button.configure(highlightcolor="black")
        self.Tape_Chart_Button.configure(pady="0")
        self.Tape_Chart_Button.configure(text='''Tape Chart''')
        
        ## private attribute. (destroy in all subclasses)
        self._Database_Button = tk.Button(top)
        self._Database_Button.place(relx=0.015, rely=0.267, height=31, width=71)
        self._Database_Button.configure(activebackground="#ececec")
        self._Database_Button.configure(activeforeground="#000000")
        self._Database_Button.configure(background="#d9d9d9")
        self._Database_Button.configure(disabledforeground="#a3a3a3")
        self._Database_Button.configure(font=font13)
        self._Database_Button.configure(foreground="#000000")
        self._Database_Button.configure(highlightbackground="#d9d9d9")
        self._Database_Button.configure(highlightcolor="black")
        self._Database_Button.configure(pady="0")
        self._Database_Button.configure(text='''Database''')
        self._Database_Button.configure(command=lambda:self.get_database("Hotel_Management_System.db",retrn_table_names("Hotel_Management_System.db")))
        
        ## private attribute. (destroy in all subclasses)
        self._Report_Button = tk.Button(top)
        self._Report_Button.place(relx=0.015, rely=0.622, height=31, width=71)
        self._Report_Button.configure(activebackground="#ececec")
        self._Report_Button.configure(activeforeground="#000000")
        self._Report_Button.configure(background="#d9d9d9")
        self._Report_Button.configure(disabledforeground="#a3a3a3")
        self._Report_Button.configure(font=font13)
        self._Report_Button.configure(foreground="#000000")
        self._Report_Button.configure(highlightbackground="#d9d9d9")
        self._Report_Button.configure(highlightcolor="black")
        self._Report_Button.configure(pady="0")
        self._Report_Button.configure(text='''Report''')

        ## private attribute. (destroy in all subclasses)
        self._Backup_Button = tk.Button(top)
        self._Backup_Button.place(relx=0.015, rely=0.722, height=31, width=71)
        self._Backup_Button.configure(activebackground="#ececec")
        self._Backup_Button.configure(activeforeground="#000000")
        self._Backup_Button.configure(background="#d9d9d9")
        self._Backup_Button.configure(disabledforeground="#a3a3a3")
        self._Backup_Button.configure(font=font11)
        self._Backup_Button.configure(foreground="#000000")
        self._Backup_Button.configure(highlightbackground="#d9d9d9")
        self._Backup_Button.configure(highlightcolor="#000000")
        self._Backup_Button.configure(pady="0")
        self._Backup_Button.configure(text='''Backup''')

    def get_database(self,db_name,tables):
        """This will create a notebook with each tab being a table.
           Each table has been given read and write permission."""
        clear_frame_or_window(self.Main_Frame)
        nb = ttk.Notebook(self.Main_Frame)
        ## Below is a for loop that will create a tab for each element in tables.
        for table in tables: 
            frame=tk.Frame(nb,background="#d9d9d9")
            read_write = ReadAndWritePermission(frame,nb)
            read_write.create_treeview(db_name,table)
            nb.add(frame,text=table) 
        nb.pack(expand=1,fill="both")
            

class CustomerMainScreen(MainMenu):
    def __init__(self, top=None):
        """This populates the customer's main screen"""
        
        super().__init__(top) # calling parent class.

        font14 = "-family Arial -size 10 -weight bold -slant roman "  \
                 "-underline 1 -overstrike 0"
        font15 = "-family Arial -size 7 -weight normal -slant roman "  \
                 "-underline 1 -overstrike 0"
        font16 = "-family Arial -size 6 -weight normal -slant roman "  \
                 "-underline 1 -overstrike 0"

        ## private attribute. (destroy in all subclasses)
        self._Check_Booking_Button = tk.Button(top)
        self._Check_Booking_Button.place(relx=0.015, rely=0.356, height=31, width=71)
        self._Check_Booking_Button.configure(activebackground="#ececec")
        self._Check_Booking_Button.configure(activeforeground="#000000")
        self._Check_Booking_Button.configure(background="#d9d9d9")
        self._Check_Booking_Button.configure(disabledforeground="#a3a3a3")
        self._Check_Booking_Button.configure(font=font15)
        self._Check_Booking_Button.configure(foreground="#000000")
        self._Check_Booking_Button.configure(highlightbackground="#d9d9d9")
        self._Check_Booking_Button.configure(highlightcolor="black")
        self._Check_Booking_Button.configure(pady="0")
        self._Check_Booking_Button.configure(text='''Check Booking''')

        ## private attribute. (destroy in all subclasses)
        self._Book_Button = tk.Button(top)
        self._Book_Button.place(relx=0.015, rely=0.267, height=31, width=71)
        self._Book_Button.configure(activebackground="#ececec")
        self._Book_Button.configure(activeforeground="#000000")
        self._Book_Button.configure(background="#d9d9d9")
        self._Book_Button.configure(disabledforeground="#a3a3a3")
        self._Book_Button.configure(font="-family {Arial} -size 9 -underline 1")
        self._Book_Button.configure(foreground="#000000")
        self._Book_Button.configure(highlightbackground="#d9d9d9")
        self._Book_Button.configure(highlightcolor="black")
        self._Book_Button.configure(pady="0")
        self._Book_Button.configure(text='''Book''')
        self._Book_Button.configure(command=lambda:self.book("Hotel_Management_System.db","Room"))

        self.Request_Record_Button = tk.Button(top)
        self.Request_Record_Button.place(relx=0.015, rely=0.444, height=31, width=71)
        self.Request_Record_Button.configure(activebackground="#ececec")
        self.Request_Record_Button.configure(activeforeground="#000000")
        self.Request_Record_Button.configure(background="#d9d9d9")
        self.Request_Record_Button.configure(disabledforeground="#a3a3a3")
        self.Request_Record_Button.configure(font=font16)
        self.Request_Record_Button.configure(foreground="#000000")
        self.Request_Record_Button.configure(highlightbackground="#d9d9d9")
        self.Request_Record_Button.configure(highlightcolor="black")
        self.Request_Record_Button.configure(pady="0")
        self.Request_Record_Button.configure(text='''Request Record''')

    def book(self,db_name,table):
        """This will only display the room table with a button
           that allows the user to book a holiday."""
        clear_frame_or_window(self.Main_Frame)
        book_hol = BookHoliday(self.Main_Frame,table)
        book_hol.create_treeview(db_name,table)

class CleanerMainScreen(CustomerMainScreen):
    def __init__(self, top=None):
        """This populates the cleaner's main screen."""
        
        super().__init__(top) # calling parent class.

        ## destroying all private 
        self._Check_Booking_Button.destroy()
        self._Book_Button.destroy()

        self.Room_Table_Button = tk.Button(top)
        self.Room_Table_Button.place(relx=0.015, rely=0.267, height=31, width=71)
        self.Room_Table_Button.configure(activebackground="#ececec")
        self.Room_Table_Button.configure(activeforeground="#000000")
        self.Room_Table_Button.configure(background="#d9d9d9")
        self.Room_Table_Button.configure(disabledforeground="#a3a3a3")
        self.Room_Table_Button.configure(font="-family {Arial} -size 9 -underline 1")
        self.Room_Table_Button.configure(foreground="#000000")
        self.Room_Table_Button.configure(highlightbackground="#d9d9d9")
        self.Room_Table_Button.configure(highlightcolor="black")
        self.Room_Table_Button.configure(pady="0")
        self.Room_Table_Button.configure(text='''Room Table''')
        self.Room_Table_Button.configure(command=lambda:self.get_table("Hotel_Management_System.db","Room"))

class AccountantsMainScreen(CustomerMainScreen):
    def __init__(self, top=None):
        """This populates the accountant's main screen."""
        
        super().__init__(top) # calling parent class.

        ## destroying all private 
        self._Check_Booking_Button.destroy()
        self._Book_Button.destroy()
        
        font13 = "-family Arial -size 10 -weight normal -slant roman "  \
                 "-underline 1 -overstrike 0"
        font14 = "-family Arial -size 10 -weight bold -slant roman "  \
                 "-underline 1 -overstrike 0"
        font15 = "-family Arial -size 7 -weight normal -slant roman "  \
                 "-underline 1 -overstrike 0"
        
        self.Bill_Table_Button = tk.Button(top)
        self.Bill_Table_Button.place(relx=0.015, rely=0.267, height=31, width=71)
        self.Bill_Table_Button.configure(activebackground="#ececec")
        self.Bill_Table_Button.configure(activeforeground="#000000")
        self.Bill_Table_Button.configure(background="#d9d9d9")
        self.Bill_Table_Button.configure(disabledforeground="#a3a3a3")
        self.Bill_Table_Button.configure(font="-family {Arial} -size 9 -underline 1")
        self.Bill_Table_Button.configure(foreground="#000000")
        self.Bill_Table_Button.configure(highlightbackground="#d9d9d9")
        self.Bill_Table_Button.configure(highlightcolor="black")
        self.Bill_Table_Button.configure(pady="0")
        self.Bill_Table_Button.configure(text='''Bill Table''')
        self.Bill_Table_Button.configure(command=lambda:self.get_table("Hotel_Management_System.db","Bill"))

        self.Salary_Button = tk.Button(top)
        self.Salary_Button.place(relx=0.015, rely=0.444, height=31, width=71)
        self.Salary_Button.configure(activebackground="#ececec")
        self.Salary_Button.configure(activeforeground="#000000")
        self.Salary_Button.configure(background="#d9d9d9")
        self.Salary_Button.configure(disabledforeground="#a3a3a3")
        self.Salary_Button.configure(font=font13)
        self.Salary_Button.configure(foreground="#000000")
        self.Salary_Button.configure(highlightbackground="#d9d9d9")
        self.Salary_Button.configure(highlightcolor="black")
        self.Salary_Button.configure(pady="0")
        self.Salary_Button.configure(text='''Salary''')

class ReceptionistMainScreen(CustomerMainScreen,ManagementMainScreen):
    def __init__(self, top=None):
        """This populates Receptionist's main screen"""
        
        super().__init__(top) # calling parent class.

        ## destroying all private 
        self._Check_Booking_Button.destroy()
        self._Book_Button.destroy()
        self._Month_Graph_Button.destroy()
        self._Room_Graph_Button.destroy()
        self._Database_Button.destroy()
        self._Report_Button.destroy()
        self._Backup_Button.destroy()

        font11 = "-family Arial -size 8 -weight normal -slant roman "  \
                 "-underline 1 -overstrike 0"

        self.Check_Tables_Button = tk.Button(top)
        self.Check_Tables_Button.place(relx=0.015, rely=0.267, height=31, width=71)
        self.Check_Tables_Button.configure(activebackground="#ececec")
        self.Check_Tables_Button.configure(activeforeground="#000000")
        self.Check_Tables_Button.configure(background="#d9d9d9")
        self.Check_Tables_Button.configure(disabledforeground="#a3a3a3")
        self.Check_Tables_Button.configure(font=font11)
        self.Check_Tables_Button.configure(foreground="#000000")
        self.Check_Tables_Button.configure(highlightbackground="#d9d9d9")
        self.Check_Tables_Button.configure(highlightcolor="black")
        self.Check_Tables_Button.configure(pady="0")
        self.Check_Tables_Button.configure(text='''Check Tables''')
        self.Check_Tables_Button.configure(command=lambda:self.get_database("Hotel_Management_System.db",["Room","Customer","Booking"]))
        


if __name__ == '__main__':
    root = tk.Tk()
    cust = ManagementMainScreen(root)
    message = "This is the main screen of the hotel\nManagement system."
    cust.welcome_message(message)
    root.mainloop()
