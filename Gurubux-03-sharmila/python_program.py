"""
This is a console-based health tracking application. Users
create an account, log workouts, record nutrition, set personal
health targets, and review a daily summary. All data persists
between sessions using four plain text files.
"""

# Constants for file paths and workout burn rates
FILES = {
    "users": "user_store.txt",
    "sessions": "session_log.txt",
    "nutrition": "nutrition_log.txt",
    "targets": "health_targets.txt"
}

# Calorie burn rates (kcal per minute)
# Derived from approximate MET values at 70 kg bodyweight
BURN_RATES = {
    "Walking": 4,
    "Jogging": 7,
    "Running": 11,
    "Swimming": 8,
    "Cycling": 6,
    "Other": 5
}


# SECTION 1: FILE UTILITIES
# All disk access is contained in this section.
# The rest of the program calls these helpers and never opens files
# directly, which makes it easy to change storage format later.


def make_file(filepath, header):
    """
    Purpose: Create a new file with the given header, but only if it doesn't already exist.
    Arguments: filepath -- name/path of the file to create
               header   -- the header line to write at the top of the file
    Returns: Nothing    
    """
    try:
        fh = open(filepath, "x")
        fh.write(header + "\n")
        fh.close()
    except FileExistsError:
        pass  # file is already present -- nothing to do


def boot_system():
    """
    Purpose: Ensure all data files exist before the app starts.
    Arguments: None
    Returns: Nothing
    """
    make_file(FILES["users"],
              "username,password")
    make_file(FILES["sessions"],
              "username,workout_type,duration_mins,kcal_burned,note")
    make_file(FILES["nutrition"],
              "username,food_item,kcal,carbs_g,protein_g,fat_g")
    make_file(FILES["targets"],
              "username,target_type,target_value,current_value")


def read_rows(filepath):
    """
    Purpose: Read all data rows from a file, skipping the header and blank lines.
    Arguments: filepath -- name/path of the file to read
    Returns: List of strings, one per data row (no header, no blanks)
    """
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


def append_row(filepath, row_str):
    """
    Purpose: Add a single new data row to the end of a file.
    Arguments: filepath -- name/path of the file to update
               row_str  -- the new row to add (should be comma-separated)
               Returns: Nothing
    """
    fh = open(filepath, "a")
    fh.write(row_str + "\n")
    fh.close()


def overwrite_rows(filepath, header, rows):
    """
    Purpose: Replace all data rows in a file with a new set. Writes the header first.
    Arguments: filepath -- name/path of the file to update
               header   -- the header line to write at the top of the file
               rows     -- list of strings, each a comma-separated data row
    Returns: Nothing
    """
    fh = open(filepath, "w")
    fh.write(header + "\n")
    for r in rows:
        fh.write(r + "\n")
    fh.close()


def credentials_match(uname, pword):
    """
    Check whether a username + password pair exists in the user store.
    Arguments:
        uname -- username entered by the user
        pword -- password entered by the user
    Returns:
        True if match found, False otherwise
    """
    all_rows = read_rows(FILES["users"])
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


def sign_in():
    """
    Purpose: Prompt the user to enter their username and password, and check
             against the user store. Returns the username on success, or None on failure.
    Arguments: None 
    Returns: The username string if credentials are correct, or None if not.
    """
    print("\n  -- Sign In --")
    typed_name = input("  Username : ").strip()
    typed_pass = input("  Password : ").strip()

    if credentials_match(typed_name, typed_pass):
        print("  Welcome back, " + typed_name + "!")
        return typed_name
    else:
        print("  Incorrect username or password.")
        return None


def new_account():
    """
    Purpose: Guide the user through creating a new account. Checks for blank
             fields and duplicate usernames. Returns the new username on success, or None on failure.
             Arguments: None
             Returns: The new username string if account creation is successful, or None if not.
    """
    print("\n  -- Create Account --")

    chosen_name = input("  Choose a username : ").strip()
    if chosen_name == "":
        print("  Username cannot be blank.")
        return None

    # Check the username is not already taken
    existing = read_rows(FILES["users"])
    for row in existing:
        cols = row.split(",")
        if len(cols) >= 1:
            if cols[0].strip() == chosen_name:
                print("  That username is already taken.")
                return None

    chosen_pass = input("Password please: ").strip()
    if chosen_pass == "":
        print("  Password cannot be blank.")
        return None

    # Write the new credentials and confirm
    append_row(FILES["users"], chosen_name + "," + chosen_pass)
    print("  Account created for " + chosen_name)
    return chosen_name


# SECTION 3: INPUT HELPERS

def validated_number(prompt, min_value, max_value, whole_only):
    """
    Purpose: Prompt the user to enter a number, and validate that it is a valid
             number within the specified range. Repeats until valid input is received.
    Arguments:
    prompt     -- the text to show when asking for input
    min_value  -- the minimum acceptable value (inclusive)
    max_value  -- the maximum acceptable value (inclusive), or -1 for no max
    whole_only -- if True, only accept whole numbers (integers)
    Returns: The validated number, as an int if whole_only is True, or a float otherwise.
    """
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


def pick_workout_type():
    """
    Purpose: Prompt the user to select a workout type from the predefined list,
             and return both the workout name and its corresponding burn rate.
             Arguments: None
             Returns: A tuple (workout_name, burn_rate) where workout_name is the string name of the workout, and burn_rate is the kcal/min value.
    """
    print("\n  Workout type:")
    workout_options = {
        "1": "Walking",
        "2": "Jogging",
        "3": "Running",
        "4": "Swimming",
        "5": "Cycling",
        "6": "Other"
    }

    print("   1. Walking  -- " + str(BURN_RATES["Walking"]) + " kcal/min")
    print("   2. Jogging  -- " + str(BURN_RATES["Jogging"]) + " kcal/min")
    print("   3. Running  -- " + str(BURN_RATES["Running"]) + " kcal/min")
    print("   4. Swimming -- " + str(BURN_RATES["Swimming"]) + " kcal/min")
    print("   5. Cycling  -- " + str(BURN_RATES["Cycling"]) + " kcal/min")
    print("   6. Other    -- " + str(BURN_RATES["Other"]) + " kcal/min")

    while True:
        sel = input("  Choose (1-6): ").strip()
        if sel in workout_options:
            workout_name = workout_options[sel]
            return workout_name, BURN_RATES[workout_name]
        else:
            print("  Enter a number between 1 and 6.")


def log_workout(active_user):
    """
    Purpose: Record a workout session for the signed-in user. Collects the workout type, duration, and an optional note. Calculates estimated calories burned and saves the entry.
    Arguments: active_user -- username of the currently signed-in user
    Returns: Nothing
    """
    print("\n*** Log Workout ***")

    # Choose workout type and get corresponding burn rate
    w_type, burn_rate = pick_workout_type()
    # Duration: whole number between 1 and 300 minutes
    mins = int(validated_number("  Duration in minutes (1-300): ", 1, 300, True))
    # Calculate estimated calories burned
    kcal_out = mins * burn_rate

    note = input("  Add a note (Enter to skip): ").strip()
    if note == "":
        note = "none"
    row = (active_user + "," + w_type + "," +
           str(mins) + "," + str(kcal_out) + "," + note)
    append_row(FILES["sessions"], row)

    print("  Saved! Estimated burn: " + str(kcal_out) + " kcal.")


# SECTION 5: NUTRITION LOGGING

def log_nutrition(active_user):
    """
    Purpose: Record a nutrition entry for the signed-in user. Collects the food item name and nutritional values, then saves the entry.
    Arguments: active_user -- username of the currently signed-in user
    Returns: Nothing
    """
    print("\n*** Log Nutrition ***")
    food_name = input("  Food item name: ").strip()
    if food_name == "":
        food_name = "Unnamed item"

    # Collect all nutritional values (must be >= 0, decimals allowed)
    kcal_val = validated_number("  Calories (kcal) : ", 0, -1, False)
    carbs_val = validated_number("  Carbs (g)       : ", 0, -1, False)
    protein_val = validated_number("  Protein (g)     : ", 0, -1, False)
    fat_val = validated_number("  Fat (g)         : ", 0, -1, False)

    # Build and save the row
    row = (active_user + "," + food_name + "," +
           str(kcal_val) + "," + str(carbs_val) + "," +
           str(protein_val) + "," + str(fat_val))
    append_row(FILES["nutrition"], row)
    print("  Nutrition entry saved.")


# SECTION 6: HEALTH TARGETS
def target_label(code):
    """
    Purpose: Convert a target code into a human-friendly label for display.
    Arguments: code -- the target type code (e.g. "weekly_kcal_burn")
    Returns: A string label to show to the user for this target type.
    """
    if code == "weekly_kcal_burn":
        return "Weekly Calorie Burn (kcal)"
    elif code == "protein_daily_g":
        return "Daily Protein Intake (g)"
    elif code == "workout_sessions":
        return "Total Workout Sessions"
    else:
        return code


def set_target(active_user):
    """
    Purpose: Allow the user to set or update a health target. The user picks a target type, enters a target value, and the system saves it. If a target of the same type already exists for this user, it is overwritten.
    Arguments: active_user -- username of the currently signed-in user
    Returns: Nothing
    """
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
    old_rows = read_rows(FILES["targets"])
    new_rows = []
    found_it = False

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
        overwrite_rows(FILES["targets"],
                       "username,target_type,target_value,current_value",
                       new_rows)
        print("  Target updated successfully.")
    else:
        new_entry = (active_user + "," + t_code + "," +
                     str(t_val) + ",0")
        append_row(FILES["targets"], new_entry)
        print("  New target saved.")


def draw_bar(pct, bar_width):
    """
    Purpose: Create a text-based progress bar string for a given percentage.
    Arguments:
    pct       -- the percentage to represent (0 to 100)
    bar_width -- the total width of the bar in characters
    Returns: A string representing the progress bar, e.g. "[#####-----]" for 50% with a width of 10.
    """
    if pct > 100.0:
        pct = 100.0
    if pct < 0.0:
        pct = 0.0

    filled = int((pct / 100.0) * bar_width)

    # Build filled portion using a counter loop
    bar_str = "["
    count = 0
    while count < filled:
        bar_str = bar_str + "#"
        count = count + 1

    # Build empty portion
    count = 0
    while count < (bar_width - filled):
        bar_str = bar_str + "-"
        count = count + 1

    bar_str = bar_str + "]"
    return bar_str


def view_progress(active_user):
    """
    Purpose: Show the user's progress towards each of their health targets. For each target, calculates the current value from the session and nutrition logs, then displays a progress bar and numeric summary.
    Arguments: active_user -- username of the currently signed-in user
    Returns: Nothing
    """
    print("\n*** Target Progress ***")

    # Load targets for this user
    target_rows = read_rows(FILES["targets"])
    my_targets = []
    for row in target_rows:
        parts = row.split(",")
        if len(parts) >= 3:
            if parts[0].strip() == active_user:
                my_targets.append(parts)

    if len(my_targets) == 0:
        print("  No targets set yet. Use option 3 to set one.")
        return

    #  Calculate current totals from session_log
    session_rows = read_rows(FILES["sessions"])
    total_sessions = 0
    total_kcal_burn = 0.0

    for row in session_rows:
        parts = row.split(",")
        if len(parts) >= 5:
            if parts[0].strip() == active_user:
                total_sessions = total_sessions + 1
                try:
                    if len(parts) >= 6:
                        total_kcal_burn = total_kcal_burn + float(parts[4].strip())
                    else:
                        total_kcal_burn = total_kcal_burn + float(parts[3].strip())
                except ValueError:
                    pass

    #  Calculate average daily protein from nutrition_log
    nutrition_rows = read_rows(FILES["nutrition"])
    protein_by_day = {}

    for row in nutrition_rows:
        parts = row.split(",")
        if len(parts) >= 6:
            if parts[0].strip() == active_user:
                if len(parts) >= 7:
                    entry_date = parts[1].strip()
                    protein_index = 5
                else:
                    entry_date = "all_entries"
                    protein_index = 4
                try:
                    p = float(parts[protein_index].strip())
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
        bar = draw_bar(pct, 25)

        print("\n  " + label)
        print("  " + bar + "  " + str(round(pct, 1)) + "%")
        print("  Current: " + str(round(current_val, 1)) +
              "  /  Target: " + str(t_goal))


# SECTION 7:SUMMARY
def overall_summary(active_user):
    """
    Purpose: Show a summary of the user's overall workout and nutrition stats, and a net energy balance. Totals are calculated live from the session and nutrition logs.
    Arguments: active_user -- username of the currently signed-in user
    Returns: Nothing
    """
    print("\n*** Summary ***")

    #  Workout totals
    session_rows = read_rows(FILES["sessions"])
    w_count, total_mins, total_kcal_out = 0.0, 0.0, 0.0

    for row in session_rows:
        parts = row.split(",")
        if len(parts) >= 5:
            if parts[0].strip() == active_user:
                w_count = w_count + 1
                try:
                    if len(parts) >= 6:
                        total_mins = total_mins + int(parts[3].strip())
                        total_kcal_out = total_kcal_out + float(parts[4].strip())
                    else:
                        total_mins = total_mins + int(parts[2].strip())
                        total_kcal_out = total_kcal_out + float(parts[3].strip())
                except ValueError:
                    pass

    #  Nutrition totals
    nutrition_rows = read_rows(FILES["nutrition"])
    f_count = 0
    total_kcal_in = 0.0
    total_carbs = 0.0
    total_protein = 0.0
    total_fat = 0.0

    for row in nutrition_rows:
        parts = row.split(",")
        if len(parts) >= 6:
            if parts[0].strip() == active_user:
                f_count = f_count + 1
                try:
                    if len(parts) >= 7:
                        total_kcal_in = total_kcal_in + float(parts[3].strip())
                        total_carbs = total_carbs + float(parts[4].strip())
                        total_protein = total_protein + float(parts[5].strip())
                        total_fat = total_fat + float(parts[6].strip())
                    else:
                        total_kcal_in = total_kcal_in + float(parts[2].strip())
                        total_carbs = total_carbs + float(parts[3].strip())
                        total_protein = total_protein + float(parts[4].strip())
                        total_fat = total_fat + float(parts[5].strip())
                except ValueError:
                    pass

    #  Net energy balance
    net_balance = total_kcal_in - total_kcal_out

    #  Display the results
    print("\n  [ WORKOUTS | " + str(w_count) + " session(s) ]")
    print("    Active time     -> " + str(total_mins) + " mins")
    print("    Calories out    -> " + str(round(total_kcal_out, 1)) + " kcal")

    print("\n  [ NUTRITION | " + str(f_count) + " entry/entries ]")
    print("    Calories in     -> " + str(round(total_kcal_in, 1)) + " kcal")
    print("    Carbohydrates   -> " + str(round(total_carbs, 1)) + " g")
    print("    Protein         -> " + str(round(total_protein, 1)) + " g")
    print("    Fat             -> " + str(round(total_fat, 1)) + " g")

    print("\n  NET BALANCE : " + str(round(net_balance, 1)) + " kcal")

    if net_balance < 0.0:
        print("  (Calorie deficit -- supports weight loss)")
    elif net_balance > 0.0:
        print("  (Calorie surplus -- supports muscle gain)")
    else:
        print("  (Calories are balanced)")


# SECTION 8 :MAIN MENU AND APPLICATION ENTRY POINT
def main_screen(active_user):
    """
    Purpose: Display the main menu for the signed-in user, and handle their choices until they sign out. The menu shows options to log workouts, log nutrition, set targets, view progress, and see a summary.
    Arguments: active_user -- username of the currently signed-in user
    Returns: Nothing
    """
    keep_going = True
    while keep_going:
        print("  HealthMate  |  " + active_user)
        print("***************************************")
        print("  1. Log workout")
        print("  2. Log nutrition")
        print("  3. Set health target")
        print("  4. View target progress")
        print("  5. Summary")
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
            overall_summary(active_user)
        elif opt == "6":
            print("\n  Signed out. Take care, " + active_user + "!")
            keep_going = False
        else:
            print("  Wrong choice. Enter a number from 1 to 6.")


def run():
    """
    Purpose: The main entry point of the application. Displays the welcome banner and prompts the user to sign in, create an account, or exit. Loops until the user chooses to exit.
    Arguments: None
    Returns: Nothing
    """
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
        print("\n  1. Log in\n2. Create account\n3. Exit")
        choice = input("\n  Choose: ").strip()

        if choice == "1":
            user = sign_in()
            if user is not None:
                print("User '" + user + "' signed in successfully.")
                main_screen(user)

        elif choice == "2":
            user = new_account()
            if user is not None:
                print("User '" + user + "' created successfully.")
                # Go straight to the main menu after registering
                main_screen(user)

        elif choice == "3":
            print("\nThank you for using HealthMate.")
            running = False

        else:
            print("Something went wrong. Please enter 1, 2, or 3.")


# Run the application
run()
