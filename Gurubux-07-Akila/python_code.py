from tkinter import *

window_main = Tk()
window_main.title("My Personal Fitness Tracking System")
window_main.geometry("600x600")

user_session_id = "" # holds username 10th grade style comment: simple holder

def action_sign_in():
    global user_session_id
    u_val = box_user_name.get().strip()
    p_val = box_user_pass.get().strip()
    
    try:
        f_handler = open("accounts.csv", "r")
        rows_all = f_handler.readlines()
        f_handler.close()
        
        ok_status = False
        # loop fast check accurate 10th grade comment: loops threw lines
        for r in rows_all:
             data_items = r.strip().split(",")
             if len(data_items) >= 2 and data_items[0] == u_val and data_items[1] == p_val:
                  ok_status = True
                  break
                  
        if ok_status:
             user_session_id = u_val
             frame_gate.grid_forget()
             action_load_stats() # load stats first
             frame_stats.grid(row=0, column=0, padx=20, pady=20)
        else:
             label_msg.config(text="Wrong Login Try Again")
    except:
        label_msg.config(text="File Missing Register First")

def action_register():
    u_val = box_user_name.get().strip()
    p_val = box_user_pass.get().strip()
    w_val = box_user_mass.get().strip() 
    
    if u_val == "" or p_val == "" or w_val == "":
         label_msg.config(text="Enter All Fields Pls")
         return
         
    try:
        float(w_val)
    except:
         label_msg.config(text="Weight Must Be Number")
         return
         
    f_handler = open("accounts.csv", "a")
    f_handler.write(u_val + "," + p_val + "," + w_val + "\n")
    f_handler.close()
    
    label_msg.config(text="Registration Done Now Login")

def action_save_workout():
    v_act = box_activity.get().strip()
    v_dur = box_mins.get().strip()
    v_int = box_intensity.get().strip()
    v_steps = box_steps_count.get().strip()
    v_date = box_date_act.get().strip() # manual date entry
    
    if v_act == "" or v_dur == "" or v_int == "" or v_steps == "" or v_date == "":
         text_feedback.insert(END, "\nEnter Activity Details With Date\n")
         return
         
    try:
        float(v_dur)
        int(v_steps)
    except:
         text_feedback.insert(END, "\nDuration and Steps Must Be Number\n")
         return
         
    f_handler = open("tracker_logs.csv", "a")
    f_handler.write(user_session_id + "," + v_date + ",WORKOUT," + v_act + "," + v_dur + "," + v_int + "," + v_steps + "\n")
    f_handler.close()
    
    text_feedback.insert(END, "\nActivity Saved Ok\n")
    action_load_stats()

def action_save_meal():
    v_food = box_meal.get().strip()
    v_cal = box_cals.get().strip()
    v_carb = box_carbs_g.get().strip()
    v_prot = box_protein_g.get().strip()
    v_fat = box_lipid_g.get().strip()
    v_date = box_date_food.get().strip() # manual date entry
    
    if v_food == "" or v_cal == "" or v_carb == "" or v_prot == "" or v_fat == "" or v_date == "":
         text_feedback.insert(END, "\nEnter Food Data and Date\n")
         return
         
    try:
        float(v_cal)
        float(v_carb)
        float(v_prot)
        float(v_fat)
    except:
         text_feedback.insert(END, "\nNumbers Only For Macros and Calories\n")
         return
         
    f_handler = open("tracker_logs.csv", "a")
    f_handler.write(user_session_id + "," + v_date + ",MEAL," + v_food + "," + v_cal + "," + v_carb + "," + v_prot + "," + v_fat + "\n")
    f_handler.close()
    
    text_feedback.insert(END, "\nFood Saved Ok\n")
    action_load_stats()

def action_save_target():
    v_kind = box_target_kind.get().strip()
    v_num = box_target_num.get().strip()
    
    if v_kind == "" or v_num == "":
         goal_msg_label.config(text="Enter Goal Details")
         return
         
    try:
        float(v_num)
    except:
         goal_msg_label.config(text="Goal Must Be Number")
         return
         
    f_handler = open("target_logs.csv", "a")
    f_handler.write(user_session_id + "," + v_kind + "," + v_num + "\n")
    f_handler.close()
    goal_msg_label.config(text="Goal Saved Ok")
    action_load_stats()

def action_load_stats():
    text_dashboard.delete(1.0, END)
    
    g_steps = 0
    g_cals_burn = 0
    g_cals_eat = 0
    g_prot = 0
    g_carb = 0
    g_lipid = 0
    
    view_date = date_load_box.get().strip() 
    if view_date == "":
         text_dashboard.insert(END, "--- SELECT DATE TO LOAD ---\nType Date Below & Press Load Button!\n")
         return

    user_weight = 70.0 
    try:
         f_handler = open("accounts.csv", "r")
         for row in f_handler:
              data_items = row.strip().split(",")
              if len(data_items) >= 3 and data_items[0] == user_session_id:
                   user_weight = float(data_items[2])
         f_handler.close()
    except: pass

    try:
         f_handler = open("tracker_logs.csv", "r")
         for row in f_handler:
              data_items = row.strip().split(",")
              if len(data_items) > 1 and data_items[0] == user_session_id:
                   row_date = data_items[1]
                   type_row = data_items[2]
                   
                   if row_date == view_date:
                        if type_row == "WORKOUT":
                             dur = float(data_items[4])
                             int_val = data_items[5].lower()
                             steps = int(data_items[6]) if len(data_items) > 6 else 0
                             g_steps += steps
                             
                             met = 3.0 
                             if int_val == "high": met = 8.0
                             if int_val == "medium" or int_val == "med": met = 5.0
                             
                             cal_burn = met * user_weight * (dur / 60.0)
                             g_cals_burn += cal_burn
                             
                        elif type_row == "MEAL":
                             g_cals_eat += float(data_items[4])
                             g_carb += float(data_items[5])
                             g_prot += float(data_items[6])
                             g_lipid += float(data_items[7])
         f_handler.close()
    except: pass
    
    text_dashboard.insert(END, "--- SUMMARY STATS ---\n")
    text_dashboard.insert(END, "Date: " + view_date + "\n\n")
    text_dashboard.insert(END, "Total Steps: " + str(g_steps) + "\n")
    text_dashboard.insert(END, "Cals Burned: " + str(round(g_cals_burn, 1)) + "\n")
    text_dashboard.insert(END, "Cals Eaten: " + str(g_cals_eat) + "\n\n")
    text_dashboard.insert(END, "Macros (g):\n")
    text_dashboard.insert(END, " Carb: " + str(g_carb) + "g\n")
    text_dashboard.insert(END, " Prot: " + str(g_prot) + "g\n")
    text_dashboard.insert(END, " Fat: " + str(g_lipid) + "g\n\n")
    
    try:
         f_handler = open("target_logs.csv", "r")
         for row in f_handler:
              data_items = row.strip().split(",")
              if data_items[0] == user_session_id:
                   g_type_row = data_items[1].lower()
                   g_val_row = float(data_items[2])
                   
                   if g_type_row == "steps":
                        percent = (g_steps / g_val_row) * 100 if g_val_row > 0 else 100
                        text_dashboard.insert(END, "Steps Target: " + str(g_val_row) + "\n")
                        text_dashboard.insert(END, "Progress: " + str(round(percent, 1)) + "%\n\n")
                   if g_type_row == "calories":
                        percent = (g_cals_eat / g_val_row) * 100 if g_val_row > 0 else 100
                        text_dashboard.insert(END, "Calorie Target: " + str(g_val_row) + "\n")
                        text_dashboard.insert(END, "Progress: " + str(round(percent, 1)) + "%\n\n")
         f_handler.close()
    except: pass

def action_switch_screen(screen_to_show):
    frame_gate.grid_forget()
    frame_stats.grid_forget()
    frame_workout_meal.grid_forget()
    frame_goals_set.grid_forget()
    frame_view_plans.grid_forget()
    screen_to_show.grid(row=0, column=0, padx=20, pady=20)

# 1. LOGIN SCREEN
frame_gate = Frame(window_main)
frame_gate.grid(row=0, column=0, padx=50, pady=50)

Label(frame_gate , text="--- USER LOGIN ---").grid(row=0, column=0, columnspan=2)
Label(frame_gate , text="Username:").grid(row=1, column=0)
box_user_name = Entry(frame_gate)
box_user_name.grid(row=1, column=1)

Label(frame_gate , text="Password:").grid(row=2, column=0)
box_user_pass = Entry(frame_gate, show="*") 
box_user_pass.grid(row=2, column=1)

Label(frame_gate , text="Weight (kg):").grid(row=3, column=0)
box_user_mass = Entry(frame_gate)
box_user_mass.grid(row=3, column=1)

Button(frame_gate , text="Login", command=action_sign_in).grid(row=4, column=0)
Button(frame_gate , text="Register", command=action_register).grid(row=4, column=1)

label_msg = Label(frame_gate , text="", fg="red")
label_msg.grid(row=5, column=0, columnspan=2)

# 2. STATS (Dashboard) Frame
frame_stats = Frame(window_main)
text_dashboard = Text(frame_stats, height=12, width=50)
text_dashboard.grid(row=0, column=0, columnspan=2)

Label(frame_stats, text="Date (eg 24/03):").grid(row=1, column=0)
date_load_box = Entry(frame_stats)
date_load_box.grid(row=1, column=1)

Button(frame_stats, text="Load Data", command=action_load_stats).grid(row=2, column=0, columnspan=2)

Button(frame_stats, text="Log Workout", command=lambda: action_switch_screen(frame_workout_meal)).grid(row=3, column=0)
Button(frame_stats, text="Set Goals", command=lambda: action_switch_screen(frame_goals_set)).grid(row=3, column=1)
Button(frame_stats, text="View Plans", command=lambda: action_switch_screen(frame_view_plans)).grid(row=4, column=0)
Button(frame_stats, text="Logout", command=lambda: action_switch_screen(frame_gate)).grid(row=4, column=1)

# 3. LOG ACTIVITY / FOOD
frame_workout_meal = Frame(window_main)
Label(frame_workout_meal , text="-- LOG ACTIVITY --").grid(row=0, column=0, columnspan=2)

Label(frame_workout_meal , text="Date (eg 24/03)").grid(row=1, column=0)
box_date_act = Entry(frame_workout_meal)
box_date_act.grid(row=1, column=1)

Label(frame_workout_meal , text="Activity Type").grid(row=2, column=0)
box_activity = Entry(frame_workout_meal)
box_activity.grid(row=2, column=1)

Label(frame_workout_meal , text="Duration (mins)").grid(row=3, column=0)
box_mins = Entry(frame_workout_meal)
box_mins.grid(row=3, column=1)

Label(frame_workout_meal , text="Intensity").grid(row=4, column=0)
box_intensity = Entry(frame_workout_meal)
box_intensity.grid(row=4, column=1)

Label(frame_workout_meal , text="Steps").grid(row=5, column=0)
box_steps_count = Entry(frame_workout_meal)
box_steps_count.grid(row=5, column=1)

Button(frame_workout_meal , text="Save Activity", command=action_save_workout).grid(row=6, column=0, columnspan=2)

Label(frame_workout_meal , text="-- LOG FOOD --").grid(row=7, column=0, columnspan=2)
Label(frame_workout_meal , text="Date (eg 24/03)").grid(row=8, column=0)
box_date_food = Entry(frame_workout_meal)
box_date_food.grid(row=8, column=1)

Label(frame_workout_meal , text="Food Name").grid(row=9, column=0)
box_meal = Entry(frame_workout_meal)
box_meal.grid(row=9, column=1)

Label(frame_workout_meal , text="Calories").grid(row=10, column=0)
box_cals = Entry(frame_workout_meal)
box_cals.grid(row=10, column=1)

Label(frame_workout_meal , text="Carbs (g)").grid(row=11, column=0)
box_carbs_g = Entry(frame_workout_meal)
box_carbs_g.grid(row=11, column=1)

Label(frame_workout_meal , text="Protein (g)").grid(row=12, column=0)
box_protein_g = Entry(frame_workout_meal)
box_protein_g.grid(row=12, column=1)

Label(frame_workout_meal , text="Fat (g)").grid(row=13, column=0)
box_lipid_g = Entry(frame_workout_meal)
box_lipid_g.grid(row=13, column=1)

Button(frame_workout_meal , text="Save Food", command=action_save_meal).grid(row=14, column=0, columnspan=2)
Button(frame_workout_meal , text="Back to Stats", command=lambda: action_switch_screen(frame_stats)).grid(row=15, column=0, columnspan=2)

text_feedback = Text(frame_workout_meal , height=5 , width=40) 
text_feedback.grid(row=16, column=0, columnspan=2)

# 4. GOALS FRAME
frame_goals_set = Frame(window_main)
Label(frame_goals_set, text="-- SET GOALS --").grid(row=0, column=0, columnspan=2)
Label(frame_goals_set, text="Goal Type").grid(row=1, column=0)
box_target_kind = Entry(frame_goals_set)
box_target_kind.grid(row=1, column=1)

Label(frame_goals_set, text="Target Value").grid(row=2, column=0)
box_target_num = Entry(frame_goals_set)
box_target_num.grid(row=2, column=1)

Button(frame_goals_set, text="Save Goal", command=action_save_target).grid(row=3, column=0, columnspan=2)
Button(frame_goals_set, text="Back to Stats", command=lambda: action_switch_screen(frame_stats)).grid(row=4, column=0, columnspan=2)

goal_msg_label = Label(frame_goals_set, text="")
goal_msg_label.grid(row=5, column=0, columnspan=2)

# 5. PLANS FRAME
frame_view_plans = Frame(window_main)
Label(frame_view_plans, text="-- PLANS --").grid(row=0, column=0)

txt_advice = Text(frame_view_plans, height=12, width=50)
txt_advice.grid(row=1, column=0)
txt_advice.insert(END, "Plans:\n1. Fat Burn: Run\n2. Muscle: Weights\n")
txt_advice.config(state=DISABLED)

Button(frame_view_plans, text="Back to Stats", command=lambda: action_switch_screen(frame_stats)).grid(row=2, column=0)

if __name__ == "__main__":
    window_main.mainloop()