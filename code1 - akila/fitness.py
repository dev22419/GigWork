def main():

 current_user=""   # store current logged in user
    
 while True:
        
        # check login status
        if current_user=="" :

            print("--- Fitness Tracker ---")
            print("1.Login")
            print("2. Register ")
            print("3. Exit")
            choice=input("Enter choice: ")

            # login part
            if choice=="1" :

                u=input("Username: ")
                p=input("Password: ")
                found=False   # check if user found
                
                try:
                        f=open("users.txt","r")   # open user file

                        for line in f :
                            parts=line.strip().split(",")
                            
                            # match username and password
                            if len(parts)>=2 and parts[0]==u and parts[1]==p :
                                    found=True
                                    # forgot break here maybe

                        f.close()
                except:
                        pass   # file may not exist
                
                if found==True :
                        current_user=u   # set current user
                        print("Login success\n")
                else:
                        print("Wrong username/password\n")
                    
            # register new user
            elif choice=="2":

                u=input("New Username: ")
                p=input("New Password: ")

                if u!="" and p!="" :
                        f=open("users.txt","a")   # append mode
                        f.write(u+","+p+"\n")
                        f.close()
                        print("Registered!\n")
                else:
                        print("Empty fields not allowed\n")
                    
            # exit program
            elif choice=="3":
                    print("Bye")
                    break

            else:
                print("invalid choice\n")

        else:

            # main menu after login
            print("\n--- Main Menu ---")
            print("User :"+current_user)
            print("1.View Dashboard")
            print("2.Log Activity")
            print("3.Log Food")
            print("4.Goals")
            print("5.History")
            print("6.Saved Stuff")
            print("7.Logout")

            choice = input("Enter choice: ")
            
            # dashboard section
            if choice=="1":

                act_count=0   # total activities
                dur_total=0
                cal_burn=0
                steps_total=0
                
                try:
                    f=open("goals.txt","r")

                    for line in f:
                        parts=line.strip().split(",")
                        
                        # calculate totals
                        if len(parts)>=6 and parts[0]==current_user:
                            act_count=act_count+1
                            dur_total+=float(parts[2])
                            cal_burn+=float(parts[4])
                            steps_total+=int(parts[5])

                    f.close()
                except:
                    pass

                cal_cons=0
                
                try:
                    f=open("nut.txt","r")

                    for line in f:
                        parts=line.strip().split(",")
                        if len(parts)>=5 and parts[0]==current_user:
                            cal_cons+=float(parts[1])

                    f.close()
                except:
                    pass
                
                # print summary
                print("\n-- Dashboard --")
                print("Workouts:",act_count)
                print("Duration:",dur_total,"mins")
                print("Steps:",steps_total)
                print("Burned:",cal_burn)
                print("Consumed:",cal_cons)

                print("\nGoals:")
                
                try:
                    f=open("goals.txt","r")

                    for line in f:
                        parts=line.strip().split(",")
                        # show goals
                        if len(parts)>=4 and parts[0]==current_user:
                            print(parts[1],parts[2],parts[3])

                    f.close()
                except:
                    pass
                    
            # log activity
            elif choice=="2":

                print("\nLog Activity")
                t=input("Type:")
                d=input("Duration:")
                i=input("Intensity:")
                cal=input("Calories:")
                s=input("Steps:")

                try:
                    float(d)
                    float(cal)
                    int(s)

                    f=open("act.txt","a")   # save activity
                    f.write(current_user+","+t+","+d+","+i+","+cal+","+s+"\n")
                    f.close()

                    print("Saved!")

                except:
                    print("Error numbers only")
                
            # log food
            elif choice=="3":

                print("\nFood Log")
                cal=input("Calories:")
                carb=input("Carbs:")
                pro=input("Protein:")
                fat=input("Fat:")

                try:
                    float(cal);float(carb);float(pro);float(fat)

                    f=open("nut.txt","a")   # save food data
                    f.write(current_user+","+cal+","+carb+","+pro+","+fat+"\n")
                    f.close()

                    print("Saved food")

                except:
                    print("error input")
                
            # manage goals
            elif choice=="4":

                print("1 burn goal")
                print("2 eat goal")

                gc=input("choice:")

                target=input("target:")

                try:
                    float(target)

                    f=open("goals.txt","a")   # just append goal
                    f.write(current_user+",goal,"+target+",0\n")
                    f.close()

                    print("goal set")

                except:
                    print("wrong input")

            # view history
            elif choice=="5":

                print("\nActivity History")
                
                try:
                    f=open("act.txt","r")

                    for line in f:
                        if current_user in line:   # simple check
                            print(line)

                    f.close()
                except:
                    print("no data")

                print("\nFood History")

                try:
                    f=open("nut.txt","r")

                    for line in f:
                        if current_user in line:
                            print(line)

                    f.close()
                except:
                    print("no data")

            # saved routines / meals
            elif choice=="6":

                print("1 workout")
                print("2 meal")
                rc=input("choice:")

                name=input("name:")
                desc=input("desc:")

                f=open("routines.txt","a")   # save routine or meal
                f.write(current_user+","+rc+","+name+","+desc+"\n")
                f.close()

                print("saved")

            # logout
            elif choice=="7":

                current_user=""   # reset user
                print("logout done")
                
            else:
                print("wrong option")


# start program
if __name__=="__main__":
    main()