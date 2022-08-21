dummy_list= []
c="y"
while (c in "yY"):
    print("1. PUSH")
    print( "2. POP")
    print("3. Display")
    print("4. Exit")
    
    choice= int(input("enter choice number:"))
    if choice==1:
        a=int(input("Enter any number:"))
        dummy_list.append(a)
    elif choice==2:
        if dummy_list==[]:
            print("Stack Empty-underflow")
        else:
            print("Deleted element is:", dummy_list.pop())
    elif choice==3:
        length=len(dummy_list)
        if length == 0: 
            print("Stack Empty Underflow")
        else:
            for i in range (length -1, -1,-1):
                print(dummy_list[i])
    elif choice==4:
        break
    else:
        print("Invalid Input.")