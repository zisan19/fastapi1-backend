def insert_student(name:str,math:int,eng:int):
    if type(math)==int and type(eng)==int:
        print("Name:",name)
        total=math+eng
        print("Total marks :",total)
    
    else:
        print("Wrong data type")
    
insert_student("Rakib",'34','78')
insert_student("Sakib",34,78)