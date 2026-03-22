from datetime import date

# using separate files for each type of data so things stay organised
MEMBERS_FILE   = "members.txt"        # username and password for login
WORKOUT_FILE   = "workout_log.txt"    # every exercise session goes here
FOOD_FILE      = "food_entries.txt"   # meals and calories each day
TARGETS_FILE   = "targets.txt"        # fitness goals the user sets

# calorie burn rates -- these are estimates per minute based on effort
# slightly higher than average to account for afterburn effect
BURN_LIGHT    = 6    # light effort like walking or gentle yoga
BURN_MODERATE = 9    # moderate effort like jogging or cycling
BURN_INTENSE  = 12   # intense effort like sprinting or HIIT

# These handle all the low level reading and writing
# checks if a file already exists on disk
# if not, creates it with the column headers as first line
def initialise_file(filepath, col_headers):
    # try opening for reading - if this works the file exists already
    try:
        handle = open(filepath, "r")
        handle.close()
        # file exists so nothing to do, just return
        return
    except FileNotFoundError:
        # file was not found so we need to create it now
        handle = open(filepath, "w")
        handle.write(col_headers + "\n")   # write headers on first line
        handle.close()
        # file is now ready to use
# call this once at startup to make sure all 4 files exist
def prepare_storage():
    initialise_file(MEMBERS_FILE,  "username,password")
    initialise_file(WORKOUT_FILE,  "username,date,exercise,duration_min,effort")
    initialise_file(FOOD_FILE,     "username,date,meal_name,kcal,carbs_g,protein_g,fat_g")
    initialise_file(TARGETS_FILE,  "username,target_type,goal_value,progress_value")

# loads all rows from a file and gives back a list of dicts
# each dict has keys matching the column headers
def load_records(filepath):
    # open and read everything at once
    file_handle = open(filepath, "r")
    raw_lines = file_handle.readlines()
    file_handle.close()
    # nothing to read if the file only has the header line
    if len(raw_lines) < 2:
        return []
    # get column names from first line
    col_names = raw_lines[0].strip().split(",")
    parsed_rows = []
    # go through every line after the header
    idx = 1
    while idx < len(raw_lines):
        current_line = raw_lines[idx].strip()   # remove whitespace and newline chars
        # skip blank lines that might sneak in
        if current_line != "":
            pieces = current_line.split(",")   # split on comma to get values
            # build a dict pairing column name with value
            record = {}
            col_idx = 0
            while col_idx < len(col_names):
                # if the line has fewer values than headers, fill with blank
                if col_idx < len(pieces):
                    record[col_names[col_idx]] = pieces[col_idx]
                else:
                    record[col_names[col_idx]] = ""
                col_idx = col_idx + 1
            parsed_rows.append(record)
        idx = idx + 1
    return parsed_rows


# adds one row at the bottom of a file
# data_vals is a list of values to write as a comma-separated line
def save_record(filepath, data_vals):
    # build the line manually without any join or f-string
    csv_line = ""
    val_idx = 0
    while val_idx < len(data_vals):
        if val_idx == 0:
            csv_line = str(data_vals[val_idx])
        else:
            csv_line = csv_line + "," + str(data_vals[val_idx])
        val_idx = val_idx + 1

    # open in append mode so existing data is not lost
    file_handle = open(filepath, "a")
    file_handle.write(csv_line + "\n")
    file_handle.close()


# rewrites the whole file -- used when updating existing records
def rewrite_file(filepath, col_headers, all_rows):
    file_handle = open(filepath, "w")
    file_handle.write(col_headers + "\n")   # header always goes first
    col_names = col_headers.split(",")
    # write each record row
    for rec in all_rows:
        line = ""
        col_idx = 0
        while col_idx < len(col_names):
            key = col_names[col_idx]
            if col_idx == 0:
                line = str(rec[key])
            else:
                line = line + "," + str(rec[key])
            col_idx = col_idx + 1
        file_handle.write(line + "\n")
    file_handle.close()




# tries to match the entered username and password against members file
# returns the username string if match found, returns None if not
def member_login():
    print("\nMember Login")
    entered_user = input("Username : ").strip()
    entered_pass = input("Password : ").strip()
    # load all registered members
    all_members = load_records(MEMBERS_FILE)
    # check each member record
    for member in all_members:
        # both username and password must match exactly (case sensitive)
        if member["username"] == entered_user and member["password"] == entered_pass:
            print("Welcome back, " + entered_user + "!")
            return entered_user   # successful login
    # if we finished the loop without returning, login failed
    print("Oops -- username or password was wrong. Try again.")
    return None


# registers a brand new account
# asks for username, checks it isn't taken, then saves it
def register_member():
    print("\n===== Create New Account =====")
    new_user = input("Pick a username : ").strip()

    # first check the username is not already in use
    existing = load_records(MEMBERS_FILE)
    for m in existing:
        if m["username"] == new_user:
            # username is taken -- can't register
            print("Sorry that username is already taken, pick another one.")
            return None
    # username is available -- ask for password now
    new_pass = input("Pick a password : ").strip()
    # save the new member
    save_record(MEMBERS_FILE, [new_user, new_pass])
    print("Account created! You can now log in, " + new_user + ".")
    return new_user

# asks user to enter one or more workout sessions
# saves each one to workout_log.txt
def record_session(logged_in_user):
    print("\n Log Workout Session")
    todays_date = str(date.today())   # e.g. 2026-03-15
    # user can log more than one exercise at a time by using commas
    exercise_input = input("Exercise name(s), use commas to separate (e.g. swimming, weights) : ").strip()
    # split the input into individual exercise names
    exercises_list = exercise_input.split(",")
    saved_count = 0   # track how many were successfully saved
    # process each exercise one at a time
    ex_i = 0
    while ex_i < len(exercises_list):
        ex_name = exercises_list[ex_i].strip()
        # skip if empty string (happens with trailing commas etc.)
        if ex_name == "":
            ex_i = ex_i + 1
            continue
        print("\n  [-] Details for: " + ex_name + " [-]")
        # validate duration -- must be a whole positive number
        # anything that's not a number or <= 0 will get rejected
        duration_ok = False
        duration_val = 0
        while not duration_ok:
            raw_dur = input("  Duration in minutes (1-300) : ")
            try:
                duration_val = int(raw_dur)
                if duration_val >= 1 and duration_val <= 300:
                    duration_ok = True
                else:
                    print("  Duration must be between 1 and 300 minutes.")
            except ValueError:
                # user typed letters or a decimal -- not valid here
                print("  Please type a whole number like 45.")

        # ask for effort level (determines calorie burn estimate later)
        print("  Effort level:  1 = Light   2 = Moderate   3 = Intense")
        effort_ok = False
        effort_label = ""
        while not effort_ok:
            effort_choice = input("  Your effort (1/2/3) : ").strip()
            if effort_choice == "1":
                effort_label = "Light"
                effort_ok = True
            elif effort_choice == "2":
                effort_label = "Moderate"
                effort_ok = True
            elif effort_choice == "3":
                effort_label = "Intense"
                effort_ok = True
            else:
                print("  Please enter 1, 2, or 3 only.")

        # everything looks good -- save to file
        save_record(WORKOUT_FILE, [logged_in_user, todays_date, ex_name, duration_val, effort_label])
        print("  Saved: " + ex_name + " | " + str(duration_val) + " min | " + effort_label)
        saved_count = saved_count + 1
        ex_i = ex_i + 1

    print("\nTotal sessions logged: " + str(saved_count))




# asks user to record a meal entry for today
# includes meal name, calories, and macros
def log_food_entry(logged_in_user):
    print("\n===== Log Food / Meal =====")
    todays_date = str(date.today())

    # get the meal name (breakfast, lunch, dinner, snack etc.)
    meal_label = input("Meal name (e.g. Breakfast, Snack) : ").strip()
    if meal_label == "":
        meal_label = "Meal"   # default name if user pressed enter without typing

    # helper for getting a number >= 0 from the user
    # kept inline here rather than separate function so code flow is clearer
    def ask_for_number(question_text):
        while True:
            raw = input(question_text)
            try:
                num = float(raw)
                if num >= 0:
                    return num
                else:
                    print("  Value cannot be negative.")
            except ValueError:
                print("  Please enter a number.")

    kcal_val    = ask_for_number("  Calories (kcal) : ")
    carbs_val   = ask_for_number("  Carbohydrates (g) : ")
    protein_val = ask_for_number("  Protein (g) : ")
    fat_val     = ask_for_number("  Fat (g) : ")
    # write this meal to food entries file
    save_record(FOOD_FILE, [logged_in_user, todays_date, meal_label, kcal_val, carbs_val, protein_val, fat_val])
    print("Meal logged: " + meal_label + " -- " + str(kcal_val) + " kcal")



# lets the user create or update a personal fitness target
def set_target(logged_in_user):
    print("\n===== Set Fitness Target =====")
    print("  What do you want to track?")
    print("  1.  Daily calorie intake limit")
    print("  2.  Weekly workout sessions")
    print("  3.  Weight loss target (kg to lose)")
    target_choice = input("Choose (1/2/3) : ").strip()
    # convert choice to a label we can store
    if target_choice == "1":
        chosen_type = "daily_calories"
    elif target_choice == "2":
        chosen_type = "weekly_sessions"
    elif target_choice == "3":
        chosen_type = "weight_loss_kg"
    else:
        print("Not a valid option, going back to menu.")
        return

    # ask for the target value
    target_num = 0.0
    valid_target = False
    while not valid_target:
        try:
            raw_target = input("Enter your target value : ")
            target_num = float(raw_target)
            if target_num > 0:
                valid_target = True
            else:
                print("Target must be a positive number.")
        except ValueError:
            print("Please enter a valid number (e.g. 2000 or 5).")

    # check if this target type already exists for this user
    all_targets = load_records(TARGETS_FILE)
    already_exists = False
    for t in all_targets:
        if t["username"] == logged_in_user and t["target_type"] == chosen_type:
            # update the existing record rather than adding a duplicate
            t["goal_value"]     = str(target_num)
            t["progress_value"] = "0"
            already_exists = True
            break

    if already_exists:
        # save the updated list back to file
        rewrite_file(TARGETS_FILE, "username,target_type,goal_value,progress_value", all_targets)
        print("Target updated.")
    else:
        # brand new target -- just append it
        save_record(TARGETS_FILE, [logged_in_user, chosen_type, target_num, 0])
        print("Target saved!")

# converts a raw target_type code into a friendly display label
def target_type_label(ttype):
    if ttype == "daily_calories":
        return "Daily Calorie Limit (kcal)"
    elif ttype == "weekly_sessions":
        return "Weekly Workout Sessions"
    elif ttype == "weight_loss_kg":
        return "Weight Loss Target (kg)"
    else:
        return ttype   # fallback -- just show the code itself


# shows percentage progress for all goals this user has set
def check_progress(logged_in_user):
    print("\n===== My Progress =====")

    # grab this user's targets
    all_targets = load_records(TARGETS_FILE)
    my_targets = []
    for t in all_targets:
        if t["username"] == logged_in_user:
            my_targets.append(t)

    if len(my_targets) == 0:
        print("You haven't set any targets yet. Use option 4 to add one.")
        return
    # load workouts to calculate sessions-based progress
    all_workouts = load_records(WORKOUT_FILE)
    my_workouts = []
    for w in all_workouts:
        if w["username"] == logged_in_user:
            my_workouts.append(w)
    total_sessions = len(my_workouts)   # total all-time workout sessions
    # load food entries to calculate average daily calories
    all_food = load_records(FOOD_FILE)
    my_food = []
    for f in all_food:
        if f["username"] == logged_in_user:
            my_food.append(f)

    # calculate today's total calories from food
    today_str = str(date.today())
    todays_kcal = 0.0
    for f in my_food:
        if f["date"] == today_str:
            todays_kcal = todays_kcal + float(f["kcal"])

    # now show each target with progress
    for t in my_targets:
        goal_val = float(t["goal_value"])
        ttype    = t["target_type"]
        # figure out the current value depending on goal type
        if ttype == "weekly_sessions":
            current_val = float(total_sessions)
        elif ttype == "daily_calories":
            # for calorie limit we show today's intake vs limit
            current_val = todays_kcal
        else:
            # weight loss progress is stored manually
            current_val = float(t["progress_value"])
        # work out percentage -- cap at 100
        if goal_val > 0:
            pct = round((current_val / goal_val) * 100, 1)
            if pct > 100:
                pct = 100.0
        else:
            pct = 0.0
        # print a simple text progress display
        label = target_type_label(ttype)
        print("\n  Goal:    " + label)
        print("  Target:  " + str(goal_val))
        print("  Current: " + str(current_val))
        print("  Progress: " + str(pct) + "%")
        # show a simple star rating (1-5 stars) as visual indicator
        star_count = int(pct / 20)   # every 20% = 1 star
        stars = ""
        s = 0
        while s < star_count:
            stars = stars + "*"
            s = s + 1
        empty = ""
        e = 0
        while e < (5 - star_count):
            empty = empty + "."
            e = e + 1
        print("  Rating:  [" + stars + empty + "]")


# shows the last few workouts the user has done
def view_workout_history(logged_in_user):
    print("\nRecent Workout History")

    all_workouts = load_records(WORKOUT_FILE)
    my_workouts = []
    for w in all_workouts:
        if w["username"] == logged_in_user:
            my_workouts.append(w)
    if len(my_workouts) == 0:
        print("No workouts logged yet!")
        return
    # show last 5 workouts (or fewer if not enough exist)
    show_count = 5
    if len(my_workouts) < show_count:
        show_count = len(my_workouts)

    print("Showing last " + str(show_count) + " sessions:")
    start_pos = len(my_workouts) - show_count

    idx = start_pos
    row_num = 1
    while idx < len(my_workouts):
        w = my_workouts[idx]
        line = str(row_num) + ".  " + w["date"] + "  |  " + w["exercise"] + "  |  " + w["duration_min"] + " min  |  " + w["effort"]
        print(line)
        idx = idx + 1
        row_num = row_num + 1


# generates a daily summary: calories burned, calories eaten, net balance
def todays_summary(logged_in_user):
    print("\nToday's Summary")
    today_str = str(date.today())

    all_workouts = load_records(WORKOUT_FILE)
    todays_workouts = []
    for w in all_workouts:
        if w["username"] == logged_in_user and w["date"] == today_str:
            todays_workouts.append(w)

    total_burned = 0
    total_active = 0
    for w in todays_workouts:
        mins = int(w["duration_min"])
        total_active = total_active + mins

        # pick the burn rate based on effort level
        effort = w["effort"]
        if effort == "Light":
            total_burned = total_burned + (mins * BURN_LIGHT)
        elif effort == "Moderate":
            total_burned = total_burned + (mins * BURN_MODERATE)
        elif effort == "Intense":
            total_burned = total_burned + (mins * BURN_INTENSE)
        else:
            # unknown effort level -- use light as default
            total_burned = total_burned + (mins * BURN_LIGHT)

    #calories consumed
    all_food = load_records(FOOD_FILE)
    todays_food = []
    for f in all_food:
        if f["username"] == logged_in_user and f["date"] == today_str:
            todays_food.append(f)

    total_consumed = 0.0
    for f in todays_food:
        total_consumed = total_consumed + float(f["kcal"])

    net_bal = total_consumed - total_burned   # positive = calorie surplus

    #print summary
    print("  Date            : " + today_str)
    print("  Workouts today  : " + str(len(todays_workouts)))
    print("  Active minutes  : " + str(total_active))
    print("  Calories burned : " + str(total_burned) + " kcal")
    print("  Calories eaten  : " + str(total_consumed) + " kcal")
    print("  Net balance     : " + str(round(net_bal, 1)) + " kcal")

    # give a simple comment on the net balance
    if net_bal > 500:
        print("  Note: You're in a significant calorie surplus today.")
    elif net_bal < -300:
        print("  Note: Great deficit today -- good for weight loss!")
    else:
        print("  Note: Calorie balance looks about right.")


# the main logged-in menu -- runs until user logs out
def app_menu(logged_in_user):
    is_running = True
    while is_running:
        print("\n+-------------------------------+")
        print("|   Fitness Journal              |")
        print("|   User: " + logged_in_user)
        print("+-------------------------------+")
        print("  1.  Log a workout session")
        print("  2.  Log a meal / food entry")
        print("  3.  Set fitness target")
        print("  4.  Check my progress")
        print("  5.  View workout history")
        print("  6.  Today's summary")
        print("  7.  Log out")
        print("+-------------------------------+")

        user_pick = input("Your choice (1-7) : ").strip()

        if user_pick == "1":
            record_session(logged_in_user)
        elif user_pick == "2":
            log_food_entry(logged_in_user)
        elif user_pick == "3":
            set_target(logged_in_user)
        elif user_pick == "4":
            check_progress(logged_in_user)
        elif user_pick == "5":
            view_workout_history(logged_in_user)
        elif user_pick == "6":
            todays_summary(logged_in_user)
        elif user_pick == "7":
            print("\nLogging out. See you next time, " + logged_in_user + "!")
            is_running = False   # this exits the while loop
        else:
            print("That wasn't a valid option. Please pick a number from 1 to 7.")


# the startup screen -- shown before login
def run_app():
    prepare_storage()   # make sure all data files are ready before anything else

    print("*************************************")
    print("*  FITNESS JOURNAL                  *")
    print("*  Your personal workout diary      *")
    print("*************************************")

    active_user = None

    # keep showing the welcome screen until someone gets in
    while active_user is None:
        print("\n  1.  Login to my account")
        print("  2.  Create a new account")
        print("  3.  Quit")

        start_choice = input("Enter option (1-3) : ").strip()

        if start_choice == "1":
            active_user = member_login()       # returns username or None
        elif start_choice == "2":
            active_user = register_member()    # returns username or None
        elif start_choice == "3":
            print("Bye! Come back soon.")
            return   # stop the whole program here
        else:
            print("Please enter 1, 2, or 3.")

    # user is now logged in -- show them the main menu
    app_menu(active_user)


# standard Python entry point
if __name__ == "__main__":
    run_app()
