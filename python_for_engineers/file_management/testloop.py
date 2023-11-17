#Loop Through A Text File

#import the os module
import os

#define the current working directory
cwd = os.getcwd()

#loop that manually opens and closes the text file
def for_loop_manual_open_and_close():
   
    #define the path to my text file
    my_switches_path = os.path.join(cwd , "file_management" , "my_switches1.txt")

    #opens the text file
    f = open(my_switches_path)

    #for loop - every line in the f variable (my text file)
    for line in f:
        print (line)

    #close the file
    f.close

#