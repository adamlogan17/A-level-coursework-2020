- [Final System](#final-system)
		- [How do I get set up?](#how-do-i-get-set-up)
		- [Login](#login)
		- [Email](#email)
		- [Backup](#backup)
		- [Encryption/Decryption](#encryptiondecryption)
		- [Validation](#validation)
		- [Dependencies](#dependencies)

# Final System #

To start the application run 'Main_Script.py'

### How do I get set up? ###
1. Navigate to this folder, ```Final System```, within the command line
2. Execute the following commands:
   ```
   $venv\scripts\activate
   $python Main_Script.py
   ```
3. To exit the virtual environment use the command ```$deactivate```
   
Alternatively it is possible to install the dependencies yourself either by using the commands within the [Dependencies](#dependencies) section or by using the requirements.txt included within this folder (example command below) 
```
pip install -r requirements.txt
```

### Login ###
The usernames and passwords for each access level is below (rember to select the correct position!):
* Customer
  * Username = alogan123
  * Password = @Log@n123
* Manager
  * Username = manager1
  * Password = M@n@ger1
* Receptionist
  * Username = receptionist1
  * Password = Receptionist1!
* Accountant
  * Username = accountant1
  * Password = @Ccount@nt1
* Cleaner
  * Username = cleaner1
  * Password = Cle@ner1

All passwords are the same as the username except: 
* All 'a' are replaced by '@'
* If the letter 'a' does not appear in the username then a '!' is added to the end
* The first letter is a capital letter

NB:This is for ease of testing. Passwords need to be 8 letters long, including special case characters and have a capital letter. 
   They do not necessarily have to conform to the rules listed above. 

### Email ###
The email that is used to send emails is 'hoteltestemail1030@gmail.com' and the password is 'Hotel123!' (do not include the apostrophes). 
Feel free to add your own email to the database to receive emails or to replace this email within the code and use your own. 
If you are using a gmail account to send emails you may need to turn on 'Less secure apps' and the instructions to do this are below. 

At certain points this email will not be able to work as 'less secure apps' has been automatically been turned off to turn this back on follow the 
instructions below:
* Go to 'https://myaccount.google.com/lesssecureapps' and sign in using the email above
* If the link above does not work: 
	* Go to 'https://myaccount.google.com/' and sign in using the email above
	* Then go to the 'Security' tab to the left
	* Then scroll down until you reach 'Less secure app access'
	* Turn on 'Less secure apps'
		
### Backup ###
Backups are stored within the 'backup' folder within the directory of 'Main_Script'.
The pickle file used for backup is stored within the directory of 'Main_Script'.
To test the backup, feel free to change the data within the pickle file using the 'change_month' script (note: this is not intended for the 
system but is only for you, the marker, to test the backup)

### Encryption/Decryption ###
I have included a script called 'encrypt - decrypt' that will encrypt and decrypt the data given to it. 
Feel free to open the database using 'db browser' or other software and copy the passwords into this and decrypt them so you can test 
other accounts which I have not given a password to. 

### Validation ###
Validation:
* The entirety of the customer table has been validated
  * 'telephone number' is checked if it is 11 characters long
  * Both 'first_name' and 'surname' are checked if they only contain alphabetic characters
  * 'Address' is checked to see if it is a number followed by 2 words
  	* The regular expression used is ```^\d+\s[A-z]+\s[A-z]+$```
  * 'Postcode' is checked if it is a valid UK postcode
  	* The regular expression used is ```^(([A-Z][A-Z]{0,1})([0-9][A-Z0-9]{0,1})) {0,}(([0-9])([A-Z]{2}))$```
  * 'Payment_Type'is checked if it is in the list ```["Visa","MaterCard"]```
  * 'Card_Number' and 'CVC_code'  is checked if it is a digit 
  * 'DOB' is checked to see if it is in the past
  * 'Allergies' is checked if it is within the list ```["N\A","Milk","Eggs", "Nuts","Fish","Shellfish","Fruit","Soy"]```
  * 'Expiry_Date' is checked to see if it is given a month and the last 2 digits of a year
  	* The regular expression used is ```([0-9][0-2]|[0-9])-([0-9][0-9])$```
  * 'Email' checks if a character is entered, then a '@', then another character, then '.com.
  	* The regular expression used is ```(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)```
  * 'Username' is checked if it exists within the table
  * 'Password' is checked if it contains 8 characters, a special case character and a number
  	* The regular expression used is ```^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$```
* The 'check_in' and 'check_out' fields have been validated in the booking table
  * Checks if the dates are in the past
  * Checks if check_in is before check_out
* In the staff table the following fields have been validated
  * 'Username' is checked if it exists within the table
  * 'Password' is checked if it contains 8 characters, a special case character and a number
  	* The regular expression used is ```^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$"```

### Dependencies ###
The commands below work under the assumption that 'pip' has been added to the PATH.
To run the commands simply type them into command prompt (cmd) or powershell. 
The following libraries need to be installed for the program to work:
* matplotlib (```$pip install matplotlib```)
* docx (```$pip install python-docx```)
* tkcalendar (```$pip install tkcalendar```)
* Pillow (```$pip install Pillow```)