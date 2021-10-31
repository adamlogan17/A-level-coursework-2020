import sqlite3

def create_table(db_name,table_name,sql):
    
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select name from sqlite_master where name=?", (table_name,))
        cursor.execute(sql)
        db.commit()

def create_customer_table():
    sql = """create table Customer
            (CustomerID integer,
            Telephone_number integer,
            First_name string,
            Surname string,
            BookingID integer,
            BillID integer,
            Address string,
            Postcode string,
            Payment_Type string,
            Card_Number integer,
            Expiry_Date string,
            CVC_code integer,
            City string,
            Age integer,
            Allergies string,
            Email string,
            Username string,
            Password string,
            primary key(CustomerID),
            foreign key(BookingID) references Booking(BookingID),
            foreign key(BillID) references Bill(BillID))"""
    create_table(db_name, "Customer" ,sql)

def create_room_type_table():
    sql = """create table Room_Type
            (Room_TypeID integer,
            Type_of_suite string,
            Balcony boolean,
            Pets boolean,
            Price float,
            primary key(Room_TypeID))"""
    create_table(db_name, "Room_Type" ,sql)

def create_staff_table():
    sql = """create table Staff
            (StaffID integer,
            Salary float,
            Frst_name string,
            Srn_name string,
            Email string,
            Postcode string,
            DOB string,
            contact_number integer,
            Username string,
            Password string,
            Job string,
            Access_level integer,
            primary key(StaffID))"""
    create_table(db_name, "Staff" ,sql)

def create_facilities_table():
    sql = """create table Facilities
            (FacilitiesID integer,
            Minibar boolean,
            Wi_Fi boolean,
            Shower boolean,
            Safe_deposit_box boolean,
            Air_conditioning boolean,
            primary key(FacilitiesID))"""
    create_table(db_name, "Facilities" ,sql)

def create_staff_room_table():
    sql = """create table Staff_Room
            (Staff_RoomID integer,
            StaffID integer,
            RoomID integer,
            primary key(Staff_RoomID),
            foreign key(StaffID) references Staff(StaffID),
            foreign key(RoomID) references Room(RoomID))"""
    create_table(db_name, "Staff_Room" ,sql)

def create_room_facilities_table():
    sql = """create table Room_Facilities 
            (Room_FacilitiesID integer,
            FacilitiesID integer,
            RoomID integer,
            primary key(Room_FacilitiesID),
            foreign key(FacilitiesID) references Facilities(FacilitiesID),
            foreign key(RoomID) references Room(RoomID))"""
    create_table(db_name, "Room_Facilities" ,sql)

def create_room_table():
    sql = """create table Room
            (RoomID integer,
            Room_Number integer,
            Price_of_room float,
            Room_TypeID integer,
            Occupied boolean,
            Number_of_beds integer,
            Room_FacilitiesID integer,
            Floor integer,
            View string,
            Maintained boolean,
            Staff_RoomID integer,
            primary key(RoomID),
            foreign key(Room_TypeID) references Room_Type(Room_TypeID),
            foreign key(Staff_RoomID) references Staff_Room(Staff_RoomID),
            foreign key(Room_FacilitiesID) references Room_Facilities(Room_FacilitiesID))"""
    create_table(db_name, "Room" ,sql)

def create_bill_table():
    sql = """create table Bill
            (BillID integer,
            BookingID integer,
            Mini_bar_bill float,
            Main_bar_bill float,
            Restaurant_bill float, 
            Telephone_bill float,
            Spa_bill float,
            Room_service float,
            Deposit_paid boolean,
            CustomerID integer,
            Gym_fee float,
            Total_price float,
            primary key(BillID),
            foreign key(CustomerID) references Customer(CustomerID),
            foreign key(BookingID) references Booking(BookingID))"""
    create_table(db_name, "Bill" ,sql)

def create_booking_table():
    sql = """create table Booking
            (BookingID integer,
            Number_of_guests integer,
            Check_in string,
            Check_out string,
            RoomID integer,
            Holiday_Type string,
            Price float,
            Date_of_booking string,
            Offer_code string,
            primary key(BookingID),
            foreign key(RoomID) references Room(RoomID))"""
    create_table(db_name, "Booking" ,sql)
    
if __name__=="__main__":
    db_name="Hotel_Management_System.db"
    create_customer_table()
    create_room_type_table()
    create_room_facilities_table()
    create_staff_table()
    create_facilities_table()
    create_staff_room_table() 
    create_room_table()
    create_booking_table()
    create_bill_table()
