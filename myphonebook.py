### a simple phone book project with python written by Armin Nasirfam ###

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
    print("\nmax length is %i! try again."%n)

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
        global contact_id
        contact_id = 0
        def add_a_name():           
            name = input("please enter a name (q! to menu) : ")
            back(name)
            # make fist letter upper case
            name = name.capitalize()
            # check valid name
            if re.match("^[a-zA-Z ]+$", name):
                contact_list = []
                # check new contact exist in phone book or not
                if name in phone_book : 
                    print("\n%s exist in phone book!\n"%name)
                    add_a_name()
                else:
                    pass        
            else : 
                print("wrong input! you can use a-z,and white space for your name! try again.")
                add_a_name()    

            # add a contact name like : home, work, ...
            def add_a_contact_name():
                global max_char
                # input contact name and check for maximum  character for contact name
                max_char = True
                while max_char  :
                    contact_name = input("please enter a contact name like (home/work,..) for %s: "%name) 
                    check(contact_name,15)
                    global contact_id
                    contact_id = contact_id + 1
                contact_dict = {}

                # input phone number and check for maximum  character 
                max_char = True
                while max_char  :
                    phone = input("please enter phone number for %s's %s: "%(name,contact_name))
                    check(phone,15)

                # input email and check for maximum character 
                max_char = True
                while max_char  :
                    mail = input("please enter email for %s's %s: "%(name,contact_name))
                    check(mail,30)

                # input address and check for maximum  character 
                max_char = True
                while max_char  :
                    addr = input("please enter address for %s's %s: "%(name,contact_name))
                    check(addr,40)

                contact_dict[contact_name]={"ID":str(contact_id),"phone":phone,"email":mail,"address":addr}
                contact_list.append(contact_dict)

                # asks to add another contact name or not
                def add_contact():
                    answer = input("do you want to add a new contact name for %s?(y/n): "%name)
                    if answer.upper() == "Y":
                        add_a_contact_name()
                    elif answer.upper() == "N":
                        phone_book[name]=contact_list
                        programe()    
                    else : 
                        print("wrong answer! try again. ")
                        add_contact()
                add_contact()            
            add_a_contact_name()        
        add_a_name()
                    
    # deleting a contact
    elif choose == "3" : 
        clear()
        def delete():
            name = input("enter the name of contact, you want to remove (q! to menu): ")
            back(name)
            name = name.capitalize()
            if name in phone_book : 
                del phone_book[name]
                print("\n%s is successfully removed! "%name)
            else:
                print("%s not found!"%name)
                delete()
        delete()
        programe()

    # search 
    elif choose == "4" : 
        clear()
        def search():
            search_by = input("""
You can search by name, number and email (q! to Menu) : 

    1) by name
    2) by number
    3) by email

    :? """)
            # by name    
            if search_by == "1" : 
                name = input("\nplease enter the name : ")
                name = name.capitalize()    
                if name in phone_book : 
                    show(name)
                    search()
                else :
                    print("\n%s not found!"%name)
                    search() 
                                   
            # by number        
            elif search_by == "2" : 
                S = False
                empty = []
                number = input('\nplease enter the number: ')
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
                    print("\n%s not found!"%number)
                    search()                
                            
            # by email
            elif search_by == "3" : 
                S = False
                empty = []
                email = input('\nplease enter the email address: ')
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
                    print("\n%s not found!"%email)    
                    search()
            elif search_by == "q!" : 
                programe()
            else : 
                print("\nwrong answer! try again.")
                search()
        search()
        programe()

    # edit contact
    elif choose == "5":
        clear()
        def edit():
            try : 
                person = new_name
            except :     
                person = input("\nenter the name of contact you want to edit (q! to menu): ")
            back(person)
            person = person.capitalize()
            if person in phone_book : 
                def edit_info(person):
                    item = input("""\nwhat do you want to do?
    
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
                            new_name = input("\nplease enter a new name (enter c! for cancel): ")
                            if new_name == "c!" : 
                                edit_info(person)
                            else:
                                new_name = new_name.capitalize()    
                                # check if new name exist in phone book or not 
                                if new_name in phone_book : 
                                    print("\n%s exist in phone book! choose another name."%new_name)
                                    change_name()
                                else:
                                    pass
                                # check for valid name
                                if re.match("^[a-zA-Z ]+$", new_name):
                                    phone_book[new_name] = phone_book.pop(person)
                                    print("\nname changed to %s!"%new_name)
                                    # after the name was change , edit function has to start again
                                    edit()
                                else : 
                                    print("\nwrong input! you can use a-z and white space for your name! try again.")
                                    change_name()
                        change_name()

                    # delete the contact name
                    elif item == "3" :
                        S = False
                        id_to_del = str(input("\nEnter ID to delete that row : "))
                        for contact in phone_book[person]:
                            for info in contact :
                                if id_to_del in  list(contact[info]["ID"]) : 
                                    S = True
                                    phone_book[person].remove(contact)
                                    print("\nrow %s removed!"%id_to_del)
                                    break
                        if not S : 
                            print("\nrow %s not found!"%id_to_del)    

                        edit_info(person)

                    # add contact name
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
                                                    
                        max_char = True
                        while max_char  :
                            new_contact_name = input("\nplease enter new contact name to add: ")
                            check(new_contact_name,15)
                        contact_dict = {}

                        # add new phone number
                        max_char = True
                        while max_char  :
                            phone = input("\nplease enter phone number: ")
                            check(phone,15)
                        
                        # add new email
                        max_char = True
                        while max_char  :
                            mail = input("\nplease enter email: ")
                            check(mail,30)

                        # add new address    
                        max_char = True
                        while max_char  :
                            addr = input("\nplease enter address: ")
                            check(addr,40)

                        contact_dict[new_contact_name]={"ID":str(contact_id),"phone":phone,"email":mail,"address":addr}
                        phone_book[person].append(contact_dict)
                        print("\n%s successfully added :)"%new_contact_name)
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
                                            new_id = ""
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
                                                    for contact in phone_book[person]:
                                                        for info in contact :
                                                            if id_to_edit  == contact[info]["ID"]:
                                                                contact[new_contact_name] = contact.pop(info)
                                                                print("\ncontact name changed to %s"%new_contact_name)
                                                                sub_edit()
                                        
                                        # edit phone number
                                            elif choose == "3" : 
                                                max_char = True
                                                while max_char : 
                                                    new_phone_number = input("Enter new phone number: ")
                                                    check(new_phone_number,15)
                                                if not max_char : 
                                                    for contact in phone_book[person]:
                                                        for info in contact :    
                                                            if id_to_edit == contact[info]["ID"] :       
                                                                contact[info]["phone"] = new_phone_number       
                                                                print("\nphone number changed to %s"%new_phone_number)
                                                                sub_edit()
                                        
                                            # edit email
                                            elif choose == "4" : 
                                                max_char = True
                                                while max_char : 
                                                    new_email = input("Enter new email: ")
                                                    check(new_email,30)
                                                if not max_char :    
                                                    for contact in phone_book[person]:
                                                        for info in contact :    
                                                            if id_to_edit  == contact[info]["ID"] :       
                                                                contact[info]["email"] = new_email 
                                                                print("\nemail changed to %s"%new_email)
                                                                sub_edit()

                                            # edit address
                                            elif choose == "5" : 
                                                max_char = True
                                                while max_char : 
                                                    new_addr = input("Enter new address: ")
                                                    check(new_addr,40)
                                                if not max_char :    
                                                    for contact in phone_book[person]:
                                                        for info in contact :    
                                                            if id_to_edit  == contact[info]["ID"] :       
                                                                contact[info]["address"] = new_addr
                                                                print("\naddress changed to %s"%new_addr)
                                                                sub_edit()                

                                            elif choose == "6" : 
                                                edit_info(person)
                                            else : 
                                                print("\n%s not found! try again."%choose)
                                                sub_edit()    
                                        sub_edit()   

                                    elif id_to_edit == "c!" :   
                                        edit_info(person)
                            if not S : 
                                print("\n%s not found! try again."%id_to_edit)
                                edit_row()
                        edit_row()
                    # back to main menu 
                    elif item == "6" :    
                        programe() 
                    else:
                        print("\nwrong answer! try again.")
                        edit_info(person)  
                edit_info(person)   
            else : 
                    print("\n%s not found! try again."%person)
                    edit()  
        edit()
        programe()
        
    # save changes
    elif choose =="6" :
        file = open("phone_book_data","w")
        file.write(str(phone_book)) 
        file.close()
        print("\nchanges saved successfully :)")
        programe()
    
    # exit          
    elif choose == "7" : 
        clear()
        print("BYE!")
        exit() 

    # wrong answer
    else:
        print("\nwrong! please select again. \n")
        programe()           

programe()        
