from tkinter import *

WinMainAPP = Tk()
WinMainAPP.title("fitness tracker thing")
WinMainAPP.geometry("600x600") # made it bigger becaus of more stuff

current_user_value = "" # global user for later

# login function
def loginNOW():
    global current_user_value
    u = user_input_box.get().strip()
    p = pass_input_box.get().strip()
    
    try:
        f = open("users.txt", "r")
        lines = f.readlines()
        f.close()
        
        found = False
        # loop over lines now very fast for checking accurate
        for line in lines:
             parts = line.strip().split(",")
             if len(parts) >= 2 and parts[0] == u and parts[1] == p:
                  found = True
                  break
                  
        if found:
             current_user_value = u
             loginFrame.pack_forget()
             summaryFrame_load() # update summary screen first
             summaryFrame.pack()
        else:
             msg_label.config(text="wrong login try again")
    except:
        msg_label.config(text="file missing, register first")

def registerNOW():
    u = user_input_box.get().strip()
    p = pass_input_box.get().strip()
    w = weight_input_box.get().strip() # added weight for calories math
    
    # checking all boxes is full
    if u == "" or p == "" or w == "":
         msg_label.config(text="enter all fields pls")
         return
         
    # check if weight is number so it doesnt crash
    try:
        float(w)
    except:
         msg_label.config(text="weight must be number")
         return
         
    f = open("users.txt", "a")
    f.write(u + "," + p + "," + w + "\n")
    f.close()
    
    msg_label.config(text="registered done now login")

# save activity
def saveAct():
    act_val = act_box.get().strip()
    dur_val = dur_box.get().strip()
    int_val = int_box.get().strip()
    steps_val = steps_box.get().strip()
    date_val = date_act_box.get().strip() # manual date entry 10th grade
    
    if act_val == "" or dur_val == "" or int_val == "" or steps_val == "" or date_val == "":
         output_box.insert(END, "\nenter activity details with date\n")
         return
         
    try:
        float(dur_val)
        int(steps_val)
    except:
         output_box.insert(END, "\nduration and steps must be number\n")
         return
         
    f = open("fitness.txt", "a")
    # saveing data with date and steps too now
    f.write(current_user_value + "," + date_val + ",ACT," + act_val + "," + dur_val + "," + int_val + "," + steps_val + "\n")
    f.close()
    
    output_box.insert(END, "\nactivity saved ok\n")
    summaryFrame_load() # reload summary maths

# save food
def saveFoodNOW():
    food_val = food_box.get().strip()
    cal_val = cal_box.get().strip()
    carb_val = carb_box.get().strip()
    prot_val = prot_box.get().strip()
    fat_val = fat_box.get().strip()
    date_val = date_food_box.get().strip() # manual date entry
    
    if food_val == "" or cal_val == "" or carb_val == "" or prot_val == "" or fat_val == "" or date_val == "":
         output_box.insert(END, "\nenter food data and date\n")
         return
         
    try:
        float(cal_val)
        float(carb_val)
        float(prot_val)
        float(fat_val)
    except:
         output_box.insert(END, "\nnumbers only for macros and calories\n")
         return
         
    f = open("fitness.txt", "a")
    f.write(current_user_value + "," + date_val + ",FOOD," + food_val + "," + cal_val + "," + carb_val + "," + prot_val + "," + fat_val + "\n")
    f.close()
    
    output_box.insert(END, "\nfood saved ok\n")
    summaryFrame_load()

def saveGoalNOW():
    g_type = goal_type_box.get().strip()
    g_val = goal_val_box.get().strip()
    
    if g_type == "" or g_val == "":
         goal_msg_label.config(text="enter goal details")
         return
         
    try:
        float(g_val)
    except:
         goal_msg_label.config(text="goal must be number")
         return
         
    f = open("goals.txt", "a")
    f.write(current_user_value + "," + g_type + "," + g_val + "\n")
    f.close()
    goal_msg_label.config(text="goal saved ok")
    summaryFrame_load()

def summaryFrame_load():
    summary_text.delete(1.0, END)
    
    tot_steps = 0
    tot_cal_burn = 0
    tot_cal_food = 0
    tot_protein = 0
    tot_carbs = 0
    tot_fat = 0
    
    # manual date matching from load box
    today_str = date_load_box.get().strip() 
    if today_str == "":
         summary_text.insert(END, "--- SELECT DATE TO LOAD ---\nType date like 24/03 below and press Load!\n")
         return

    # get user weight
    user_weight = 70.0 
    try:
         f = open("users.txt", "r")
         for line in f:
              parts = line.strip().split(",")
              if len(parts) >= 3 and parts[0] == current_user_value:
                   user_weight = float(parts[2])
         f.close()
    except: pass

    try:
         f = open("fitness.txt", "r")
         for line in f:
              parts = line.strip().split(",")
              if len(parts) > 1 and parts[0] == current_user_value:
                   row_date = parts[1]
                   type_row = parts[2]
                   
                   # checks manual string match exactly
                   if row_date == today_str:
                        if type_row == "ACT":
                             dur = float(parts[4])
                             int_val = parts[5].lower()
                             steps = int(parts[6]) if len(parts) > 6 else 0
                             tot_steps += steps
                             
                             # calc calrys burn met factor logic
                             met = 3.0 # default
                             if int_val == "high": met = 8.0
                             if int_val == "medium" or int_val == "med": met = 5.0
                             
                             cal_burn = met * user_weight * (dur / 60.0)
                             tot_cal_burn += cal_burn
                             
                        elif type_row == "FOOD":
                             tot_cal_food += float(parts[4])
                             tot_carbs += float(parts[5])
                             tot_protein += float(parts[6])
                             tot_fat += float(parts[7])
         f.close()
    except: pass
    
    summary_text.insert(END, "--- SUMMARY SCREEN ---\n")
    summary_text.insert(END, "Date Selected: " + today_str + "\n\n")
    summary_text.insert(END, "Steps Walked: " + str(tot_steps) + "\n")
    summary_text.insert(END, "Calories Burned: " + str(round(tot_cal_burn, 1)) + "\n")
    summary_text.insert(END, "Calories Eaten: " + str(tot_cal_food) + "\n\n")
    summary_text.insert(END, "Macros (Gramms):\n")
    summary_text.insert(END, " Carb: " + str(tot_carbs) + "g\n")
    summary_text.insert(END, " Prot: " + str(tot_protein) + "g\n")
    summary_text.insert(END, " Fat: " + str(tot_fat) + "g\n\n")
    
    # loops threw goals to find progress percentage
    try:
         f = open("goals.txt", "r")
         for line in f:
              parts = line.strip().split(",")
              if parts[0] == current_user_value:
                   g_type_row = parts[1].lower()
                   g_val_row = float(parts[2])
                   
                   if g_type_row == "steps":
                        percent = (tot_steps / g_val_row) * 100 if g_val_row > 0 else 100
                        summary_text.insert(END, "Steps Goal Target: " + str(g_val_row) + "\n")
                        summary_text.insert(END, "Progress: " + str(round(percent, 1)) + "%\n\n")
                   if g_type_row == "calories":
                        percent = (tot_cal_food / g_val_row) * 100 if g_val_row > 0 else 100
                        summary_text.insert(END, "Calorie Eat Target: " + str(g_val_row) + "\n")
                        summary_text.insert(END, "Progress: " + str(round(percent, 1)) + "%\n\n")
         f.close()
    except: pass

def showFrame(frame_to_show):
    loginFrame.pack_forget()
    summaryFrame.pack_forget()
    menuFrame.pack_forget()
    goalFrame.pack_forget()
    planFrame.pack_forget()
    frame_to_show.pack()

# LOGIN SCREEN
loginFrame = Frame(WinMainAPP)
loginFrame.pack()

Label(loginFrame , text="--- USER LOGIN ---").pack()
Label(loginFrame , text="username here").pack()
user_input_box = Entry(loginFrame)
user_input_box.pack()

Label(loginFrame , text="password here").pack()
pass_input_box = Entry(loginFrame, show="*") 
pass_input_box.pack()

Label(loginFrame , text="weight (kg) for signup").pack()
weight_input_box = Entry(loginFrame)
weight_input_box.pack()

Button(loginFrame , text="login now pls", command=loginNOW).pack()
Button(loginFrame , text="register now pls", command=registerNOW).pack()

msg_label = Label(loginFrame , text="", fg="red")
msg_label.pack()

# SUMMARY Screen (Dashboard)
summaryFrame = Frame(WinMainAPP)
summary_text = Text(summaryFrame, height=12, width=50)
summary_text.pack()

Label(summaryFrame, text="Enter Date to load (eg 24/03)").pack()
date_load_box = Entry(summaryFrame)
date_load_box.pack()

Button(summaryFrame, text="Load Summary Data", command=summaryFrame_load).pack()

Button(summaryFrame, text="Log Activity/Work", command=lambda: showFrame(menuFrame)).pack()
Button(summaryFrame, text="Set Goals", command=lambda: showFrame(goalFrame)).pack()
Button(summaryFrame, text="View Workout/Meal Plans", command=lambda: showFrame(planFrame)).pack()
Button(summaryFrame, text="Logout", command=lambda: showFrame(loginFrame)).pack()

# LOG ACTIVITY (Menu Frame updated)
menuFrame = Frame(WinMainAPP)
Label(menuFrame , text="-- LOG ACTIVITY --").pack()

Label(menuFrame , text="Date (eg 24/03)").pack()
date_act_box = Entry(menuFrame)
date_act_box.pack()

Label(menuFrame , text="activity type (eg Running)").pack()
act_box = Entry(menuFrame)
act_box.pack()

Label(menuFrame , text="duration time (minutes)").pack()
dur_box = Entry(menuFrame)
dur_box.pack()

Label(menuFrame , text="intensity level (Low/Mid/High)").pack()
int_box = Entry(menuFrame)
int_box.pack()

Label(menuFrame , text="steps count").pack()
steps_box = Entry(menuFrame)
steps_box.pack()

Button(menuFrame , text="save activity now", command=saveAct).pack()

Label(menuFrame , text="-- LOG FOOD --").pack()
Label(menuFrame , text="Date (eg 24/03)").pack()
date_food_box = Entry(menuFrame)
date_food_box.pack()

Label(menuFrame , text="food name").pack()
food_box = Entry(menuFrame)
food_box.pack()

Label(menuFrame , text="calories number").pack()
cal_box = Entry(menuFrame)
cal_box.pack()

Label(menuFrame , text="Carbs (g)").pack()
carb_box = Entry(menuFrame)
carb_box.pack()

Label(menuFrame , text="Protein (g)").pack()
prot_box = Entry(menuFrame)
prot_box.pack()

Label(menuFrame , text="Fat (g)").pack()
fat_box = Entry(menuFrame)
fat_box.pack()

Button(menuFrame , text="save food now", command=saveFoodNOW).pack()
Button(menuFrame , text="Back to Summary", command=lambda: showFrame(summaryFrame)).pack()

output_box = Text(menuFrame , height=5 , width=50) 
output_box.pack()

# GOALS FRAME
goalFrame = Frame(WinMainAPP)
Label(goalFrame, text="-- SET GOALS --").pack()
Label(goalFrame, text="Goal Type (Steps or Calories)").pack()
goal_type_box = Entry(goalFrame)
goal_type_box.pack()

Label(goalFrame, text="Target Number Value").pack()
goal_val_box = Entry(goalFrame)
goal_val_box.pack()

Button(goalFrame, text="Save Goal Now", command=saveGoalNOW).pack()
Button(goalFrame, text="Back to Summary", command=lambda: showFrame(summaryFrame)).pack()

goal_msg_label = Label(goalFrame, text="")
goal_msg_label.pack()

# PLANS FRAME
planFrame = Frame(WinMainAPP)
Label(planFrame, text="-- WORKOUT & MEAL PLANS --").pack()

plan_text = Text(planFrame, height=15, width=50)
plan_text.pack()
plan_text.insert(END, "Personalised Fitness Plan Recommendation:\n\n")
plan_text.insert(END, "1. Fat Burn Plan:\n   Workout: 30 min Running, 15 min Weights\n   Meal: Low Carb (Eggs, Chicken, Salad)\n\n")
plan_text.insert(END, "2. Muscle Gain Plan:\n   Workout: 45 min Strength Training\n   Meal: High Protein (Steak, Protein Shake)\n\n")
plan_text.config(state=DISABLED)

Button(planFrame, text="Back to Summary", command=lambda: showFrame(summaryFrame)).pack()

if __name__ == "__main__":
    WinMainAPP.mainloop()