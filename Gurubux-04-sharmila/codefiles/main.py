# -------------------------------------------------------
# FitBuddy - FC308 Programming Assignment 2
# Student:
# -------------------------------------------------------
# A fitness tracking app that logs training, food, and goals.
# Stores everything in plain .txt files -- no imports except date.
# -------------------------------------------------------

from datetime import date

# using short names so they're easy to type
MEMBERS="member_list.txt"      # username + password
TRAINING="training_sessions.txt"  # workout records
FOOD="food_diary.txt"        # food and kcal
GOALS="fitness_goals.txt"     # user goals

# different activities burn at very different rates
# using WHO and NHS activity guidelines as reference
CARDIO_EASY= 4   # light cardio e.g. walking
CARDIO_MED= 7   # medium e.g. cycling
CARDIO_HARD= 10  # hard e.g. running
STRENGTH= 5   # weight training, average
HIIT= 13  # high intensity interval training

def prep_all_files():
    # make sure every file exists before we try to read it
    create_if_missing(MEMBERS,"username,password")
    create_if_missing(TRAINING,"user,date,activity,duration,intensity,kcal_burned")
    create_if_missing(FOOD,"user,date,description,kcal,carbs,protein,fat")
    create_if_missing(GOALS,"user,goal_type,goal_target,logged_value")


def create_if_missing(fname, header):
    # try to open for reading -- only fails if file doesn't exist
    try:
        f = open(fname, "r")
        f.close()
        # file exists, nothing needed
    except FileNotFoundError:
        # create the file with a header row
        f = open(fname, "w")
        f.write(header + "\n")
        f.close()

def get_all_rows(fname):
    # returns list of raw strings, skips the header row
    f = open(fname, "r")
    lines = f.readlines()
    f.close()

    rows = []
    i    = 0
    for line in lines:
        if i == 0:
            # skip header
            i = i + 1
            continue
        clean = line.strip()
        if clean != "":
            rows.append(clean)
        i = i + 1
    return rows


def save_row(fname, row_data):
    # appends one row to the end of a file
    f = open(fname, "a")
    f.write(row_data + "\n")
    f.close()


def replace_file(fname, header, new_rows):
    # completely rewrites a file -- used for goal updates
    f = open(fname, "w")
    f.write(header + "\n")
    for r in new_rows:
        f.write(r + "\n")
    f.close()

def do_login():
    # asks for username + password, checks against member_list
    # returns the username if correct, None if wrong
    print("\n[ Sign In ]")
    uname = input("Username: ").strip()
    pword = input("Password: ").strip()
    rows = get_all_rows(MEMBERS)
    for row in rows:
        cols = row.split(",")
        if len(cols) >= 2:
            if cols[0].strip() == uname and cols[1].strip() == pword:
                print("  Logged in as " + uname)
                return uname
    print("Wrong username or password.")
    return None


def do_register():
    # lets a new user pick a username and password
    # returns username on success, None if taken or blank
    print("\n[ Register ]")
    uname = input("Pick a username: ").strip()
    if uname == "":
        print("Username can't be blank.")
        return None
    # make sure this name isn't already used
    rows = get_all_rows(MEMBERS)
    for row in rows:
        cols = row.split(",")
        if len(cols) >= 1:
            if cols[0].strip() == uname:
                print("  That username is taken.")
                return None
    pword = input("  Pick a password: ").strip()
    if pword == "":
        print("  Password can't be blank.")
        return None
    save_row(MEMBERS, uname + "," + pword)
    print("  Registered! Welcome " + uname)
    return uname

def ask_number(msg, must_be_int, min_val, max_val):
    # loops until the user enters a valid number
    # must_be_int=True means whole numbers only
    # max_val=-1 means no upper limit
    while True:
        raw = input(msg).strip()
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
            print("  Please enter a valid number.")
            continue

        if num < min_val:
            print("  Minimum is " + str(min_val))
            continue

        if max_val != -1 and num > max_val:
            print("  Maximum is " + str(max_val))
            continue

        return num

def add_training(current_user):
    # records a workout session
    # shows 5 activity types with kcal/min rates
    # also checks for a personal best (longest session ever)
    print("\n[ Log Training Session ]")
    today = str(date.today())

    # show activity menu
    print("Activity type:")
    print("1. Light cardio(4 kcal/min)")
    print("2. Moderate cardio(7 kcal/min)")
    print("3. Hard cardio(10 kcal/min)")
    print("4. Strength(5 kcal/min)")
    print("5. HIIT(13 kcal/min)")

    # pick activity until valid
    burn  = 0
    aname = ""
    while True:
        pick = input("  Choose (1-5): ").strip()
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
            print("  Enter 1 to 5 only.")

    # get duration
    mins = int(ask_number("  Duration (mins, 1-240): ", True, 1, 240))

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
            if cols[0].strip() == current_user:
                try:
                    d = int(cols[3].strip())
                    if d > pb:
                        pb = d
                except ValueError:
                    pass

    # save the session
    save_row(TRAINING,
             current_user + "," + today + "," + aname + "," +
             str(mins) + "," + intensity + "," + str(kcal))

    print("  Session saved. Burned approx " + str(kcal) + " kcal.")

    # personal best message
    if mins > pb:
        print("  NEW PERSONAL BEST! Longest session yet: " + str(mins) + " mins.")
    else:
        print("  Personal best: " + str(pb) + " mins. Keep pushing!")


def add_food(current_user):
    # records a food/meal entry with kcal and macros
    print("\n[ Log Food Entry ]")
    today = str(date.today())

    desc = input("  Food description: ").strip()
    if desc == "":
        desc = "Unspecified"

    kcal    = ask_number("  Calories (kcal): ",  False, 0, -1)
    carbs   = ask_number("  Carbs (g)      : ",  False, 0, -1)
    protein = ask_number("  Protein (g)    : ",  False, 0, -1)
    fat     = ask_number("  Fat (g)        : ",  False, 0, -1)

    save_row(FOOD,
             current_user + "," + today + "," + desc + "," +
             str(kcal) + "," + str(carbs) + "," + str(protein) + "," + str(fat))

    print("  Food entry saved.")

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
        g = input("  Choose goal (1-3): ").strip()
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
            print("  Enter 1, 2, or 3.")

    gval = ask_number("  Target value: ", False, 0.01, -1)

    # check if goal already exists for this user + type
    old_rows= get_all_rows(GOALS)
    new_rows= []
    updated = False

    for row in old_rows:
        cols = row.split(",")
        if len(cols) >= 2:
            if cols[0].strip() == current_user and cols[1].strip() == gcode:
                # replace the old goal with updated target
                cur_val = "0"
                if len(cols) >= 4:
                    cur_val = cols[3].strip()
                new_rows.append(current_user + "," + gcode + "," +
                                str(gval) + "," + cur_val)
                updated = True
                continue
        new_rows.append(row)

    if updated:
        replace_file(GOALS, "user,goal_type,goal_target,logged_value", new_rows)
        print("  Goal updated.")
    else:
        save_row(GOALS, current_user + "," + gcode + "," + str(gval) + ",0")
        print("  Goal saved.")


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
            if cols[0].strip() == current_user:
                user_goals.append(cols)

    if len(user_goals) == 0:
        print("  No goals set. Use option 3 first.")
        return

    # compute totals from training and food files
    train_rows     = get_all_rows(TRAINING)
    total_sessions = 0
    total_kcal_out = 0.0

    for row in train_rows:
        cols = row.split(",")
        if len(cols) >= 6:
            if cols[0].strip() == current_user:
                total_sessions = total_sessions + 1
                try:
                    total_kcal_out = total_kcal_out + float(cols[5].strip())
                except ValueError:
                    pass

    # avg daily protein
    food_rows      = get_all_rows(FOOD)
    protein_totals = {}
    for row in food_rows:
        cols = row.split(",")
        if len(cols) >= 6:
            if cols[0].strip() == current_user:
                d = cols[1].strip()
                try:
                    p = float(cols[5].strip())
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
        gcode = g[1].strip()
        try:
            gtarget = float(g[2].strip())
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
        print("  " + bar + "  " + str(round(pct, 1)) + "%")
        print("  " + str(round(current, 1)) + " / " + str(gtarget))

def daily_snapshot(current_user):
    # shows everything logged today -- workouts + food + net balance
    today = str(date.today())
    print("\n[ Daily Snapshot -- " + today + " ]")

    # today's training
    train_rows  = get_all_rows(TRAINING)
    t_count     = 0
    t_mins      = 0
    t_kcal      = 0.0

    for row in train_rows:
        cols = row.split(",")
        if len(cols) >= 6:
            if cols[0].strip() == current_user and cols[1].strip() == today:
                t_count = t_count + 1
                try:
                    t_mins = t_mins + int(cols[3].strip())
                    t_kcal = t_kcal + float(cols[5].strip())
                except ValueError:
                    pass

    # today's food
    food_rows = get_all_rows(FOOD)
    f_count   = 0
    f_kcal    = 0.0
    f_carbs   = 0.0
    f_protein = 0.0
    f_fat     = 0.0

    for row in food_rows:
        cols = row.split(",")
        if len(cols) >= 7:
            if cols[0].strip() == current_user and cols[1].strip() == today:
                f_count = f_count + 1
                try:
                    f_kcal    = f_kcal    + float(cols[3].strip())
                    f_carbs   = f_carbs   + float(cols[4].strip())
                    f_protein = f_protein + float(cols[5].strip())
                    f_fat     = f_fat     + float(cols[6].strip())
                except ValueError:
                    pass

    net = f_kcal - t_kcal

    print("\nTraining:" + str(t_count) + "session(s)")
    print("Time:" + str(t_mins) + " mins")
    print("Burned:" + str(round(t_kcal, 1)) + " kcal")

    print("\nFood:" + str(f_count) + " entry/entries")
    print("Eaten:" + str(round(f_kcal,1)) + " kcal")
    print("Carbs:" + str(round(f_carbs,1)) + " g")
    print("Protein:" + str(round(f_protein, 1)) + " g")
    print("Fat:" + str(round(f_fat,1)) + " g")
    print("\n  Net balance: " + str(round(net, 1)) + " kcal")
    if net < 0:
        print("  Deficit! Good for fat loss.")
    elif net > 0:
        print("  Surplus. Good for muscle building.")
    else:
        print("  Balanced day.")

def run_menu(current_user):
    # main menu loop -- runs until user logs out
    going = True
    while going:
        print("\n-------------------------------")
        print("  FitBuddy | " + current_user)
        print("------------------------------")
        print("1. Log training session")
        print("2. Log food")
        print("3. Set fitness goal")
        print("4. View goal progress")
        print("5. Daily snapshot")
        print("6. Log out")

        opt = input("  Option: ").strip()

        if opt == "1":
            add_training(current_user)
        elif opt == "2":
            add_food(current_user)
        elif opt == "3":
            set_goal(current_user)
        elif opt == "4":
            show_progress(current_user)
        elif opt == "5":
            daily_snapshot(current_user)
        elif opt == "6":
            print("  Logged out. Bye " + current_user + "!")
            going = False
        else:
            print("  Invalid. Enter 1-6.")

def launch():
    # entry point -- sets up files, shows login screen
    prep_all_files()
    print("FitBuddy")
    active = True
    while active:
        print("\n 1. Log in")
        print("2. Register")
        print("3. Quit")
        choice = input("  Choice: ").strip()
        if choice == "1":
            logged_in_as = do_login()
            if logged_in_as is not None:
                run_menu(logged_in_as)

        elif choice == "2":
            new_user = do_register()
            if new_user is not None:
                run_menu(new_user)

        elif choice == "3":
            print("  Goodbye!")
            active = False

        else:
            print("  Enter 1, 2, or 3.")

launch()
