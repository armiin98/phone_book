### a simple phone book project with python3 ###

# IMPORT REGEX
import re

# IMPORT COLORS
from colorama import Fore, Back, Style

# IMPORT TIME MODULE
import time

#IMPORT ARGUMENT PARSER
import argparse

#IMPORT SYS
import sys

# CLEAR SCREAN
from clear_screen import clear 

# FUCNTION TO BACK TO MENU 
def back(back):
    if back == "q!":
        programe()
    else:
        pass    

# MAX LENGTH CHECK
def check(item,n):
  if len(item) <=n:
    global max_char
    max_char = False
  else:
    print(Fore.RED+"\nMax length is %i! try again.\n"%n,Style.RESET_ALL)

# OPEN PHONE BOOK DATA
try : 
    file = open("phone_book_data","r")
    reader = file.read()
    # READ DICTIONARY FROM FILE
    import ast
    phone_book = ast.literal_eval(reader)
    file.close()
    # IF THERE WAS NO DATABASE, CREATE ONE
except FileNotFoundError : 
    phone_book = {}   

# A BOOLEAN TO CHECK IF CHANGES SAVED OR NOT 
global SAVE
SAVE = True

# A FUNCTION TO CHECK THAT INPUT  IS NOT  EMPTY
def ask_user(message=''):
    user_input = ''
    while not user_input:
        user_input = input(message)
    return user_input


# MAIN FUNCTION OF PROGRAME
def programe():
    # MENU
    print("""

            ~MENU~

    1) READ ALL CONTACTS
    2) ADD A CONTACT
    3) DELETE A CONTACT
    4) SEARCH A CONTACT
    5) EDIT A CONTACT
    6) SAVE CHANGES
    7) Exit\n""")
    choose = ask_user("    Please select an Option: ")    

    # THIS FUNCTION SHOWS PERSONS INFORMATION IN A TABLE
    def show(person):
        print(Fore.BLUE+"\n>> %s"%person,Style.RESET_ALL,"'s informations: \n",sep="")
        # DECRATE BEFORE PRINTING CONTACTS
        print("     ","+","="*4,"+","="*15,"+","="*15,"+","="*30,"+","="*40,"+",sep="")
        print("     ","|",Fore.RED+"ID".center(4),Style.RESET_ALL,"|",Fore.RED+"CONTACT NAME".center(15),Style.RESET_ALL,"|",Fore.RED+"PHONE NUMBER".center(15),Style.RESET_ALL,"|",Fore.RED+"E-MAIL".center(30),Style.RESET_ALL,"|",Fore.RED+"ADDRESS".center(40),Style.RESET_ALL,"|",sep="")
        print("     ","+","="*4,"+","="*15,"+","="*15,"+","="*30,"+","="*40,"+",sep="")
        for contact in phone_book[person]:
            for info in contact : 
                print("     ","|",Fore.GREEN+contact[info]["ID"].center(4),Style.RESET_ALL,"|",info.center(15),"|",contact[info]["phone"].center(15),"|",contact[info]["email"].center(30),"|",contact[info]["address"].center(40),"|",sep="")  
                print("     ","+","-"*4,"+","-"*15,"+","-"*15,"+","-"*30,"+","-"*40,"+",sep="")
            
    # PRINT PHONE BOOK
    if choose == "1" : 
        clear()
        def all_contacts():
            # SORT BEFORE SHOW CONTACTS
            sorted_contacts = sorted(phone_book)
            for person in sorted_contacts :
                show(person)
        all_contacts()
        programe()    
    
    # ADD NEW CONTACT    
    elif choose == "2" :
        clear()
        # MAKE AN ID FOR EACH CONTACT NAME
        global contact_id
        contact_id = 0
        def add_a_name():           
            name = ask_user("Please enter a name (q! to menu) : ")
            back(name)
            # MAKE FIST LETTER UPPER CASE
            name = name.capitalize()
            # CHECK VALID NAME
            if re.match("^[a-zA-Z ]+$", name):
                contact_list = []
                # CHECK NEW CONTACT EXIST IN PHONE BOOK OR NOT
                if name in phone_book : 
                    print(Fore.RED+"\n%s exist in phone book!\n"%name,Style.RESET_ALL)
                    add_a_name()       
            else : 
                print(Fore.RED+"\nWrong input! you can use \"english alphabet\" and \"white space\" for your name! try again.\n",Style.RESET_ALL)
                add_a_name()    

            # ADD A CONTACT NAME LIKE : HOME, WORK, ...
            def add_a_contact_name():
                global SAVE, max_char
                SAVE = False
                # INPUT CONTACT NAME AND CHECK FOR MAXIMUM  CHARACTER FOR CONTACT NAME
                max_char = True
                while max_char  :
                    contact_name = ask_user("Please enter a contact name like (home/work,..) for %s: "%name) 
                    check(contact_name,15)
                    global contact_id
                    contact_id += 1 
                contact_dict = {}

                # INPUT PHONE NUMBER AND CHECK FOR VALIDATION AND MAX LIMIT
                max_char = True
                while max_char  :
                    try : 
                        phone = int(ask_user("Please enter phone number for %s's %s: "%(name,contact_name)))
                        phone = str(phone)
                        check(phone,15)
                    except : 
                        print(Fore.RED+"\nThis is not a phone number! try again\n",Style.RESET_ALL)
                   
                # INPUT EMAIL AND CHECK FOR VALIDATION AND MAX LIMIT
                max_char = True
                while max_char  :
                    mail = ask_user("Please enter email for %s's %s: "%(name,contact_name))
                    # CHECK VALID EMAIL
                    if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", mail):
                        check(mail,30)
                    else :
                        print(Fore.RED+"\nThis is not an email! try again.\n",Style.RESET_ALL)     

                        
                # INPUT ADDRESS AND CHECK FOR MAXIMUM  CHARACTER 
                max_char = True
                while max_char  :
                    addr = ask_user("Please enter address for %s's %s: "%(name,contact_name))
                    check(addr,40)
                    
                # ADD THIS INPUTS TO PHONE BOOK
                contact_dict[contact_name]={"ID":str(contact_id),"phone":phone,"email":mail,"address":addr}
                contact_list.append(contact_dict)

                # ASKS TO ADD ANOTHER CONTACT NAME OR NOT
                def add_contact():
                    answer = ask_user("Do you want to add a new contact name for %s?(y/n): "%name)
                    if answer.upper() == "Y":
                        add_a_contact_name()
                    elif answer.upper() == "N":
                        phone_book[name]=contact_list
                        # ADDING NEW CONTACT FINISHED
                        print(Fore.GREEN+"\n\"%s\" succesfully added to your phone book!"%name,Style.RESET_ALL)
                        programe()    
                    else : 
                        print(Fore.RED+"\nWrong answer! try again.\n",Style.RESET_ALL)
                        add_contact()
                add_contact()            
            add_a_contact_name()        
        add_a_name()
                    
    # DELETING A CONTACT
    elif choose == "3" : 
        clear()
        def delete():
            name = ask_user("Enter the name of contact, you want to remove (q! to menu): ")
            back(name)
            name = name.capitalize()
            if name in phone_book : 
                del phone_book[name]
                print(Fore.GREEN+"\n\"%s\" has been successfully removed! "%name,Style.RESET_ALL)
                global SAVE
                SAVE = False
            else:
                print(Fore.RED+"\"%s\" not found!"%name,Style.RESET_ALL)
                delete()        
        delete()
        programe()

    # SEARCH 
    elif choose == "4" : 
        clear()
        def search():
            search_by = ask_user("""
You can search by \"name\", \"number\" and \"email\" (q! to Menu) : 

    1) by name
    2) by number
    3) by email

    :? """)
            back(search_by)

            # BY NAME    
            if search_by == "1" : 
                name = ask_user("\nPlease enter the name : ")
                name = name.capitalize()    
                if name in phone_book : 
                    show(name)
                    search()
                else :
                    print(Fore.RED+"\n\"%s\" not found!"%name,Style.RESET_ALL)
                    search() 
                                   
            # BY NUMBER        
            elif search_by == "2" : 
                S = False
                empty = []
                number = ask_user('\nPlease enter the number: ')
                for person in phone_book : 
                    for contact in phone_book[person] :
                        if person not in empty : 
                            for info in contact :
                                if contact[info]["phone"] == number :  
                                    empty.append(person)
                                    show(person)
                                    S = True
                                    search()
                if not S : 
                    print(Fore.RED+"\n\"%s\" not found!"%number,Style.RESET_ALL)
                    search()                
                            
            # BY EMAIL
            elif search_by == "3" : 
                S = False
                empty = []
                email = ask_user('\nPlease enter the email address: ')
                for person in phone_book : 
                    for contact in phone_book[person] :
                        if person not in empty :
                            for info in contact :
                                if contact[info]["email"] == email :  
                                    empty.append(person)
                                    show(person)
                                    S = True
                                    search()            
                if not S : 
                    print(Fore.RED+"\n\"%s\" not found!"%email,Style.RESET_ALL)    
                    search()
            else : 
                print(Fore.RED+"\nWrong answer! try again.",Style.RESET_ALL)
                search()
        search()
        programe()

    # EDIT CONTACT
    elif choose == "5":
        clear()
        # THIS TRY STATEMENT CREATED BECAUSE IF NAME HAS CHANGED BY USER, USER DOES NOT HAVE TO ENTER NEW NAME AGAIN TO RUN EDIT OPTION
        def edit():
            try : 
                person = new_name
            except :     
                person = ask_user("\nEnter the name of contact you want to edit (q! to menu): ")
            back(person)
            person = person.capitalize()
            if person in phone_book : 
                def edit_info(person):
                    item = ask_user("""\nWhat do you want to do?
    
    1) show contact info
    2) edit name
    3) remove a row
    4) add a row
    5) edit a row
    6) exit

    :? """)

                    #SHOW INFO OF CONTACT
                    if item == "1" :
                        clear()
                        show(person)
                        edit_info(person)

                    # CHANGE THE NAME
                    elif item == "2" :
                        def change_name():
                            global new_name
                            new_name = ask_user("\nPlease enter a new name (enter c! for cancel): ")
                            # C! FOR CANCELING THIS OPRATION
                            if new_name == "c!" : 
                                edit_info(person)
                            else:
                                new_name = new_name.capitalize()    
                                # CHECK IF NEW NAME EXIST IN PHONE BOOK OR NOT 
                                if new_name in phone_book : 
                                    print(Fore.RED+"\n\"%s\" Exist in phone book! choose another name."%new_name,Style.RESET_ALL)
                                    change_name()
                                else:
                                    pass
                                # CHECK FOR VALID NAME
                                if re.match("^[a-zA-Z ]+$", new_name):
                                    phone_book[new_name] = phone_book.pop(person)
                                    print(Fore.GREEN+"\nName changed to \"%s\" !"%new_name,Style.RESET_ALL)
                                    global SAVE
                                    SAVE = False
                                    # AFTER THE NAME WAS CHANGE , EDIT FUNCTION HAS TO START AGAIN
                                    edit()
                                else : 
                                    print(Fore.RED+"\nWrong input! you can use \"english alphabet\" and \"white space\" for your name! try again.",Style.RESET_ALL)
                                    change_name()
                        change_name()

                    # DELETE A ROW
                    elif item == "3" :
                        S = False
                        id_to_del = str(ask_user("\nEnter ID to delete that row (enter c! for cancel): "))
                        if id_to_del == "c!" : 
                            edit_info(person)
                        for contact in phone_book[person]:
                            for info in contact :
                                if id_to_del in  list(contact[info]["ID"]) : 
                                    S = True
                                    phone_book[person].remove(contact)
                                    print(Fore.GREEN+"\nRow \"%s\" removed!"%id_to_del,Style.RESET_ALL)
                                    global SAVE
                                    SAVE = False
                                    break
                        if not S : 
                            print(Fore.RED+"\nRow \"%s\" not found!"%id_to_del,Style.RESET_ALL)    
                        edit_info(person)

                    # ADD A ROW
                    elif item == "4" : 
                        global max_char
                        # READ CONTACT ID ; IF THERE WAS NO ROW , ID WOULD BE 1
                        try : 
                            for contact in phone_book[person]:
                                for info in contact : 
                                    contact_id = int(contact[info]["ID"])
                            contact_id = str(contact_id + 1)  
                        except : 
                            contact_id = 1      

                        # ADD NEW CONTACT NAME                          
                        max_char = True
                        while max_char  :
                            new_contact_name = ask_user("\nPlease enter new contact name to add (enter c! for cancel): ")
                            if new_contact_name == "c!" : 
                                edit_info(person)
                            check(new_contact_name,15)
                        contact_dict = {}

                        # ADD NEW PHONE NUMBER
                        max_char = True
                        while max_char  :
                            # CHECK FOR VAKID PHONE NUMBER
                            try : 
                                phone = int(ask_user("Please enter phone number: "))
                                phone = str(phone)
                                check(phone,15)
                            except : 
                                print(Fore.RED+"\nThis is not a phone number! try again\n",Style.RESET_ALL)
                        
                        # ADD NEW EMAIL
                        max_char = True
                        while max_char  :
                            mail = ask_user("Please enter email: ")
                            # CHECK VALID EMAIL
                            if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", mail):
                                check(mail,30)
                            else :
                                print(Fore.RED+"\nThis is not an email! try again.\n",Style.RESET_ALL)

                        # ADD NEW ADDRESS    
                        max_char = True
                        while max_char  :
                            addr = ask_user("Please enter address: ")
                            check(addr,40)

                        # ADD INFORMATIONS TO PHONE BOOK
                        contact_dict[new_contact_name]={"ID":str(contact_id),"phone":phone,"email":mail,"address":addr}
                        phone_book[person].append(contact_dict)
                        print(Fore.GREEN+"\n\"%s\" successfully added!"%new_contact_name,Style.RESET_ALL)
                        SAVE = False
                        edit_info(person)
                    
                    # EDIT A ROW
                    elif item == "5" :    
                        def edit_row():
                            id_to_edit = ask_user("\nEnter ID to edit the row (c! for cancel): ") 
                            S = False
                            for contact in phone_book[person]:
                                for info in contact :          
                                    if id_to_edit == contact[info]["ID"]:
                                        S = True
                                        clear()
                                        def sub_edit():
                                            global max_char
                                            choose = ask_user("""\nwhat are you gonna do?

    1) show row info
    2) edit Contact Name
    3) edit Phone number
    4) edit E-mail
    5) edit Address
    6) exit

    ?: """)                                 # SHOW TABLE
                                            if choose == "1" : 
                                                clear()
                                                print(Fore.BLUE+"\n>> %s"%person,Style.RESET_ALL,"'s informations: \n",sep="")
                                                # DECRATE BEFORE PRINTING CONTACTS
                                                print("     ","+","="*4,"+","="*15,"+","="*15,"+","="*30,"+","="*40,"+",sep="")
                                                print("     ","|",Fore.RED+"ID".center(4),Style.RESET_ALL,"|",Fore.RED+"CONTACT NAME".center(15),Style.RESET_ALL,"|",Fore.RED+"PHONE NUMBER".center(15),Style.RESET_ALL,"|",Fore.RED+"E-MAIL".center(30),Style.RESET_ALL,"|",Fore.RED+"ADDRESS".center(40),Style.RESET_ALL,"|",sep="")
                                                print("     ","+","="*4,"+","="*15,"+","="*15,"+","="*30,"+","="*40,"+",sep="")
                                                for contact in phone_book[person]:
                                                    for info in contact : 
                                                        # JUST PRINT A ROW THAT USER WANTS
                                                        if id_to_edit == contact[info]["ID"] : 
                                                            print("     ","|",Fore.GREEN+contact[info]["ID"].center(4),Style.RESET_ALL,"|",info.center(15),"|",contact[info]["phone"].center(15),"|",contact[info]["email"].center(30),"|",contact[info]["address"].center(40),"|",sep="")  
                                                            print("     ","+","-"*4,"+","-"*15,"+","-"*15,"+","-"*30,"+","-"*40,"+",sep="")

                                                sub_edit()                                   
                                            
                                            # EDIT CONTACT NAME
                                            elif choose == "2" : 
                                                max_char = True
                                                while max_char : 
                                                    new_contact_name = ask_user("\nEnter new contact name: ")
                                                    check(new_contact_name,15)
                                                if not max_char : 
                                                    global SAVE
                                                    SAVE = False    
                                                    for contact in phone_book[person]:
                                                        for info in contact :
                                                            if id_to_edit  == contact[info]["ID"]:
                                                                contact[new_contact_name] = contact.pop(info)
                                                                print(Fore.GREEN+"\ncontact name changed to \"%s\""%new_contact_name,Style.RESET_ALL)
                                                                sub_edit()
                                        
                                            # EDIT PHONE NUMBER
                                            elif choose == "3" : 
                                                max_char = True
                                                while max_char : 
                                                    # CHECK FOR VALID PHONE NUMBER
                                                    try :
                                                        new_phone_number = int(ask_user("\nEnter new phone number: "))
                                                        new_phone_number = str(new_phone_number)
                                                        check(new_phone_number,15)
                                                    except : 
                                                        print(Fore.RED+"\nThis is not a phone number! try again",Style.RESET_ALL)
                                                if not max_char : 
                                                    for contact in phone_book[person]:
                                                        for info in contact :    
                                                            if id_to_edit == contact[info]["ID"] :       
                                                                contact[info]["phone"] = new_phone_number       
                                                                print(Fore.GREEN+"\nphone number changed to \"%s\""%new_phone_number,Style.RESET_ALL)
                                                                SAVE = False
                                                                sub_edit()
                                        
                                            # EDIT EMAIL
                                            elif choose == "4" : 
                                                max_char = True
                                                while max_char : 
                                                    new_email = ask_user("\nEnter new email: ")
                                                    # CHECK VALID EMAIL
                                                    if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", new_email):
                                                        check(new_email,30)
                                                    else : 
                                                        print(Fore.RED+"\nThis is not an email! try again.",Style.RESET_ALL)    
                                                if not max_char :    
                                                    for contact in phone_book[person]:
                                                        for info in contact :    
                                                            if id_to_edit  == contact[info]["ID"] :       
                                                                contact[info]["email"] = new_email 
                                                                print(Fore.GREEN+"\nemail changed to \"%s\""%new_email,Style.RESET_ALL)
                                                                SAVE = False
                                                                sub_edit()

                                            # EDIT ADDRESS
                                            elif choose == "5" : 
                                                max_char = True
                                                while max_char : 
                                                    new_addr = ask_user("\nEnter new address: ")
                                                    check(new_addr,40)
                                                if not max_char :    
                                                    for contact in phone_book[person]:
                                                        for info in contact :    
                                                            if id_to_edit  == contact[info]["ID"] :       
                                                                contact[info]["address"] = new_addr
                                                                print(Fore.GREEN+"\nAddress changed to \"%s\""%new_addr,Style.RESET_ALL)  
                                                                SAVE = False                                                              
                                                                sub_edit() 
                                            
                                            # EXIT AND BACK TO MENU               
                                            elif choose == "6" : 
                                                edit_info(person)
                                            else : 
                                                print(Fore.RED+"\nWrong answer! try again.",Style.RESET_ALL)
                                                sub_edit()    
                                        sub_edit()   

                                    elif id_to_edit == "c!" :   
                                        edit_info(person)
                            if not S : 
                                print(Fore.RED+"\n\"%s\" not found! try again."%id_to_edit,Style.RESET_ALL)
                                edit_row()
                        edit_row()

                    # BACK TO MAIN MENU 
                    elif item == "6" :
                        try : 
                            # DELETE NEW NAME VARIABLE
                            global new_name
                            del new_name
                        except : 
                            pass

                        programe() 
                    else:
                        print(Fore.RED+"\nWrong answer! try again.",Style.RESET_ALL)
                        edit_info(person)  
                edit_info(person)   
            else : 
                    print(Fore.RED+"\n%s not found! try again."%person,Style.RESET_ALL)
                    edit()  
        edit()
        programe()
        
    # SAVE CHANGES
    elif choose =="6" :
        def write () :
            file = open("phone_book_data","w")
            file.write(str(phone_book)) 
            file.close()
            print(Fore.GREEN+"\n    Changes saved successfully!",Style.RESET_ALL)
            global SAVE
            SAVE = True
            programe()
        write()    
    
    # EXIT          
    elif choose == "7" : 
        def quit():
            # EXIT, IF CHANGES HAVE BEEN SAVED
            if SAVE == True : 
                print("    BYE!")
                time.sleep(3) 
                clear()
                exit()

            elif SAVE == False : 
                # ASK TO EXIT OR NOT WHEN CHANGES HAVE NOT SAVED
                print("\n    The changes have not been saved yet! do you want to save before quit?",Fore.RED+"(y/n): ",Style.RESET_ALL,end="")
                answer = input("") 
                # SAVE BEFORE EXIT
                if answer.upper() == "Y" : 
                    file = open("phone_book_data","w")
                    file.write(str(phone_book)) 
                    file.close()
                    print(Fore.GREEN+"\n    Changes saved successfully!",Style.RESET_ALL)
                    print("    BYE!")
                    time.sleep(3) 
                    clear()
                    exit()
                # EXIT WITHOUT SAVE
                elif answer.upper() == "N" :
                    print("    BYE!")
                    time.sleep(3) 
                    clear()
                    exit()
                else : 
                    quit()    
        quit()            

    # WRONG ANSWER
    else:
        print(Fore.RED+"\n    Wrong! please select again. \n",Style.RESET_ALL)
        programe()           
# programe

#Get options from the command line
def ArgumentParser():
    #Define the options
    parser = argparse.ArgumentParser(description="--> a program for save and read your contacts information <--")
    parser.add_argument("name",help="Show contact information by name", nargs="*")
    parser.add_argument("-v", "--verbosity", help="Show more information from contacts {Can not be used with [-A]}", action="store_true")
    # Options that conflict each other
    conflicts = parser.add_mutually_exclusive_group()
    conflicts.add_argument("-A", help="Show all contact numbers", dest="ShowAll", action="store_true")
    conflicts.add_argument("-n", "--number", help="Show contact information by number", dest="ContactNumber", type=int, required=False)

    #a function for show complet information (for verbosity option)
    def CompletInfo(ContactName,pattern,PatternType):
        global phone_book
        # show additional information by name:
        if PatternType == 'name':
            for info in phone_book[pattern]:
                for contact in info:
                    if contact == ContactName:
                        print("{0} ID --> {1}".format(ContactName,info[ContactName]['ID']))
                        print("{0} Email --> {1}".format(ContactName,info[ContactName]['email']))
                        print("{0} Address --> {1}".format(ContactName,info[ContactName]['address']))
                        print(25*"-")
        #show additional information by number:
        elif PatternType == 'number':
            for name in phone_book:
                for info in phone_book[name]:
                    for contact in info:
                        if contact == ContactName:
                            if info[ContactName]['phone'] == pattern:
                                print("{0} ID --> {1}".format(ContactName, info[ContactName]['ID']))
                                print("{0} Email --> {1}".format(ContactName, info[ContactName]['email']))
                                print("{0} Address --> {1}".format(ContactName, info[ContactName]['address']))
                                print(25*"-")
