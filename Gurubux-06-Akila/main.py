from tkinter import *
from datetime import date

# simple files for this basic tracker
# i make some files here to save data
FILE_USERS = "ft_users.txt"
FILE_LOGS = "ft_logs.txt"
FILE_GOALS = "ft_goals.txt"

# todays date auto text
# get the date from system
TODAY = str(date.today())

# current session user
# who is using the app now
current_user = ""

# system setup and config finished
def make_files():
    # create files if not there
    # if files not exist then make them empty
    f1 = open(FILE_USERS, "a")
    f1.close()

    f2 = open(FILE_LOGS, "a")
    f2.close()

    f3 = open(FILE_GOALS, "a")
    f3.close()

# helper tools for validating inputs
def bad_text(v):
    # bad means empty or storage separators
    # check if user put weird symbols or nothing
    # reject empty string inputs
    if len(v) == 0:
        return True
    # prevent breaking pipe separated logs structure
    if "|" in v:
        return True
    if "\n" in v:
        return True
    return False

# check if we have a valid float number
def number_text(v):
    # simple number checker with max one dot
    # this function check if string is a number or not
    if len(v) == 0:
        return False

    i = 0
    dots = 0
    while i < len(v):
        ch = v[i]
        if ch == ".":
            dots = dots + 1
            if dots > 1:
                return False
        elif ch < "0" or ch > "9":
            return False
        i = i + 1

    return True

# functions to read and write from files
def read_user_map():
    # output: user -> {password, weight}
    # get all users from the file into a list or dict
    users = {}

    f = open(FILE_USERS, "r")
    lines = f.readlines()
    f.close()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        p = line.split("|")
        if len(p) >= 3:
            u = p[0]
            pw = p[1]
            w = p[2]
            if number_text(w):
                users[u] = {"password": pw, "weight": float(w)}
        i = i + 1

    return users

# update user file with new map data
def write_user_map(users):
    # rewrite full user file from dict
    # save the user data back to the disk
    f = open(FILE_USERS, "w")

    for uname in users:
        info = users[uname]
        row = uname + "|" + info["password"] + "|" + str(info["weight"]) + "\n"
        f.write(row)

    f.close()

# operations relating to goals fit tracker
def read_goal_map():
    # output: user -> {steps, calories}
    # read the goal file so we know what they want reach
    goals = {}

    f = open(FILE_GOALS, "r")
    lines = f.readlines()
    f.close()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        p = line.split("|")
        if len(p) >= 3:
            u = p[0]
            s = p[1]
            c = p[2]
            if number_text(s) and number_text(c):
                goals[u] = {"steps": float(s), "calories": float(c)}
        i = i + 1

    return goals

# write goals map back into memory disk
def write_goal_map(goals):
    # rewrite full goal file from dict
    # put the goals into the txt file
    f = open(FILE_GOALS, "w")

    for uname in goals:
        info = goals[uname]
        row = uname + "|" + str(info["steps"]) + "|" + str(info["calories"]) + "\n"
        f.write(row)

    f.close()

# row appenders for history logging
def append_activity_row(user_name, day_text, act_type, dur_text, intensity_text, steps_text):
    # A row format: A|user|date|type|duration|intensity|steps
    # just add one newline for new activity
    # open in append mode to preserve previous logs history
    f = open(FILE_LOGS, "a")
    row = "A|" + user_name + "|" + day_text + "|" + act_type + "|" + dur_text + "|" + intensity_text + "|" + steps_text + "\n"
    f.write(row)
    f.close()

# write food row into log structure
def append_food_row(user_name, day_text, food_name, cal_text, carb_text, prot_text, fat_text):
    # F row format: F|user|date|name|cal|carb|prot|fat
    # write food into log file
    f = open(FILE_LOGS, "a")
    row = "F|" + user_name + "|" + day_text + "|" + food_name + "|" + cal_text + "|" + carb_text + "|" + prot_text + "|" + fat_text + "\n"
    f.write(row)
    f.close()

# retrieval functions for user info
def get_weight_for_user(user_name):
    # read weight for calories burned math
    # i need weight or i cant calcuclate calories
    users = read_user_map()
    if user_name in users:
        return users[user_name]["weight"]
    return 70.0

# aggregate numbers for the main dashboard view
def get_today_data(user_name):
    # collect all today totals from log file
    # this loop look for everything user did today
    total_steps = 0.0
    total_burned = 0.0
    total_eaten = 0.0
    total_carb = 0.0
    total_prot = 0.0
    total_fat = 0.0

    weight = get_weight_for_user(user_name)

    log_text.delete("1.0", END)
    log_text.insert(END, "today entries\n")
    log_text.insert(END, "------------------------------\n")

    f = open(FILE_LOGS, "r")
    lines = f.readlines()
    f.close()

    show_count = 0
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        p = line.split("|")

        if len(p) >= 4:
            kind = p[0]
            uname = p[1]
            day = p[2]

            if uname == user_name and day == TODAY:
                if kind == "A" and len(p) >= 7:
                    act_type = p[3]
                    dur = p[4]
                    inten = p[5]
                    st = p[6]

                    if number_text(dur) and number_text(st):
                        dval = float(dur)
                        sval = float(st)
                        total_steps = total_steps + sval

                        # Metabolic Equivalent of Task rates
                        # higher intensity burns significantly more energy per minute
                        met = 3.0
                        if inten == "medium":
                            met = 5.0
                        elif inten == "high":
                            met = 8.0

                        # formula: MET * weight * duration_in_hours = calories burned
                        total_burned = total_burned + (met * weight * (dval / 60.0))

                        log_text.insert(END, "ACT  " + act_type + "  " + str(dval) + " min  " + inten + "  " + str(int(sval)) + " steps\n")
                        show_count = show_count + 1

                elif kind == "F" and len(p) >= 8:
                    # unpack food macros index map from row variables
                    fname = p[3]
                    cal = p[4]
                    carb = p[5]
                    prot = p[6]
                    fat = p[7]

                    if number_text(cal) and number_text(carb) and number_text(prot) and number_text(fat):
                        cval = float(cal)
                        carbv = float(carb)
                        protv = float(prot)
                        fatv = float(fat)

                        total_eaten = total_eaten + cval
                        total_carb = total_carb + carbv
                        total_prot = total_prot + protv
                        total_fat = total_fat + fatv

                        log_text.insert(END, "FOOD " + fname + "  " + str(cval) + " kcal  C" + str(carbv) + " P" + str(protv) + " F" + str(fatv) + "\n")
                        show_count = show_count + 1

        i = i + 1

    if show_count == 0:
        log_text.insert(END, "no entries today\n")

    return total_steps, total_burned, total_eaten, total_carb, total_prot, total_fat

# main trigger for refreshing the app text boxes
def refresh_summary_action():
    # update summary text and goals progress
    # clear the text box and put new numbers inside
    if len(current_user) == 0:
        summary_text.delete("1.0", END)
        summary_text.insert(END, "login first")
        return

    welcome_label.config(text="logged user: " + current_user)

    t_steps, t_burn, t_eat, t_carb, t_prot, t_fat = get_today_data(current_user)
    # calculate total balance (consumed minus spent)
    net = t_eat - t_burn

    summary_text.delete("1.0", END)
    summary_text.insert(END, "today: " + TODAY + "\n")
    summary_text.insert(END, "steps: " + str(int(t_steps)) + "\n")
    summary_text.insert(END, "burned kcal: " + str(round(t_burn, 1)) + "\n")
    summary_text.insert(END, "eaten kcal: " + str(round(t_eat, 1)) + "\n")
    summary_text.insert(END, "net kcal: " + str(round(net, 1)) + "\n")
    summary_text.insert(END, "carbs: " + str(round(t_carb, 1)) + " g\n")
    summary_text.insert(END, "protein: " + str(round(t_prot, 1)) + " g\n")
    summary_text.insert(END, "fat: " + str(round(t_fat, 1)) + " g\n")

    goals = read_goal_map()
    if current_user in goals:
        gs = goals[current_user]["steps"]
        gc = goals[current_user]["calories"]

        # percentage of goal reached for today
        step_p = 0.0
        cal_p = 0.0
        if gs > 0:
            step_p = (t_steps / gs) * 100.0
        if gc > 0:
            cal_p = (t_eat / gc) * 100.0

        summary_text.insert(END, "\n")
        summary_text.insert(END, "goal steps: " + str(int(gs)) + "  progress: " + str(int(step_p)) + "%\n")
        summary_text.insert(END, "goal calories: " + str(int(gc)) + "  progress: " + str(int(cal_p)) + "%\n")
    else:
        summary_text.insert(END, "\n")
        summary_text.insert(END, "goals not set yet\n")

    summary_text.insert(END, "\n")
    summary_text.insert(END, simple_plan_text(net))


def simple_plan_text(net_kcal):
    # simple static-like advice text
    # some advice based on calories balance
    if net_kcal > 300:
        return "plan: reduce snacks and add walk"
    if net_kcal < -300:
        return "plan: eat enough and recover"
    return "plan: keep same routine"


def login_click():
    # login existing account
    # check if user and pass match
    global current_user

    # pull strings and clean accidental spaces
    u = login_user_entry.get().strip()
    p = login_pass_entry.get().strip()

    users = read_user_map()
    if u in users and users[u]["password"] == p:
        current_user = u
        login_msg.config(text="")
        login_frame.pack_forget()
        app_frame.pack(padx=8, pady=8)
        refresh_summary_action()
    else:
        login_msg.config(text="wrong username or password")


def register_click():
    # create new account
    # make a new user if not already there
    u = login_user_entry.get().strip()
    p = login_pass_entry.get().strip()
    w = login_weight_entry.get().strip()

    if bad_text(u) or bad_text(p):
        login_msg.config(text="username/password invalid")
        return

    if len(p) < 4:
        login_msg.config(text="password too short")
        return

    if not number_text(w):
        login_msg.config(text="weight must be number")
        return

    wv = float(w)
    # validate that body weight is within human thresholds
    if wv < 25 or wv > 250:
        login_msg.config(text="weight out of range")
        return

    users = read_user_map()
    if u in users:
        login_msg.config(text="username already taken")
        return

    users[u] = {"password": p, "weight": wv}
    write_user_map(users)
    login_msg.config(text="register done, now login")


def logout_click():
    # logout and back to login panel
    # go back to start page
    global current_user
    current_user = ""
    app_frame.pack_forget()
    login_frame.pack(padx=8, pady=8)
    login_msg.config(text="logged out")


def add_activity_click():
    # save one activity row
    # button for adding exercise
    if len(current_user) == 0:
        action_msg.config(text="login first")
        return

    t = act_type_entry.get().strip()
    d = act_duration_entry.get().strip()
    n = act_intensity_entry.get().strip().lower()
    s = act_steps_entry.get().strip()

    if bad_text(t):
        action_msg.config(text="activity type needed")
        return

    if not number_text(d) or not number_text(s):
        action_msg.config(text="duration and steps must be numbers")
        return

    dv = float(d)
    sv = float(s)

    if dv <= 0:
        action_msg.config(text="duration must be > 0")
        return

    if sv < 1:
        action_msg.config(text="steps must be >= 1")
        return

    if n != "low" and n != "medium" and n != "high":
        action_msg.config(text="intensity: low/medium/high")
        return

    append_activity_row(current_user, TODAY, t, d, n, s)
    action_msg.config(text="activity saved")

    act_type_entry.delete(0, END)
    act_duration_entry.delete(0, END)
    act_intensity_entry.delete(0, END)
    act_steps_entry.delete(0, END)

    refresh_summary_action()


def add_food_click():
    # save one food row
    # store what i eat today
    if len(current_user) == 0:
        action_msg.config(text="login first")
        return

    n = food_name_entry.get().strip()
    c = food_cal_entry.get().strip()
    carb = food_carb_entry.get().strip()
    prot = food_prot_entry.get().strip()
    fat = food_fat_entry.get().strip()

    if bad_text(n):
        action_msg.config(text="food name needed")
        return

    if not number_text(c) or not number_text(carb) or not number_text(prot) or not number_text(fat):
        action_msg.config(text="food numbers are invalid")
        return

    cv = float(c)
    carbv = float(carb)
    protv = float(prot)
    fatv = float(fat)

    if cv <= 0:
        action_msg.config(text="calories must be > 0")
        return

    if carbv < 0 or protv < 0 or fatv < 0:
        action_msg.config(text="macro values cannot be negative")
        return

    append_food_row(current_user, TODAY, n, c, carb, prot, fat)
    action_msg.config(text="food saved")

    food_name_entry.delete(0, END)
    food_cal_entry.delete(0, END)
    food_carb_entry.delete(0, END)
    food_prot_entry.delete(0, END)
    food_fat_entry.delete(0, END)

    refresh_summary_action()


def save_goal_click():
    # save daily goals
    # update the goals for user
    if len(current_user) == 0:
        action_msg.config(text="login first")
        return

    s = goal_steps_entry.get().strip()
    c = goal_cal_entry.get().strip()

    if not number_text(s) or not number_text(c):
        action_msg.config(text="goal values must be numbers")
        return

    sv = float(s)
    cv = float(c)

    if sv < 1000:
        action_msg.config(text="steps goal too low")
        return

    if cv < 500:
        action_msg.config(text="calorie goal too low")
        return

    goals = read_goal_map()
    goals[current_user] = {"steps": sv, "calories": cv}
    write_goal_map(goals)

    action_msg.config(text="goals saved")
    refresh_summary_action()


# start of script
make_files()

root = Tk()
root.title("Basic Fit Tracker")
root.geometry("760x760")

# login frame
# first screen for login or register
login_frame = Frame(root)
login_frame.pack(padx=8, pady=8)

Label(login_frame, text="basic fit tracker", font=("Arial", 16, "bold")).pack(pady=4)
Label(login_frame, text="username").pack(anchor=W)
# text box for entering username
login_user_entry = Entry(login_frame, width=30)
login_user_entry.pack()

Label(login_frame, text="password").pack(anchor=W)
# security entry hiding typed characters
login_pass_entry = Entry(login_frame, width=30, show="*")
login_pass_entry.pack()

Label(login_frame, text="weight kg (only for register)").pack(anchor=W)
# needed to compute how many calories you burn
login_weight_entry = Entry(login_frame, width=30)
login_weight_entry.pack()

Button(login_frame, text="login", width=16, command=login_click).pack(pady=2)
Button(login_frame, text="register", width=16, command=register_click).pack(pady=2)

login_msg = Label(login_frame, text="")
login_msg.pack()

# app frame
# main screen with all data fields
app_frame = Frame(root)

welcome_label = Label(app_frame, text="logged user:")
welcome_label.grid(row=0, column=0, columnspan=2, sticky=W)

Button(app_frame, text="logout", width=12, command=logout_click).grid(row=0, column=2, sticky=E)

Label(app_frame, text="today date: " + TODAY).grid(row=1, column=0, columnspan=3, sticky=W, pady=2)

# activity area
# part for entering exercise
Label(app_frame, text="activity type").grid(row=2, column=0, sticky=W)
# e.g. walk, run, gym
act_type_entry = Entry(app_frame, width=24)
act_type_entry.grid(row=2, column=1, sticky=W)

Label(app_frame, text="duration min").grid(row=3, column=0, sticky=W)
# total minutes spent exercising
act_duration_entry = Entry(app_frame, width=24)
act_duration_entry.grid(row=3, column=1, sticky=W)

Label(app_frame, text="intensity low/medium/high").grid(row=4, column=0, sticky=W)
# allowed keywords only: low, medium, high
act_intensity_entry = Entry(app_frame, width=24)
act_intensity_entry.grid(row=4, column=1, sticky=W)

Label(app_frame, text="steps").grid(row=5, column=0, sticky=W)
# total steps from pedometer counts
act_steps_entry = Entry(app_frame, width=24)
act_steps_entry.grid(row=5, column=1, sticky=W)

Button(app_frame, text="add activity", width=14, command=add_activity_click).grid(row=6, column=1, sticky=W, pady=2)

# food area
# part for entering food
Label(app_frame, text="food name").grid(row=7, column=0, sticky=W)
# what did you eat today
food_name_entry = Entry(app_frame, width=24)
food_name_entry.grid(row=7, column=1, sticky=W)

Label(app_frame, text="food calories").grid(row=8, column=0, sticky=W)
# energy value of the food in kcal
food_cal_entry = Entry(app_frame, width=24)
food_cal_entry.grid(row=8, column=1, sticky=W)

Label(app_frame, text="carbs g").grid(row=9, column=0, sticky=W)
food_carb_entry = Entry(app_frame, width=24)
food_carb_entry.grid(row=9, column=1, sticky=W)

Label(app_frame, text="protein g").grid(row=10, column=0, sticky=W)
food_prot_entry = Entry(app_frame, width=24)
food_prot_entry.grid(row=10, column=1, sticky=W)

Label(app_frame, text="fat g").grid(row=11, column=0, sticky=W)
food_fat_entry = Entry(app_frame, width=24)
food_fat_entry.grid(row=11, column=1, sticky=W)

Button(app_frame, text="add food", width=14, command=add_food_click).grid(row=12, column=1, sticky=W, pady=2)

# goals area
# part for changing goals
Label(app_frame, text="goal steps").grid(row=13, column=0, sticky=W)
# target steps for daily health goal
goal_steps_entry = Entry(app_frame, width=24)
goal_steps_entry.grid(row=13, column=1, sticky=W)

goal_steps_entry.insert(0, "8000")

Label(app_frame, text="goal calories").grid(row=14, column=0, sticky=W)
goal_cal_entry = Entry(app_frame, width=24)
goal_cal_entry.grid(row=14, column=1, sticky=W)

goal_cal_entry.insert(0, "2000")

Button(app_frame, text="save goals", width=14, command=save_goal_click).grid(row=15, column=1, sticky=W, pady=2)

# utility buttons
Button(app_frame, text="refresh summary", width=14, command=refresh_summary_action).grid(row=16, column=0, sticky=W, pady=2)

action_msg = Label(app_frame, text="")
action_msg.grid(row=16, column=1, sticky=W)

# output boxes
# view everything here
Label(app_frame, text="summary").grid(row=17, column=0, sticky=W, pady=2)
summary_text = Text(app_frame, width=44, height=13)
summary_text.grid(row=18, column=0, columnspan=2, sticky=W)

Label(app_frame, text="today log lines").grid(row=17, column=2, sticky=W, pady=2)
log_text = Text(app_frame, width=42, height=13)
log_text.grid(row=18, column=2, sticky=W)

root.mainloop()