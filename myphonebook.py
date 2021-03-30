### a simple phone book project with python3 ###

# import regex
import re

# import colors
from colorama import Fore, Back, Style

# clear screan
from clear_screen import clear 

# fucntion to back to menu 
def back(back):
    if back == "q!":
        programe()
    else:
        pass    

# max length check
def check(item,n):
  if len(item) <=n:
    global max_char
    max_char = False
  else:
    print(Fore.RED+"\nMax length is %i! try again.\n"%n,Style.RESET_ALL)

# open phone book data
try : 
    file = open("phone_book_data","r")
    reader = file.read()
    # read dictionary from file
    import ast
    phone_book = ast.literal_eval(reader)
    file.close()
    # if there was no database, create one
except FileNotFoundError : 
    phone_book = {}   

# a boolean to check if changes saved or not 
global SAVE
SAVE = True

# main function of programe
def programe():
    print("""

            ~MENU~

    1) READ ALL CONTACTS
    2) ADD A CONTACT
    3) DELETE A CONTACT
    4) SEARCH A CONTACT
    5) EDIT A CONTACT
    6) SAVE CHANGES
    7) Exit\n""")
    choose = input("    Please select an Option: ")    

    # this function shows persons information in a table
    def show(person):
        print(Fore.BLUE+"\n>> %s"%person,Style.RESET_ALL,"'s informations: \n",sep="")
        # decrate before printing contacts
        print("     ","+","="*4,"+","="*15,"+","="*15,"+","="*30,"+","="*40,"+",sep="")
        print("     ","|",Fore.RED+"ID".center(4),Style.RESET_ALL,"|",Fore.RED+"CONTACT NAME".center(15),Style.RESET_ALL,"|",Fore.RED+"PHONE NUMBER".center(15),Style.RESET_ALL,"|",Fore.RED+"E-MAIL".center(30),Style.RESET_ALL,"|",Fore.RED+"ADDRESS".center(40),Style.RESET_ALL,"|",sep="")
        print("     ","+","="*4,"+","="*15,"+","="*15,"+","="*30,"+","="*40,"+",sep="")
        for contact in phone_book[person]:
            for info in contact : 
                print("     ","|",Fore.GREEN+contact[info]["ID"].center(4),Style.RESET_ALL,"|",info.center(15),"|",contact[info]["phone"].center(15),"|",contact[info]["email"].center(30),"|",contact[info]["address"].center(40),"|",sep="")  
                print("     ","+","-"*4,"+","-"*15,"+","-"*15,"+","-"*30,"+","-"*40,"+",sep="")
            
    # print phone book
    if choose == "1" : 
        clear()
        def all_contacts():
            # sort before show contacts
            sorted_contacts = sorted(phone_book)
            for person in sorted_contacts :
                show(person)
        all_contacts()
        programe()    
    
    # add new contact    
    elif choose == "2" :
        clear()
        # make an id for each contact name
        global contact_id
        contact_id = 0
        def add_a_name():           
            name = input("Please enter a name (q! to menu) : ")
            back(name)
            # make fist letter upper case
            name = name.capitalize()
            # check valid name
            if re.match("^[a-zA-Z ]+$", name):
                contact_list = []
                # check new contact exist in phone book or not
                if name in phone_book : 
                    print(Fore.RED+"\n%s exist in phone book!\n"%name,Style.RESET_ALL)
                    add_a_name()       
            else : 
                print(Fore.RED+"\nWrong input! you can use \"english alphabet\" and \"white space\" for your name! try again.\n",Style.RESET_ALL)
                add_a_name()    

            # add a contact name like : home, work, ...
            def add_a_contact_name():
                global SAVE, max_char
                SAVE = False
                # input contact name and check for maximum  character for contact name
                max_char = True
                while max_char  :
                    contact_name = input("Please enter a contact name like (home/work,..) for %s: "%name) 
                    check(contact_name,15)
                    global contact_id
                    contact_id += 1 
                contact_dict = {}

                # input phone number and check for validation and max limit
                max_char = True
                while max_char  :
                    try : 
                        phone = int(input("Please enter phone number for %s's %s: "%(name,contact_name)))
                        phone = str(phone)
                        check(phone,15)
                    except : 
                        print(Fore.RED+"\nThis is not a phone number! try again\n",Style.RESET_ALL)
                   
                # input email and check for validation and max limit
                max_char = True
                while max_char  :
                    mail = input("Please enter email for %s's %s: "%(name,contact_name))
                    # check valid email
                    if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", mail):
                        check(mail,30)
                    else :
                        print(Fore.RED+"\nThis is not an email! try again.\n",Style.RESET_ALL)     

                        
                # input address and check for maximum  character 
                max_char = True
                while max_char  :
                    addr = input("Please enter address for %s's %s: "%(name,contact_name))
                    check(addr,40)
                    
                # add this inputs to phone book
                contact_dict[contact_name]={"ID":str(contact_id),"phone":phone,"email":mail,"address":addr}
                contact_list.append(contact_dict)

                # asks to add another contact name or not
                def add_contact():
                    answer = input("Do you want to add a new contact name for %s?(y/n): "%name)
                    if answer.upper() == "Y":
                        add_a_contact_name()
                    elif answer.upper() == "N":
                        phone_book[name]=contact_list
                        # adding new contact finished
                        print(Fore.GREEN+"\n\"%s\" succesfully added to your phone book!"%name,Style.RESET_ALL)
                        programe()    
                    else : 
                        print(Fore.RED+"\nWrong answer! try again.\n",Style.RESET_ALL)
                        add_contact()
                add_contact()            
            add_a_contact_name()        
        add_a_name()
                    
    # deleting a contact
    elif choose == "3" : 
        clear()
        def delete():
            name = input("Enter the name of contact, you want to remove (q! to menu): ")
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

    # search 
    elif choose == "4" : 
        clear()
        def search():
            search_by = input("""
You can search by \"name\", \"number\" and \"email\" (q! to Menu) : 

    1) by name
    2) by number
    3) by email

    :? """)
            back(search_by)

            # by name    
            if search_by == "1" : 
                name = input("\nPlease enter the name : ")
                name = name.capitalize()    
                if name in phone_book : 
                    show(name)
                    search()
                else :
                    print(Fore.RED+"\n\"%s\" not found!"%name,Style.RESET_ALL)
                    search() 
                                   
            # by number        
            elif search_by == "2" : 
                S = False
                empty = []
                number = input('\nPlease enter the number: ')
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
                            
            # by email
            elif search_by == "3" : 
                S = False
                empty = []
                email = input('\nPlease enter the email address: ')
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

    # edit contact
    elif choose == "5":
        clear()
        # this try statement created because if name has changed by user, user does not have to enter new name again to run edit option
        def edit():
            try : 
                person = new_name
            except :     
                person = input("\nEnter the name of contact you want to edit (q! to menu): ")
            back(person)
            person = person.capitalize()
            if person in phone_book : 
                def edit_info(person):
                    item = input("""\nWhat do you want to do?
    
    1) show contact info
    2) edit name
    3) remove a row
    4) add a row
    5) edit a row
    6) exit

    :? """)

                    #show info of contact
                    if item == "1" :
                        clear()
                        show(person)
                        edit_info(person)

                    # change the name
                    elif item == "2" :
                        def change_name():
                            global new_name
                            new_name = input("\nPlease enter a new name (enter c! for cancel): ")
                            # c! for canceling this opration
                            if new_name == "c!" : 
                                edit_info(person)
                            else:
                                new_name = new_name.capitalize()    
                                # check if new name exist in phone book or not 
                                if new_name in phone_book : 
                                    print(Fore.RED+"\n\"%s\" Exist in phone book! choose another name."%new_name,Style.RESET_ALL)
                                    change_name()
                                else:
                                    pass
                                # check for valid name
                                if re.match("^[a-zA-Z ]+$", new_name):
                                    phone_book[new_name] = phone_book.pop(person)
                                    print(Fore.GREEN+"\nName changed to \"%s\" !"%new_name,Style.RESET_ALL)
                                    global SAVE
                                    SAVE = False
                                    # after the name was change , edit function has to start again
                                    edit()
                                else : 
                                    print(Fore.RED+"\nWrong input! you can use \"english alphabet\" and \"white space\" for your name! try again.",Style.RESET_ALL)
                                    change_name()
                        change_name()

                    # delete a row
                    elif item == "3" :
                        S = False
                        id_to_del = str(input("\nEnter ID to delete that row (enter c! for cancel): "))
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

                    # add a row
                    elif item == "4" : 
                        global max_char
                        # read contact id ; if there was no row , id would be 1
                        try : 
                            for contact in phone_book[person]:
                                for info in contact : 
                                    contact_id = int(contact[info]["ID"])
                            contact_id = str(contact_id + 1)  
                        except : 
                            contact_id = 1      

                        # add new contact name                          
                        max_char = True
                        while max_char  :
                            new_contact_name = input("\nPlease enter new contact name to add (enter c! for cancel): ")
                            if new_contact_name == "c!" : 
                                edit_info(person)
                            check(new_contact_name,15)
                        contact_dict = {}

                        # add new phone number
                        max_char = True
                        while max_char  :
                            # check for vakid phone number
                            try : 
                                phone = int(input("Please enter phone number: "))
                                phone = str(phone)
                                check(phone,15)
                            except : 
                                print(Fore.RED+"\nThis is not a phone number! try again\n",Style.RESET_ALL)
                        
                        # add new email
                        max_char = True
                        while max_char  :
                            mail = input("Please enter email: ")
                            # check valid email
                            if re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", mail):
                                check(mail,30)
                            else :
                                print(Fore.RED+"\nThis is not an email! try again.\n",Style.RESET_ALL)

                        # add new address    
                        max_char = True
                        while max_char  :
                            addr = input("Please enter address: ")
                            check(addr,40)

                        # add informations to phone book
                        contact_dict[new_contact_name]={"ID":str(contact_id),"phone":phone,"email":mail,"address":addr}
                        phone_book[person].append(contact_dict)
                        print(Fore.GREEN+"\n\"%s\" successfully added!"%new_contact_name,Style.RESET_ALL)
                        SAVE = False
                        edit_info(person)
                    
                    # edit a row
                    elif item == "5" :    
                        def edit_row():
                            id_to_edit = input("\nEnter ID to edit the row (c! for cancel): ") 
                            S = False
                            for contact in phone_book[person]:
                                for info in contact :          
                                    if id_to_edit == contact[info]["ID"]:
                                        S = True
                                        clear()
                                        def sub_edit():
                                            global max_char
                                            choose = input("""\nwhat are you gonna do?

    1) show row info
    2) edit Contact Name
    3) edit Phone number
    4) edit E-mail
    5) edit Address
    6) exit

    ?: """)                                 # show table
                                            if choose == "1" : 
                                                clear()
                                                print(Fore.BLUE+"\n>> %s"%person,Style.RESET_ALL,"'s informations: \n",sep="")
                                                # decrate before printing contacts
                                                print("     ","+","="*4,"+","="*15,"+","="*15,"+","="*30,"+","="*40,"+",sep="")
                                                print("     ","|",Fore.RED+"ID".center(4),Style.RESET_ALL,"|",Fore.RED+"CONTACT NAME".center(15),Style.RESET_ALL,"|",Fore.RED+"PHONE NUMBER".center(15),Style.RESET_ALL,"|",Fore.RED+"E-MAIL".center(30),Style.RESET_ALL,"|",Fore.RED+"ADDRESS".center(40),Style.RESET_ALL,"|",sep="")
                                                print("     ","+","="*4,"+","="*15,"+","="*15,"+","="*30,"+","="*40,"+",sep="")
                                                for contact in phone_book[person]:
                                                    for info in contact : 
                                                        # just print a row that user wants
                                                        if id_to_edit == contact[info]["ID"] : 
                                                            print("     ","|",Fore.GREEN+contact[info]["ID"].center(4),Style.RESET_ALL,"|",info.center(15),"|",contact[info]["phone"].center(15),"|",contact[info]["email"].center(30),"|",contact[info]["address"].center(40),"|",sep="")  
                                                            print("     ","+","-"*4,"+","-"*15,"+","-"*15,"+","-"*30,"+","-"*40,"+",sep="")

                                                sub_edit()                                   
                                            
                                            # edit contact name
                                            elif choose == "2" : 
                                                max_char = True
                                                while max_char : 
                                                    new_contact_name = input("\nEnter new contact name: ")
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
                                        
                                            # edit phone number
                                            elif choose == "3" : 
                                                max_char = True
                                                while max_char : 
                                                    # check for valid phone number
                                                    try :
                                                        new_phone_number = int(input("\nEnter new phone number: "))
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
                                        
                                            # edit email
                                            elif choose == "4" : 
                                                max_char = True
                                                while max_char : 
                                                    new_email = input("\nEnter new email: ")
                                                    # check valid email
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

                                            # edit address
                                            elif choose == "5" : 
                                                max_char = True
                                                while max_char : 
                                                    new_addr = input("\nEnter new address: ")
                                                    check(new_addr,40)
                                                if not max_char :    
                                                    for contact in phone_book[person]:
                                                        for info in contact :    
                                                            if id_to_edit  == contact[info]["ID"] :       
                                                                contact[info]["address"] = new_addr
                                                                print(Fore.GREEN+"\nAddress changed to \"%s\""%new_addr,Style.RESET_ALL)  
                                                                SAVE = False                                                              
                                                                sub_edit() 
                                            
                                            # exit and back to menu               
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

                    # back to main menu 
                    elif item == "6" :
                        try : 
                            # delete new name variable
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
        
    # save changes
    elif choose =="6" :
        file = open("phone_book_data","w")
        file.write(str(phone_book)) 
        file.close()
        print(Fore.GREEN+"\n    Changes saved successfully!",Style.RESET_ALL)
        global SAVE
        SAVE = True
        programe()
    
    # exit          
    elif choose == "7" : 
        # exit, if changes have been saved
        if SAVE == True : 
            clear()
            print("BYE!")
            exit()
        elif SAVE == False : 
            # ask to exit or not when changes have not saved
            print("\n    The changes have not been saved yet! quit anyway?",Fore.RED+"(y/n): ",Style.RESET_ALL,end="")
            answer = input("") 
            if answer.upper() == "Y" : 
                clear()
                print("BYE!")
                exit()
            else : 
                programe()

    # wrong answer
    else:
        print(Fore.RED+"\n    Wrong! please select again. \n",Style.RESET_ALL)
        programe()           

programe()        
