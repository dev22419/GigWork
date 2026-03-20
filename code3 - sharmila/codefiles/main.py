
"""
This is a console-based health tracking application. Users
create an account, log workouts, record nutrition, set personal
health targets, and review a daily summary. All data persists
between sessions using four plain text files.
FILE LAYOUT:-
  user_store.txt
  session_log.txt
  nutrition_log.txt
  health_targets.txt
"""
######################################################################

from datetime import date
FILE_USERS      = "user_store.txt"
FILE_SESSIONS   = "session_log.txt"
FILE_NUTRITION  = "nutrition_log.txt"
FILE_TARGETS    = "health_targets.txt"

# Calorie burn rates (kcal per minute)
# Derived from approximate MET values at 70 kg bodyweight

BURN_WALK   = 4
BURN_JOG    = 7
BURN_RUN    = 11
BURN_SWIM   = 8
BURN_CYCLE  = 6
BURN_OTHER  = 5

# Progress bar settings
BAR_WIDTH = 25
BAR_FULL  = "#"
BAR_EMPTY = "-"


# SECTION 1: FILE UTILITIES
# All disk access is contained in this section.
# The rest of the program calls these helpers and never opens files
# directly, which makes it easy to change storage format later.

# make_file
# Purpose  : Create a new text file with a header row if it does not
#            already exist on disk. Does nothing when file is present.
# Arguments: filepath  -- name/path of the file to check or create
#            header    -- the first line (column names) to write
# Returns  : Nothing
def make_file(filepath, header):
    # Opening with "x" (exclusive creation) raises FileExistsError
    # if the file is already there, so we can safely ignore that case.
    try:
        fh = open(filepath, "x")
        fh.write(header + "\n")
        fh.close()
    except FileExistsError:
        pass   # file is already present -- nothing to do


#  boot_system
# Purpose  : Initialise all four storage files at startup.
#            Each file gets a comma-separated header row.
# Returns  : Nothing
def boot_system():
    make_file(FILE_USERS,
              "username,password")
    make_file(FILE_SESSIONS,
              "username,date,workout_type,duration_mins,kcal_burned,note")
    make_file(FILE_NUTRITION,
              "username,date,food_item,kcal,carbs_g,protein_g,fat_g")
    make_file(FILE_TARGETS,
              "username,target_type,target_value,current_value")


#  read_rows
# Purpose  : Load every data row from a file as a list of raw strings.
#            The header line (row 0) is excluded from the result.
# Arguments: filepath -- path to the file to read
# Returns  : List of stripped strings, one per data row
def read_rows(filepath):
    fh = open(filepath, "r")
    lines = fh.readlines()
    fh.close()
    collected = []
    # skip index 0 (the header) and skip blank lines
    idx = 1
    while idx < len(lines):
        stripped = lines[idx].strip()
        if stripped != "":
            collected.append(stripped)
        idx = idx + 1

    return collected




#  append_row
# Purpose  : Add one new data row at the end of an existing file.
# Arguments: filepath: path to the file to write to
#            row_str: the comma-separated data line to append
# Returns  : Nothing
def append_row(filepath, row_str):
    fh = open(filepath, "a")
    fh.write(row_str + "\n")
    fh.close()


#  overwrite_rows
# Purpose : Replace the entire contents of a file with a new set of
#            rows. Used when an existing record needs updating.
# Arguments: filepath: path to the file to overwrite
#            header: the column header line to put on line 1
#            rows: list of data row strings to write
# Returns: Nothing
def overwrite_rows(filepath, header, rows):
    fh = open(filepath, "w")
    fh.write(header + "\n")
    for r in rows:
        fh.write(r + "\n")
    fh.close()


# SECTION 2: ACCOUNT MANAGEMENT
#  credentials_match
# Purpose: Check whether a username + password pair exists in the
#            user store. Returns True on a successful match.
# Arguments: uname -- username entered by the user
#            pword -- password entered by the user
# Returns: True if match found, False otherwise
def credentials_match(uname, pword):
    all_rows = read_rows(FILE_USERS)
    for row in all_rows:
        cols = row.split(",")
        # each valid row must have at least 2 columns
        if len(cols) < 2:
            continue
        stored_name = cols[0].strip()
        stored_pass = cols[1].strip()
        # both fields must match exactly
        if stored_name == uname and stored_pass == pword:
            return True
    return False


#  sign_in
# Purpose: Prompt for username and password; validate against stored
#            credentials. Returns the username on success or None.
# Arguments: None
# Returns: Validated username string, or None if sign-in fails
def sign_in():
    print("\n  -- Sign In --")
    typed_name = input("  Username : ").strip()
    typed_pass = input("  Password : ").strip()

    if credentials_match(typed_name, typed_pass):
        print("  Welcome back, " + typed_name + "!")
        return typed_name
    else:
        print("  Incorrect username or password.")
        return None


#  new_account
# Purpose: Walk the user through registering a new account.
#            Rejects blank inputs and usernames already in use.
# Arguments: None
# Returns: New username string on success, or None on failure
def new_account():
    print("\n  -- Create Account --")

    chosen_name = input("  Choose a username : ").strip()
    if chosen_name == "":
        print("  Username cannot be blank.")
        return None

    # Check the username is not already taken
    existing = read_rows(FILE_USERS)
    for row in existing:
        cols = row.split(",")
        if len(cols) >= 1:
            if cols[0].strip() == chosen_name:
                print("  That username is already taken.")
                return None

    chosen_pass = input("  Choose a password : ").strip()
    if chosen_pass == "":
        print("  Password cannot be blank.")
        return None

    # Write the new credentials and confirm
    append_row(FILE_USERS, chosen_name + "," + chosen_pass)
    print("  Account created! Welcome, " + chosen_name + ".")
    return chosen_name


# SECTION 3: INPUT HELPERS

#  validated_number
# Purpose: Repeatedly prompt the user until a valid number is entered.
#            Supports both integer and float validation.
# Arguments: prompt -- the text shown to the user
#            min_value-- smallest acceptable value (inclusive)
#            max_value -- largest acceptable value; -1 means no limit
#            whole_only -- True means only integers are accepted
def validated_number(prompt, min_value, max_value, whole_only):
    while True:
        raw = input(prompt).strip()
        converted = None

        try:
            if whole_only:
                converted = int(raw)
            else:
                converted = float(raw)
        except ValueError:
            if whole_only:
                print("  Please enter a whole number.")
            else:
                print("  Please enter a number.")
            continue
        if converted < min_value:
            print("  Value must be at least " + str(min_value) + ".")
            continue
        if max_value != -1 and converted > max_value:
            print("  Value must be no more than " + str(max_value) + ".")
            continue

        return converted


#  pick_workout_type
# Purpose: Display a numbered workout type menu and return the user's
#            selection as a (type_name, burn_rate) tuple.
# Returns  : Tuple of (workout name string, kcal-per-minute integer)
def pick_workout_type():
    print("\n  Workout type:")
    print("   1. Walking  -- 4 kcal/min")
    print("   2. Jogging  -- 7 kcal/min")
    print("   3. Running  -- 11 kcal/min")
    print("   4. Swimming -- 8 kcal/min")
    print("   5. Cycling  -- 6 kcal/min")
    print("   6. Other    -- 5 kcal/min")

    while True:
        sel = input("  Choose (1-6): ").strip()
        if sel == "1":
            return "Walking",  BURN_WALK
        elif sel == "2":
            return "Jogging",  BURN_JOG
        elif sel == "3":
            return "Running",  BURN_RUN
        elif sel == "4":
            return "Swimming", BURN_SWIM
        elif sel == "5":
            return "Cycling",  BURN_CYCLE
        elif sel == "6":
            return "Other",    BURN_OTHER
        else:
            print("  Enter a number between 1 and 6.")

# SECTION 4:WORKOUT LOGGING
#  log_workout
# Purpose: Record a workout session for the signed-in user.
#            Asks for workout type, duration, and an optional note.
#            Calculates kcal burned automatically from duration x rate.
# Arguments: active_user -- username of the currently signed-in user
# Returns: Nothing
def log_workout(active_user):
    print("\n*** Log Workout ***")
    today = str(date.today())

    # Choose workout type and get corresponding burn rate
    w_type, burn_rate = pick_workout_type()
    # Duration: whole number between 1 and 300 minutes
    mins = int(validated_number("  Duration in minutes (1-300): ", 1, 300, True))
    # Calculate estimated calories burned
    kcal_out = mins * burn_rate

    note = input("  Add a note (Enter to skip): ").strip()
    if note == "":
        note = "none"
    row = (active_user + "," + today + "," + w_type + "," +
           str(mins) + "," + str(kcal_out) + "," + note)
    append_row(FILE_SESSIONS, row)

    print("  Saved! Estimated burn: " + str(kcal_out) + " kcal.")


# SECTION 5: NUTRITION LOGGING
#  log_nutrition
# Purpose: Record a food entry for the signed-in user.
#            Collects the food name, calories, and full macros.
# Arguments: active_user -- username of the currently signed-in user
# Returns: Nothing
def log_nutrition(active_user):
    print("\n*** Log Nutrition ***")
    today     = str(date.today())
    food_name = input("  Food item name: ").strip()
    if food_name == "":
        food_name = "Unnamed item"

    # Collect all nutritional values (must be >= 0, decimals allowed)
    kcal_val    = validated_number("  Calories (kcal) : ",  0, -1, False)
    carbs_val   = validated_number("  Carbs (g)       : ",  0, -1, False)
    protein_val = validated_number("  Protein (g)     : ",  0, -1, False)
    fat_val     = validated_number("  Fat (g)         : ",  0, -1, False)

    # Build and save the row
    row = (active_user + "," + today + "," + food_name + "," +
           str(kcal_val) + "," + str(carbs_val) + "," +
           str(protein_val) + "," + str(fat_val))
    append_row(FILE_NUTRITION, row)
    print("  Nutrition entry saved.")


# SECTION 6: HEALTH TARGETS
#
#  target_label
# Purpose: Convert a target_type code into a human-readable label.
# Arguments: code -- the target type string (e.g. "weekly_kcal_burn")
# Returns: A readable string label
def target_label(code):
    if code == "weekly_kcal_burn":
        return "Weekly Calorie Burn (kcal)"
    elif code == "protein_daily_g":
        return "Daily Protein Intake (g)"
    elif code == "workout_sessions":
        return "Total Workout Sessions"
    else:
        return code


#  set_target
# Purpose: Let the user define or update a personal health target.
#            Three target types are available.
#            Updates an existing row if the same type already exists.
# Arguments: active_user - the signed-in username
# Returns: Nothing
def set_target(active_user):
    print("\n*** Set Health Target ***")
    print("  1. Weekly calorie burn target (kcal)")
    print("  2. Daily protein intake target (g)")
    print("  3. Total workout sessions target")

    # Validate the type selection
    while True:
        t_pick = input("  Choose target type (1-3): ").strip()
        if t_pick == "1":
            t_code = "weekly_kcal_burn"
            break
        elif t_pick == "2":
            t_code = "protein_daily_g"
            break
        elif t_pick == "3":
            t_code = "workout_sessions"
            break
        else:
            print("  Please enter 1, 2, or 3.")

    # Get the target value (must be > 0)
    t_val = validated_number("  Enter your target value: ", 0.01, -1, False)

    # Search for an existing row with the same user + type
    old_rows  = read_rows(FILE_TARGETS)
    new_rows  = []
    found_it  = False

    for row in old_rows:
        parts = row.split(",")
        if len(parts) >= 2:
            # Match on both username AND target type
            if parts[0].strip() == active_user and parts[1].strip() == t_code:
                # Keep the old current_value but update the target
                old_current = "0"
                if len(parts) >= 4:
                    old_current = parts[3].strip()
                updated_row = (active_user + "," + t_code + "," +
                               str(t_val) + "," + old_current)
                new_rows.append(updated_row)
                found_it = True
                continue
        new_rows.append(row)

    if found_it:
        overwrite_rows(FILE_TARGETS,
                       "username,target_type,target_value,current_value",
                       new_rows)
        print("  Target updated successfully.")
    else:
        new_entry = (active_user + "," + t_code + "," +
                     str(t_val) + ",0")
        append_row(FILE_TARGETS, new_entry)
        print("  New target saved.")


#  draw_bar
# Purpose: Build a text-based progress bar string.
# Arguments: pct       -- percentage (0.0 to 100.0)
#            bar_width -- total number of characters in the bar
# Returns: A string like [####-]
def draw_bar(pct, bar_width):
    if pct > 100.0:
        pct = 100.0
    if pct < 0.0:
        pct = 0.0

    filled = int((pct / 100.0) * bar_width)

        # Build filled portion using a counter loop
    bar_str = "["
    count = 0
    while count < filled:
        bar_str = bar_str + BAR_FULL
        count = count + 1

    # Build empty portion
    count = 0
    while count < (bar_width - filled):
        bar_str = bar_str + BAR_EMPTY
        count = count + 1

    bar_str = bar_str + "]"
    return bar_str


#  view_progress
# Purpose: Display all targets for the current user with progress bars.
#            Calculates current values live from session and nutrition files.
# Arguments: active_user - the signed-in username
# Returns: Nothing
def view_progress(active_user):
    print("\n*** Target Progress ***")

    # Load targets for this user
    target_rows = read_rows(FILE_TARGETS)
    my_targets  = []
    for row in target_rows:
        parts = row.split(",")
        if len(parts) >= 3:
            if parts[0].strip() == active_user:
                my_targets.append(parts)

    if len(my_targets) == 0:
        print("  No targets set yet. Use option 3 to set one.")
        return

    #  Calculate current totals from session_log
    session_rows    = read_rows(FILE_SESSIONS)
    total_sessions  = 0
    total_kcal_burn = 0.0

    for row in session_rows:
        parts = row.split(",")
        if len(parts) >= 5:
            if parts[0].strip() == active_user:
                total_sessions = total_sessions + 1
                try:
                    total_kcal_burn = total_kcal_burn + float(parts[4].strip())
                except ValueError:
                    pass

    #  Calculate average daily protein from nutrition_log
    nutrition_rows = read_rows(FILE_NUTRITION)
    protein_by_day = {}

    for row in nutrition_rows:
        parts = row.split(",")
        if len(parts) >= 6:
            if parts[0].strip() == active_user:
                entry_date = parts[1].strip()
                try:
                    p = float(parts[5].strip())
                except ValueError:
                    p = 0.0

                # Add protein to the day's running total
                if entry_date in protein_by_day:
                    protein_by_day[entry_date] = protein_by_day[entry_date] + p
                else:
                    protein_by_day[entry_date] = p

    # Average daily protein across all days that have entries
    avg_protein = 0.0
    if len(protein_by_day) > 0:
        protein_sum = 0.0
        for day in protein_by_day:
            protein_sum = protein_sum + protein_by_day[day]
        avg_protein = protein_sum / len(protein_by_day)

    #  Display each target
    for t in my_targets:
        t_code = t[1].strip()
        try:
            t_goal = float(t[2].strip())
        except ValueError:
            t_goal = 1.0

        # Pick the right current value for each target type
        if t_code == "weekly_kcal_burn":
            current_val = total_kcal_burn
        elif t_code == "protein_daily_g":
            current_val = avg_protein
        elif t_code == "workout_sessions":
            current_val = float(total_sessions)
        else:
            current_val = 0.0

        # Calculate percentage (capped at 100)
        if t_goal > 0:
            pct = (current_val / t_goal) * 100.0
        else:
            pct = 0.0
        if pct > 100.0:
            pct = 100.0

        # Build and show the bar
        label = target_label(t_code)
        bar   = draw_bar(pct, BAR_WIDTH)

        print("\n  " + label)
        print("  " + bar + "  " + str(round(pct, 1)) + "%")
        print("  Current: " + str(round(current_val, 1)) +
              "  /  Target: " + str(t_goal))


# SECTION 7:DAILY SUMMARY
#  todays_summary
# Purpose: Print a complete summary of all activity and food for today.
#            Shows kcal in, kcal out, macros, and net energy balance.
# Arguments: active_user - the signed-in username
# Returns: Nothing
def todays_summary(active_user):
    today = str(date.today())
    print("\n*** Today's Summary  (" + today + ") ***")

    #  Workout totals for today
    session_rows  = read_rows(FILE_SESSIONS)
    w_count       = 0
    total_mins    = 0
    total_kcal_out = 0.0

    for row in session_rows:
        parts = row.split(",")
        if len(parts) >= 5:
            if parts[0].strip() == active_user and parts[1].strip() == today:
                w_count = w_count + 1
                try:
                    total_mins     = total_mins     + int(parts[3].strip())
                    total_kcal_out = total_kcal_out + float(parts[4].strip())
                except ValueError:
                    pass

    #  Nutrition totals for today
    nutrition_rows = read_rows(FILE_NUTRITION)
    f_count        = 0
    total_kcal_in  = 0.0
    total_carbs    = 0.0
    total_protein  = 0.0
    total_fat      = 0.0

    for row in nutrition_rows:
        parts = row.split(",")
        if len(parts) >= 7:
            if parts[0].strip() == active_user and parts[1].strip() == today:
                f_count = f_count + 1
                try:
                    total_kcal_in  = total_kcal_in  + float(parts[3].strip())
                    total_carbs    = total_carbs    + float(parts[4].strip())
                    total_protein  = total_protein  + float(parts[5].strip())
                    total_fat      = total_fat      + float(parts[6].strip())
                except ValueError:
                    pass

    #  Net energy balance
    net_balance = total_kcal_in - total_kcal_out

    #  Display the results
    print("\n  WORKOUTS  (" + str(w_count) + " session(s))")
    print("  Active time    : " + str(total_mins)               + " mins")
    print("  Calories out   : " + str(round(total_kcal_out, 1)) + " kcal")

    print("\n  NUTRITION  (" + str(f_count) + " entry/entries)")
    print("  Calories in    : " + str(round(total_kcal_in,  1)) + " kcal")
    print("  Carbohydrates  : " + str(round(total_carbs,    1)) + " g")
    print("  Protein        : " + str(round(total_protein,  1)) + " g")
    print("  Fat            : " + str(round(total_fat,      1)) + " g")

    print("\n  NET BALANCE : " + str(round(net_balance, 1)) + " kcal")

    if net_balance < 0.0:
        print("  (Calorie deficit -- supports weight loss)")
    elif net_balance > 0.0:
        print("  (Calorie surplus -- supports muscle gain)")
    else:
        print("  (Calories are balanced)")


# SECTION 8 :MAIN MENU AND APPLICATION ENTRY POINT
#  main_screen
# Purpose: Display the main menu for a signed-in user and dispatch
#            to the appropriate function based on their choice.
#            Loops until the user chooses to sign out.
# Arguments: active_user - the signed-in username
# Returns: Nothing
def main_screen(active_user):
    keep_going = True
    while keep_going:
        print("  HealthMate  |  " + active_user)
        print("***************************************")
        print("  1. Log workout")
        print("  2. Log nutrition")
        print("  3. Set health target")
        print("  4. View target progress")
        print("  5. Today's summary")
        print("  6. Sign out")
        print("")

        opt = input("  Enter option (1-6): ").strip()

        if opt == "1":
            log_workout(active_user)
        elif opt == "2":
            log_nutrition(active_user)
        elif opt == "3":
            set_target(active_user)
        elif opt == "4":
            view_progress(active_user)
        elif opt == "5":
            todays_summary(active_user)
        elif opt == "6":
            print("\n  Signed out. Take care, " + active_user + "!")
            keep_going = False
        else:
            print("  Invalid choice. Enter a number from 1 to 6.")


#  run
# Purpose  : Application entry point. Boots the file system, shows the
#            welcome screen, and handles the startup loop.
# Arguments: None
# Returns  : Nothing
def run():
    # Ensure all data files exist before anything else
    boot_system()

    # Display the welcome banner
    print("[**************************************]")
    print("         HealthMate                     ")
    print("  FC308 Programming Assignment 2        ")
    print("[**************************************]")

    # Startup loop -- keep showing until user exits or logs in
    running = True
    while running:
        print("\n  1. Sign in")
        print("  2. Create account")
        print("  3. Exit")
        choice = input("\n  Choose: ").strip()

        if choice == "1":
            user = sign_in()
            if user is not None:
                main_screen(user)

        elif choice == "2":
            user = new_account()
            if user is not None:
                # Go straight to the main menu after registering
                main_screen(user)

        elif choice == "3":
            print("\nThank you for using HealthMate. Goodbye!")
            running = False

        else:
            print("  Please enter 1, 2, or 3.")
run()
