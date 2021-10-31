import pickle


## This is intended to test the system and is not part of the intende system

print("This program manually changes the previous backup month")
data = int(input("Please enter the data (data must be an integer and below 12) \nyou would like to be in in the pickle file = "))

pickle.dump(data,open("backup.p", "wb" ))
