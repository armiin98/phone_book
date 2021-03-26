phone_book = {'Test': [{'home': {'ID': '1', 'phone': '1111', 'email': 'test@info.com', 'address': 'Iran'}}, {'work': {'ID': '2', 'phone': '1234', 'email': 'test@test.com', 'address': 'Tazbriz'}}]}

for person in phone_book:
    for contact in phone_book[person]:
        for info in contact :
            print(info)
                        
                                








                        
# edit id
                   #     if choose == "1" : 
                    #        new_id = input("\nEnter new ID: ")
                     #       for contact in phone_book[person]:
                      ##             if id_to_edit == contact[info]["ID"] :       
                        #                contact[info]["ID"] = new_id                        
