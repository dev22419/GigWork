from tkinter import *  

# making window
WinMainAPP = Tk()
WinMainAPP.title("fitness tracker thing")  


# global user
current_user_value = ""  

# login function
def loginNOW():  

 global current_user_value  

 u = user_input_box.get().strip()
 p = pass_input_box.get().strip()

 try:
  # open users file to read credentials
  f = open("users.txt" , "r")
  data = f.read().strip()
  f.close()

  # simple check (not perfect but ok)
  if u in data and p in data:
        current_user_value = u  
        loginFrame.pack_forget()
        menuFrame.pack()
  else:
     msg_label.config(text="wrong login try again")

 except:
   msg_label.config(text="file not found")  



# register
def registerNOW():  
 """registering new user"""
 u = user_input_box.get().strip()
 p = pass_input_box.get().strip()

 if u == "" or p == "":
     msg_label.config(text="enter all fields pls")
     return  

 f = open("users.txt","a")

 # saving user
 f.write(u + "," + p + "\n")

 f.close()

 msg_label.config(text="registered done now login")  



# save activity
def saveAct():  

 act_val = act_box.get().strip()
 dur_val = dur_box.get().strip()
 int_val = int_box.get().strip()

 if act_val == "" or dur_val == "" or int_val == "":
      output_box.insert(END,"\nenter activity full\n")
      return  

 f = open("fitness.txt","a")

 f.write(current_user_value + ",ACT," + act_val + "," + dur_val + "," + int_val + "\n")

 f.close()

 output_box.insert(END,"\nactivity saved ok\n")  



# save food
def saveFoodNOW():  

 food_val = food_box.get().strip()
 cal_val = cal_box.get().strip()

 if food_val == "" or cal_val == "":
     output_box.insert(END,"\nenter food data\n")
     return  

 f = open("fitness.txt","a")

 f.write(current_user_value + ",FOOD," + food_val + "," + cal_val + "\n")

 f.close()

 output_box.insert(END,"\nfood saved ok\n")  



# view data
def showDataNOW():  

 output_box.delete(1.0 , END)

 try:
   f = open("fitness.txt","r")
   data_all = f.read().strip()
   f.close()

   if data_all == "":
        output_box.insert(END,"no data yet")
        return  
   """viewing data"""
   lines = data_all.split("\n")

   i = 0  

   while i < len(lines):

        # checking current user
        if current_user_value in lines[i]:
            output_box.insert(END , lines[i] + "\n")

        i = i + 1  

 except:
   output_box.insert(END,"file missing")  



# LOGIN 
loginFrame = Frame(WinMainAPP)
loginFrame.pack()

"""login screen"""
Label(loginFrame , text="username here").pack()
user_input_box = Entry(loginFrame)
user_input_box.pack()

"""password screen"""
Label(loginFrame , text="password here").pack()
pass_input_box = Entry(loginFrame)
pass_input_box.pack()

"""login button"""
Button(loginFrame , text="login now pls", command=loginNOW).pack()

"""register button"""
Button(loginFrame , text="register now pls", command=registerNOW).pack()

"""message label"""
msg_label = Label(loginFrame , text="")
msg_label.pack()



# MENU 
menuFrame = Frame(WinMainAPP)

"""activity type"""
Label(menuFrame , text="activity type").pack()
act_box = Entry(menuFrame)
act_box.pack()

"""duration time"""
Label(menuFrame , text="duration time").pack()
dur_box = Entry(menuFrame)
dur_box.pack()

Label(menuFrame , text="intensity level").pack()
int_box = Entry(menuFrame)
int_box.pack()

Button(menuFrame , text="save activity now", command=saveAct).pack()


Label(menuFrame , text="food name").pack()
food_box = Entry(menuFrame)
food_box.pack()

# calories number 
Label(menuFrame , text="calories number").pack()
cal_box = Entry(menuFrame)
cal_box.pack()

Button(menuFrame , text="save food now", command=saveFoodNOW).pack()

Button(menuFrame , text="view progress data", command=showDataNOW).pack()

output_box = Text(menuFrame , height=15 , width=50)
output_box.pack()


if __name__ == "__main__":
    WinMainAPP.mainloop()