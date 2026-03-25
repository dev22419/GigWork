# -------------------------------------------------------
# FitBuddy - FC308 Programming Assignment 2
# -------------------------------------------------------
# A fitness tracking app that logs training, food, and goals.
# Stores everything in plain .txt files.
# -------------------------------------------------------

import os

# Config file with constants and filenames
from config import (
    MEMBERS,
    TRAINING,
    FOOD,
    GOALS,
    CARDIO_EASY,
    CARDIO_MED,
    CARDIO_HARD,
    STRENGTH,
    HIIT,
)


def create_if_missing(fname, header):
    if not os.path.exists(fname):
        with open(fname, "w") as file_obj:
            file_obj.write(header + "\n")


def get_all_rows(fname):
    with open(fname, "r") as source_stream:
        ledger_entries = []
        is_header_row = True

        for raw_record in source_stream:
            if is_header_row:
                is_header_row = False
                continue

            trimmed_record = raw_record.strip()
            if trimmed_record:
                ledger_entries.append(trimmed_record)

    return ledger_entries


def save_row(fname, row_data):
    with open(fname, "a") as file_obj:
        file_obj.write(row_data + "\n")


def replace_file(fname, header, new_rows):
    with open(fname, "w") as file_obj:
        file_obj.write(header + "\n")
        for row in new_rows:
            file_obj.write(row + "\n")

def do_login():
    # asks for username + password, checks against member_list
    # returns the username if correct, None if wrong
    print("\n[ Sign In ]")
    uname = input("Username:")
    pword = input("Password:")
    rows = get_all_rows(MEMBERS)
    for row in rows:
        cols = row.split(",")
        if len(cols) >= 2:
            if cols[0] == uname and cols[1] == pword:
                print("Logged in as " + uname)
                return uname
    print("Wrong username or password.")
    return None


def do_register():
    # lets a new user pick a username and password
    # returns username on success, None if taken or blank 
    # also checks password strength (at least 6 chars, has a number)
    print("\n[ Register ]")
    uname = input("Pick a username: ")
    if uname == "":
        print("Username can't be blank.")
        return None
    # make sure this name isn't already used
    rows = get_all_rows(MEMBERS)
    for row in rows:
        cols = row.split(",")
        if len(cols) >= 1:
            if cols[0] == uname:
                print("That username is taken.")
                return None
    pword = input("Pick a password: ")
    if pword == "":
        print("Password can't be blank.")
        return None
    # check password strength (at least 6 chars, has a number)
    if len(pword) < 6:
        print("Password must be at least 6 characters.")
        return None
    save_row(MEMBERS, uname + "," + pword)
    print(uname + " registered successfully.")    
    return uname

def ask_number(msg, must_be_int, min_val, max_val):
    # loops until the user enters a valid number
    # must_be_int=True means whole numbers only
    # max_val=-1 means no upper limit
    while True:
        raw = input(msg)
        ok  = True
        num = 0
        try:
            if must_be_int:
                num = int(raw)
            else:
                num = float(raw)
        except ValueError:
            ok = False

        if not ok:
            print("Please enter a valid number.")
            continue

        if num < min_val:
            print("Minimum is " + str(min_val))
            continue

        if max_val != -1 and num > max_val:
            print("Maximum is " + str(max_val))
            continue

        return num

def add_training(current_user):
    # records a workout session
    # shows 5 activity types with kcal/min rates
    # also checks for a personal best (longest session ever)
    print("\n[ Log Training Session ]")

    # show activity menu
    print("Activity type:")
    print("1. Light cardio(4 kcal/min)\n2. Moderate cardio(7 kcal/min)\n3. Hard cardio(10 kcal/min)\n4. Strength(5 kcal/min)\n5. HIIT(13 kcal/min)")

    # pick activity until valid
    burn  = 0
    aname = ""
    while True:
        pick = input("Choose (1-5): ")
        if pick == "1":
            aname = "Light cardio"
            burn  = CARDIO_EASY
            break
        elif pick == "2":
            aname = "Moderate cardio"
            burn  = CARDIO_MED
            break
        elif pick == "3":
            aname = "Hard cardio"
            burn  = CARDIO_HARD
            break
        elif pick == "4":
            aname = "Strength"
            burn  = STRENGTH
            break
        elif pick == "5":
            aname = "HIIT"
            burn  = HIIT
            break
        else:
            print("Enter 1 to 5 only.")

    # get duration
    mins = int(ask_number("Duration (mins, 1-240): ", True, 1, 240))

    # intensity label
    if burn <= 5:
        intensity = "Low"
    elif burn <= 8:
        intensity = "Medium"
    else:
        intensity = "High"

    # calc kcal
    kcal = mins * burn

    # check personal best (longest session for this user)
    pb = 0
    old_rows = get_all_rows(TRAINING)
    for row in old_rows:
        cols = row.split(",")
        if len(cols) >= 4:
            if cols[0] == current_user:
                try:
                    if len(cols) >= 6:
                        d = int(cols[3])
                    else:
                        d = int(cols[2])
                    if d > pb:
                        pb = d
                except ValueError:
                    pass

    # save the session
    save_row(TRAINING,
             current_user + "," + aname + "," +
             str(mins) + "," + intensity + "," + str(kcal))

    print("Session saved. Burned approx " + str(kcal) + " kcal.")

    # personal best message
    if mins > pb:
        print("NEW PERSONAL BEST! Longest session yet: " + str(mins) + " mins.")
    else:
        print("Personal best: " + str(pb) + " mins. Keep pushing!")


def add_food(current_user):
    # records a food/meal entry with kcal and macros
    print("\n[ Log Food Entry ]")

    desc = input("Food description: ")
    if desc == "":
        desc = "Unspecified"

    kcal    = ask_number("Calories (kcal): ",  False, 0, -1)
    carbs   = ask_number("Carbs (g)      : ",  False, 0, -1)
    protein = ask_number("Protein (g)    : ",  False, 0, -1)
    fat     = ask_number("Fat (g)        : ",  False, 0, -1)

    save_row(FOOD,
             current_user + "," + desc + "," +
             str(kcal) + "," + str(carbs) + "," + str(protein) + "," + str(fat))

    print("Food entry saved.")

def goal_name(code):
    # converts a goal code to a readable name
    if code == "sessions_target":
        return "Total Training Sessions"
    elif code == "kcal_burn_target":
        return "Total Calories Burned (kcal)"
    elif code == "protein_goal_g":
        return "Avg Daily Protein (g)"
    else:
        return code


def set_goal(current_user):
    # lets the user pick and set one of 3 goal types
    print("\n[ Set Fitness Goal ]")
    print("1. Total training sessions target")
    print("2. Total calories burned target (kcal)")
    print("3. Average daily protein target (g)")
    while True:
        g = input("Choose goal (1-3): ")
        if g == "1":
            gcode = "sessions_target"
            break
        elif g == "2":
            gcode = "kcal_burn_target"
            break
        elif g == "3":
            gcode = "protein_goal_g"
            break
        else:
            print("Enter 1, 2, or 3.")

    gval = ask_number("Target value: ", False, 0.01, -1)

    # check if goal already exists for this user + type
    old_rows= get_all_rows(GOALS)
    new_rows= []
    updated = False

    for row in old_rows:
        cols = row.split(",")
        if len(cols) >= 2:
            if cols[0] == current_user and cols[1] == gcode:
                # replace the old goal with updated target
                cur_val = "0"
                if len(cols) >= 4:
                    cur_val = cols[3]
                new_rows.append(current_user + "," + gcode + "," +
                                str(gval) + "," + cur_val)
                updated = True
                continue
        new_rows.append(row)

    if updated:
        replace_file(GOALS, "user,goal_type,goal_target,logged_value", new_rows)
        print("Goal updated.")
    else:
        save_row(GOALS, current_user + "," + gcode + "," + str(gval) + ",0")
        print("Goal saved.")


def build_progress_bar(pct):
    # builds a text bar like [====      ] out of 20 chars
    if pct > 100.0:
        pct = 100.0
    if pct < 0.0:
        pct = 0.0

    total   = 20
    filled  = int((pct / 100.0) * total)
    bar_str = "["
    i = 0
    while i < total:
        if i < filled:
            bar_str = bar_str + "="
        else:
            bar_str = bar_str + " "
        i = i + 1
    bar_str = bar_str + "]"
    return bar_str


def show_progress(current_user):
    # shows goal progress with a text bar for each goal
    print("\n[ Goal Progress ]")

    goal_rows  = get_all_rows(GOALS)
    user_goals = []
    for row in goal_rows:
        cols = row.split(",")
        if len(cols) >= 3:
            if cols[0] == current_user:
                user_goals.append(cols)

    if len(user_goals) == 0:
        print("No goals set. Use option 3 first.")
        return

    # compute totals from training and food files
    train_rows     = get_all_rows(TRAINING)
    total_sessions = 0
    total_kcal_out = 0.0

    for row in train_rows:
        cols = row.split(",")
        if len(cols) >= 5:
            if cols[0] == current_user:
                total_sessions = total_sessions + 1
                try:
                    if len(cols) >= 6:
                        total_kcal_out = total_kcal_out + float(cols[5])
                    else:
                        total_kcal_out = total_kcal_out + float(cols[4])
                except ValueError:
                    pass

    # avg daily protein
    food_rows      = get_all_rows(FOOD)
    protein_totals = {}
    for row in food_rows:
        cols = row.split(",")
        if len(cols) >= 6:
            if cols[0] == current_user:
                if len(cols) >= 7:
                    d = cols[1]
                    protein_index = 5
                else:
                    d = "all_entries"
                    protein_index = 4
                try:
                    p = float(cols[protein_index])
                except ValueError:
                    p = 0.0
                if d in protein_totals:
                    protein_totals[d] = protein_totals[d] + p
                else:
                    protein_totals[d] = p

    avg_protein = 0.0
    if len(protein_totals) > 0:
        s = 0.0
        for k in protein_totals:
            s = s + protein_totals[k]
        avg_protein = s / len(protein_totals)

    # show each goal
    for g in user_goals:
        gcode = g[1]
        try:
            gtarget = float(g[2])
        except ValueError:
            gtarget = 1.0

        if gcode == "sessions_target":
            current = float(total_sessions)
        elif gcode == "kcal_burn_target":
            current = total_kcal_out
        elif gcode == "protein_goal_g":
            current = avg_protein
        else:
            current = 0.0

        if gtarget > 0:
            pct = (current / gtarget) * 100.0
        else:
            pct = 0.0
        if pct > 100.0:
            pct = 100.0

        bar = build_progress_bar(pct)
        print("\n  " + goal_name(gcode))
        print("" + bar + "" + str(round(pct, 1)) + "%")
        print("" + str(round(current, 1)) + " / " + str(gtarget))

def daily_snapshot(current_user):
    # shows all logged workouts + food + net balance
    print("\n[ Daily Snapshot ]")

    # training totals
    train_rows  = get_all_rows(TRAINING)
    t_count     = 0
    t_mins      = 0
    t_kcal      = 0.0

    for row in train_rows:
        cols = row.split(",")
        if len(cols) >= 5:
            if cols[0] == current_user:
                t_count = t_count + 1
                try:
                    if len(cols) >= 6:
                        t_mins = t_mins + int(cols[3])
                        t_kcal = t_kcal + float(cols[5])
                    else:
                        t_mins = t_mins + int(cols[2])
                        t_kcal = t_kcal + float(cols[4])
                except ValueError:
                    pass

    # food totals
    food_rows = get_all_rows(FOOD)
    f_count   = 0
    f_kcal    = 0.0
    f_carbs   = 0.0
    f_protein = 0.0
    f_fat     = 0.0

    for row in food_rows:
        cols = row.split(",")
        if len(cols) >= 6:
            if cols[0] == current_user:
                f_count = f_count + 1
                try:
                    if len(cols) >= 7:
                        f_kcal    = f_kcal    + float(cols[3])
                        f_carbs   = f_carbs   + float(cols[4])
                        f_protein = f_protein + float(cols[5])
                        f_fat     = f_fat     + float(cols[6])
                    else:
                        f_kcal    = f_kcal    + float(cols[2])
                        f_carbs   = f_carbs   + float(cols[3])
                        f_protein = f_protein + float(cols[4])
                        f_fat     = f_fat     + float(cols[5])
                except ValueError:
                    pass

    net = f_kcal - t_kcal

    print("\n  Training: " + str(t_count) + " session(s)")
    print("Time:" + str(t_mins) + " mins")
    print("Burned:" + str(round(t_kcal, 1)) + " kcal")

    print("\n  Food: " + str(f_count) + " entry/entries")
    print("Eaten:" + str(round(f_kcal, 1)) + " kcal")
    print("Carbs:" + str(round(f_carbs, 1)) + " g")
    print("Protein:" + str(round(f_protein, 1)) + " g")
    print("Fat:" + str(round(f_fat, 1)) + " g")

    print("\n  Net balance: " + str(round(net, 1)) + " kcal")

    if net < 0:
        print("Deficit! Good for fat loss.")
    elif net > 0:
        print("Surplus. Good for muscle building.")
    else:
        print("Balanced day.")

def run_menu(current_user):
    # main menu loop : runs until user logs out
    going = True
    while going:
        print("\n-------------------------------")
        print("FitBuddy | " + current_user)
        print("------------------------------")
        print("T. Log training session\nF. Log food\nG. Set fitness goal\nP. View goal progress\nS. Daily snapshot\nL. Log out")

        opt = input("Option: ")

        if opt == "T":
            add_training(current_user)
        elif opt == "F":
            add_food(current_user)
        elif opt == "G":
            set_goal(current_user)
        elif opt == "P":
            show_progress(current_user)
        elif opt == "S":
            daily_snapshot(current_user)
        elif opt == "L":
            print("Logged out. Bye " + current_user + "!")
            going = False
        else:
            print("Invalid. View options and enter the letter for your choice.")


if __name__ == "__main__":
    # entry point : sets up files, shows login screen
    create_if_missing(MEMBERS,"username,password")
    create_if_missing(TRAINING,"user,activity,duration,intensity,kcal_burned")
    create_if_missing(FOOD,"user,description,kcal,carbs,protein,fat")
    create_if_missing(GOALS,"user,goal_type,goal_target,logged_value")

    print("FitBuddy")
    print("FC308 Assignment 2")

    active = True
    while active:
        print("\nSI. Sign in\nSU. Sign up\nQ. Quit the Program")
        choice = input("Choice: ")

        if choice == "SI":
            logged_in_as = do_login()
            if logged_in_as is not None:
                run_menu(logged_in_as)

        elif choice == "SU":
            new_user = do_register()
            if new_user is not None:
                run_menu(new_user)

        elif choice == "Q":
            print("Exiting the program!")
            active = False

        else:
            print("Enter Correct choice")
