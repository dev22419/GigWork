from tkinter import *

appWindow = Tk()
appWindow.title("My Simple Fitness Tracker App Without Much Functions")
appWindow.geometry("600x600")

logged_user_ref = "" # this will store current user name 10th grade style

def handler_login():
    global logged_user_ref
    entered_u = tb_user.get().strip()
    entered_p = tb_pass.get().strip()
    
    try:
        file_obj = open("user_database.csv", "r")
        records = file_obj.readlines()
        file_obj.close()
        
        is_match = False
        # loop through records now very fast for checking accurate
        for row in records:
             tokens = row.strip().split(",")
             if len(tokens) >= 2 and tokens[0] == entered_u and tokens[1] == entered_p:
                  is_match = True
                  break
                  
        if is_match:
             logged_user_ref = entered_u
             screen_login.pack_forget()
             handler_load_summary() # update summary screen first
             screen_dashboard.pack()
        else:
             status_msg.config(text="Wrong Login Try Again")
    except:
        status_msg.config(text="File Database Missing, Register First")

def handler_register():
    entered_u = tb_user.get().strip()
    entered_p = tb_pass.get().strip()
    entered_w = tb_mass.get().strip() # added weight for calories math
    
    if entered_u == "" or entered_p == "" or entered_w == "":
         status_msg.config(text="Enter All Fields Pls")
         return
         
    try:
        float(entered_w)
    except:
         status_msg.config(text="Weight Must Be Number")
         return
         
    file_obj = open("user_database.csv", "a")
    file_obj.write(entered_u + "," + entered_p + "," + entered_w + "\n")
    file_obj.close()
    
    status_msg.config(text="Registration Done Now Login")

def handler_save_activity():
    val_act = tb_activity.get().strip()
    val_dur = tb_mins.get().strip()
    val_int = tb_intensity.get().strip()
    val_steps = tb_steps_count.get().strip()
    val_date = tb_date_act.get().strip() # manual date entry
    
    if val_act == "" or val_dur == "" or val_int == "" or val_steps == "" or val_date == "":
         txt_feedback.insert(END, "\nEnter Activity Details With Date\n")
         return
         
    try:
        float(val_dur)
        int(val_steps)
    except:
         txt_feedback.insert(END, "\nDuration and Steps Must Be Number\n")
         return
         
    file_obj = open("tracking_database.csv", "a")
    # loops threw data for saveing
    file_obj.write(logged_user_ref + "," + val_date + ",ACT," + val_act + "," + val_dur + "," + val_int + "," + val_steps + "\n")
    file_obj.close()
    
    txt_feedback.insert(END, "\nActivity Saved Ok\n")
    handler_load_summary()

def handler_save_food():
    val_food = tb_meal.get().strip()
    val_cal = tb_cals.get().strip()
    val_carb = tb_carbs_g.get().strip()
    val_prot = tb_protein_g.get().strip()
    val_fat = tb_lipid_g.get().strip()
    val_date = tb_date_food.get().strip() # manual date entry
    
    if val_food == "" or val_cal == "" or val_carb == "" or val_prot == "" or val_fat == "" or val_date == "":
         txt_feedback.insert(END, "\nEnter Food Data and Date\n")
         return
         
    try:
        float(val_cal)
        float(val_carb)
        float(val_prot)
        float(val_fat)
    except:
         txt_feedback.insert(END, "\nNumbers Only For Macros and Calories\n")
         return
         
    file_obj = open("tracking_database.csv", "a")
    file_obj.write(logged_user_ref + "," + val_date + ",FOOD," + val_food + "," + val_cal + "," + val_carb + "," + val_prot + "," + val_fat + "\n")
    file_obj.close()
    
    txt_feedback.insert(END, "\nFood Saved Ok\n")
    handler_load_summary()

def handler_save_goal():
    kind_g = tb_goal_kind.get().strip()
    num_g = tb_goal_num.get().strip()
    
    if kind_g == "" or num_g == "":
         goal_feedback_msg.config(text="Enter Goal Details")
         return
         
    try:
        float(num_g)
    except:
         goal_feedback_msg.config(text="Goal Must Be Number")
         return
         
    file_obj = open("goal_database.csv", "a")
    file_obj.write(logged_user_ref + "," + kind_g + "," + num_g + "\n")
    file_obj.close()
    goal_feedback_msg.config(text="Goal Saved Ok")
    handler_load_summary()

def handler_load_summary():
    txt_dashboard.delete(1.0, END)
    
    sum_steps = 0
    sum_cal_burn = 0
    sum_cal_food = 0
    sum_protein = 0
    sum_carbs = 0
    sum_fat = 0
    
    selected_date = date_load_box.get().strip() 
    if selected_date == "":
         txt_dashboard.insert(END, "--- SELECT DATE TO LOAD ---\nType Date Below & Press Load Button!\n")
         return

    user_weight = 70.0 
    try:
         file_obj = open("user_database.csv", "r")
         for row in file_obj:
              tokens = row.strip().split(",")
              if len(tokens) >= 3 and tokens[0] == logged_user_ref:
                   user_weight = float(tokens[2])
         file_obj.close()
    except: pass

    try:
         file_obj = open("tracking_database.csv", "r")
         for row in file_obj:
              tokens = row.strip().split(",")
              if len(tokens) > 1 and tokens[0] == logged_user_ref:
                   row_date = tokens[1]
                   type_row = tokens[2]
                   
                   if row_date == selected_date:
                        if type_row == "ACT":
                             dur = float(tokens[4])
                             int_val = tokens[5].lower()
                             steps = int(tokens[6]) if len(tokens) > 6 else 0
                             sum_steps += steps
                             
                             met = 3.0 
                             if int_val == "high": met = 8.0
                             if int_val == "medium" or int_val == "med": met = 5.0
                             
                             cal_burn = met * user_weight * (dur / 60.0)
                             sum_cal_burn += cal_burn
                             
                        elif type_row == "FOOD":
                             sum_cal_food += float(tokens[4])
                             sum_carbs += float(tokens[5])
                             sum_protein += float(tokens[6])
                             sum_fat += float(tokens[7])
         file_obj.close()
    except: pass
    
    txt_dashboard.insert(END, "--- SUMMARY DASHBOARD ---\n")
    txt_dashboard.insert(END, "Date: " + selected_date + "\n\n")
    txt_dashboard.insert(END, "Steps Walked: " + str(sum_steps) + "\n")
    txt_dashboard.insert(END, "Calories Burned: " + str(round(sum_cal_burn, 1)) + "\n")
    txt_dashboard.insert(END, "Calories Eaten: " + str(sum_cal_food) + "\n\n")
    txt_dashboard.insert(END, "Macros (Gramms):\n")
    txt_dashboard.insert(END, " Carb: " + str(sum_carbs) + "g\n")
    txt_dashboard.insert(END, " Prot: " + str(sum_protein) + "g\n")
    txt_dashboard.insert(END, " Fat: " + str(sum_fat) + "g\n\n")
    
    try:
         file_obj = open("goal_database.csv", "r")
         for row in file_obj:
              tokens = row.strip().split(",")
              if tokens[0] == logged_user_ref:
                   g_type_row = tokens[1].lower()
                   g_val_row = float(tokens[2])
                   
                   if g_type_row == "steps":
                        percent = (sum_steps / g_val_row) * 100 if g_val_row > 0 else 100
                        txt_dashboard.insert(END, "Steps Goal Target: " + str(g_val_row) + "\n")
                        txt_dashboard.insert(END, "Progress: " + str(round(percent, 1)) + "%\n\n")
                   if g_type_row == "calories":
                        percent = (sum_cal_food / g_val_row) * 100 if g_val_row > 0 else 100
                        txt_dashboard.insert(END, "Calorie Eat Target: " + str(g_val_row) + "\n")
                        txt_dashboard.insert(END, "Progress: " + str(round(percent, 1)) + "%\n\n")
         file_obj.close()
    except: pass

def handler_switch_screen(screen_to_show):
    screen_login.pack_forget()
    screen_dashboard.pack_forget()
    screen_activity_food.pack_forget()
    screen_goals.pack_forget()
    screen_plans.pack_forget()
    screen_to_show.pack()

# LOGIN SCREEN
screen_login = Frame(appWindow)
screen_login.pack()

Label(screen_login , text="--- USER LOGIN ---").pack()
Label(screen_login , text="Username Here").pack()
tb_user = Entry(screen_login)
tb_user.pack()

Label(screen_login , text="Password Here").pack()
tb_pass = Entry(screen_login, show="*") 
tb_pass.pack()

Label(screen_login , text="Weight (kg) for Signup").pack()
tb_mass = Entry(screen_login)
tb_mass.pack()

Button(screen_login , text="Login Now Pls", command=handler_login).pack()
Button(screen_login , text="Register Now Pls", command=handler_register).pack()

status_msg = Label(screen_login , text="", fg="red")
status_msg.pack()

# DASHBOARD Frame
screen_dashboard = Frame(appWindow)
txt_dashboard = Text(screen_dashboard, height=12, width=50)
txt_dashboard.pack()

Label(screen_dashboard, text="Enter Date to load (eg 24/03)").pack()
date_load_box = Entry(screen_dashboard)
date_load_box.pack()

Button(screen_dashboard, text="Load Summary Data", command=handler_load_summary).pack()

Button(screen_dashboard, text="Log Activity/Work", command=lambda: handler_switch_screen(screen_activity_food)).pack()
Button(screen_dashboard, text="Set Goals", command=lambda: handler_switch_screen(screen_goals)).pack()
Button(screen_dashboard, text="View Workout/Meal Plans", command=lambda: handler_switch_screen(screen_plans)).pack()
Button(screen_dashboard, text="Logout", command=lambda: handler_switch_screen(screen_login)).pack() # OOPS wait, summaryFrame is not defined in this code!

# LOG ACTIVITY / FOOD
screen_activity_food = Frame(appWindow)
Label(screen_activity_food , text="-- LOG ACTIVITY --").pack()

Label(screen_activity_food , text="Date (eg 24/03)").pack()
tb_date_act = Entry(screen_activity_food)
tb_date_act.pack()

Label(screen_activity_food , text="Activity Type (eg Running)").pack()
tb_activity = Entry(screen_activity_food)
tb_activity.pack()

Label(screen_activity_food , text="Duration Time (minutes)").pack()
tb_mins = Entry(screen_activity_food)
tb_mins.pack()

Label(screen_activity_food , text="Intensity Level (Low/Mid/High)").pack()
tb_intensity = Entry(screen_activity_food)
tb_intensity.pack()

Label(screen_activity_food , text="Steps Count").pack()
tb_steps_count = Entry(screen_activity_food)
tb_steps_count.pack()

Button(screen_activity_food , text="Save Activity Now", command=handler_save_activity).pack()

Label(screen_activity_food , text="-- LOG FOOD --").pack()
Label(screen_activity_food , text="Date (eg 24/03)").pack()
tb_date_food = Entry(screen_activity_food)
tb_date_food.pack()

Label(screen_activity_food , text="Food Name").pack()
tb_meal = Entry(screen_activity_food)
tb_meal.pack()

Label(screen_activity_food , text="Calories Number").pack()
tb_cals = Entry(screen_activity_food)
tb_cals.pack()

Label(screen_activity_food , text="Carbs (g)").pack()
tb_carbs_g = Entry(screen_activity_food)
tb_carbs_g.pack()

Label(screen_activity_food , text="Protein (g)").pack()
tb_protein_g = Entry(screen_activity_food)
tb_protein_g.pack()

Label(screen_activity_food , text="Fat (g)").pack()
tb_lipid_g = Entry(screen_activity_food)
tb_lipid_g.pack()

Button(screen_activity_food , text="Save Food Now", command=handler_save_food).pack()
Button(screen_activity_food , text="Back to Dashboard", command=lambda: handler_switch_screen(screen_dashboard)).pack()

txt_feedback = Text(screen_activity_food , height=5 , width=50) 
txt_feedback.pack()

# GOALS FRAME
screen_goals = Frame(appWindow)
Label(screen_goals, text="-- SET GOALS --").pack()
Label(screen_goals, text="Goal Type (Steps or Calories)").pack()
tb_goal_kind = Entry(screen_goals)
tb_goal_kind.pack()

Label(screen_goals, text="Target Number Value").pack()
tb_goal_num = Entry(screen_goals)
tb_goal_num.pack()

Button(screen_goals, text="Save Goal Now", command=handler_save_goal).pack()
Button(screen_goals, text="Back to Dashboard", command=lambda: handler_switch_screen(screen_dashboard)).pack()

goal_feedback_msg = Label(screen_goals, text="")
goal_feedback_msg.pack()

# PLANS FRAME
screen_plans = Frame(appWindow)
Label(screen_plans, text="-- WORKOUT & MEAL PLANS --").pack()

txt_advice = Text(screen_plans, height=15, width=50)
txt_advice.pack()
txt_advice.insert(END, "Personalised Fitness Plan Recommendation:\n\n")
txt_advice.insert(END, "1. Fat Burn Plan:\n   Workout: 30 min Running, 15 min Weights\n   Meal: Low Carb (Eggs, Chicken, Salad)\n\n")
txt_advice.insert(END, "2. Muscle Gain Plan:\n   Workout: 45 min Strength Training\n   Meal: High Protein (Steak, Protein Shake)\n\n")
txt_advice.config(state=DISABLED)

Button(screen_plans, text="Back to Dashboard", command=lambda: handler_switch_screen(screen_dashboard)).pack()

if __name__ == "__main__":
    appWindow.mainloop()