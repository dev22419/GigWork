# importing date from datetime so we can get today's date
from datetime import date

# these are the file names where we save all the data
# i am using variables so i don't have to type the names again and again
USERS_FILE      = "users.txt"       # this file stores usernames and passwords
ACTIVITIES_FILE = "activities.txt"  # this file stores all the workouts
NUTRITION_FILE  = "nutrition.txt"   # this file stores food/calorie info
GOALS_FILE      = "goals.txt"       # this file stores the fitness goals


# this function checks if a file exists
# if it doesn't exist, it creates a new one with a header line
def create_file_if_not_exists(filename, header):

    try:
        # try to open the file to see if it already exists
        f = open(filename, "r")
        f.close()  # close it if it opened successfully, we don't need to do anything

    except FileNotFoundError:
        # if file not found, we create a new one and write the header
        f = open(filename, "w")
        f.write(header + "\n")  # write the header and go to next line
        f.close()


# this function sets up all 4 files at the start of the program
# it calls the above function 4 times, one for each file
def setup_files():
    create_file_if_not_exists(USERS_FILE,      "username,password")
    create_file_if_not_exists(ACTIVITIES_FILE, "username,date,type,duration_mins,intensity")
    create_file_if_not_exists(NUTRITION_FILE,  "username,date,calories,carbs_g,protein_g,fat_g")
    create_file_if_not_exists(GOALS_FILE,      "username,goal_type,target,current")


# this function reads a file and gives back all the rows as a list of dictionaries
# dictionary is like key = column name, value = actual data
def read_file(filename):
    result = []   # empty list, we will add rows here

    # open file and read everything
    f = open(filename, "r")
    all_lines = f.readlines()   # readlines() gives each line as item in a list
    f.close()

    # if file has only header or is empty, return empty list
    if len(all_lines) < 2:
        return result

    # first line is the header (like "username,password")
    header_line = all_lines[0].strip()   # strip() removes spaces and newlines
    headers = header_line.split(",")     # split by comma to get list of column names

    # now loop through all other lines (skip line 0 because that's the header)
    for i in range(1, len(all_lines)):
        line = all_lines[i].strip()   # remove extra whitespace
        if line == "":
            continue   # skip empty lines
        values = line.split(",")   # split the line by comma

        # create a dictionary for this row
        row = {}
        for j in range(len(headers)):
            if j < len(values):
                row[headers[j]] = values[j]   # match column name to value
            else:
                row[headers[j]] = ""   # if value is missing, put empty string
        result.append(row)   # add this row to our list

    return result   # give back the full list of rows


# this function adds a new row at the bottom of a file
# values is a list like [username, date, calories, ...]
def append_to_file(filename, values):
    # join all values with comma to make one line
    line = ""
    for i in range(len(values)):
        if i == 0:
            line = str(values[i])           # first value, no comma before it
        else:
            line = line + "," + str(values[i])   # add comma before other values

    # open file in append mode ("a" means add at the end, not overwrite)
    f = open(filename, "a")
    f.write(line + "\n")   # write the line and go to next line
    f.close()


# this function re-writes the whole file from scratch
# we use this when we need to update/edit a row (like changing a goal)
def overwrite_file(filename, header, rows):
    # open in write mode ("w") which clears the file first
    f = open(filename, "w")
    f.write(header + "\n")   # write the header first
    headers = header.split(",")   # get list of column names

    # write each row one by one
    for row in rows:
        line = ""
        for i in range(len(headers)):
            col = headers[i]
            if i == 0:
                line = str(row[col])               # first column
            else:
                line = line + "," + str(row[col])  # rest of columns
        f.write(line + "\n")   # write the row

    f.close()


# this function lets a new user create an account
# returns the username if successful, otherwise returns None
def register():
    print("\n--- Register New Account ---")
    username = input("Choose a username: ").strip()

    # check if username is already taken
    users = read_file(USERS_FILE)
    for user in users:
        if user["username"] == username:
            print("That username is already taken. Please try a different one.")
            return None   # stop here and return nothing

    # get password from user
    password = input("Choose a password: ").strip()

    # save new user to file
    append_to_file(USERS_FILE, [username, password])
    print("Account created! Welcome, " + username + ".")
    return username   # return username so we know who is logged in


# this function lets an existing user login
# returns the username if login is correct, otherwise returns None
def login():
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    # read all users from the file
    users = read_file(USERS_FILE)

    # check if username and password match any user in the file
    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login successful! Welcome back, " + username + ".")
            return username   # login success!

    # if we get here, no match was found
    print("Incorrect username or password. Please try again.")
    return None


# this function lets the user log their physical activity for today
def log_activity(username):
    print("\n--- Log Physical Activity ---")
    today = str(date.today())   # get today's date as a string like "2024-01-15"

    # user can enter multiple activities at once, separated by commas
    activity_input = input("Activity type(s), separated by commas (e.g. running, cycling): ").strip()
    activity_list = activity_input.split(",")   # split into individual activities
    logged_count = 0   # keep track of how many we logged

    # loop through each activity
    for i in range(len(activity_list)):
        activity_type = activity_list[i].strip()   # remove spaces around name
        if activity_type == "":
            continue   # skip if empty (user put two commas maybe)

        print("\nDetails for: " + activity_type)

        # keep asking for duration until user gives a valid positive number
        while True:
            try:
                duration = int(input("  Duration (in minutes): "))
                if duration > 0:
                    break   # good input, exit the loop
                else:
                    print("  Please enter a positive number greater than zero.")
            except ValueError:
                # ValueError happens when user types letters instead of a number
                print("  Please enter a whole number (e.g. 30).")

        # ask for intensity level
        print("  Intensity levels: 1 = Low   2 = Medium   3 = High")
        while True:
            intensity_choice = input("  Select intensity (1/2/3): ").strip()
            if intensity_choice == "1":
                intensity = "Low"
                break
            elif intensity_choice == "2":
                intensity = "Medium"
                break
            elif intensity_choice == "3":
                intensity = "High"
                break
            else:
                print("  Invalid selection. Please enter 1, 2, or 3.")

        # save this activity to the file
        append_to_file(ACTIVITIES_FILE, [username, today, activity_type, duration, intensity])

        print("  Logged: " + activity_type + " for " + str(duration) + " mins at " + intensity + " intensity.")
        logged_count = logged_count + 1   # increase counter by 1

    print("\n" + str(logged_count) + " activity/activities logged successfully!")


# this is a helper function to get a number from user
# it keeps asking until user enters a valid number that is 0 or more
def get_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))   # float() allows decimals like 65.5
            if value >= 0:
                return value   # valid number, return it
            else:
                print("Please enter a positive number (0 or more).")
        except ValueError:
            # user typed something that is not a number
            print("Please enter a valid number (e.g. 1800 or 65.5).")


# this function lets user log what they ate today
def log_nutrition(username):
    print("\n--- Log Nutrition / Calorie Intake ---")
    today = str(date.today())   # get today's date

    # ask for each nutrition value using our helper function
    calories = get_positive_number("Total calories consumed today: ")
    carbs    = get_positive_number("Carbohydrates (grams): ")
    protein  = get_positive_number("Protein (grams): ")
    fat      = get_positive_number("Fat (grams): ")

    # save nutrition data to file
    append_to_file(NUTRITION_FILE, [username, today, calories, carbs, protein, fat])
    print("Nutrition logged: " + str(calories) + " kcal  |  " + str(carbs) + "g carbs  |  " + str(protein) + "g protein  |  " + str(fat) + "g fat.")


# this function lets user set a fitness goal
def set_fitness_plan(username):
    print("\n--- Set Fitness Goal ---")
    print("  1. Weight loss      (target kg to lose)")
    print("  2. Running distance (target total km)")
    print("  3. Workout sessions (target sessions per week)")

    choice = input("Select goal type (1/2/3): ").strip()

    # convert user choice to a goal type name
    if choice == "1":
        goal_type = "weight_loss_kg"
    elif choice == "2":
        goal_type = "running_km"
    elif choice == "3":
        goal_type = "sessions_per_week"
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
        return   # exit the function early if invalid

    # ask for the target value
    while True:
        try:
            target = float(input("Enter your target value: "))
            if target > 0:
                break   # valid target, exit loop
            else:
                print("Target must be greater than zero.")
        except ValueError:
            print("Please enter a valid number.")

    # check if user already has this goal type saved
    goals = read_file(GOALS_FILE)
    goal_found = False
    for goal in goals:
        if goal["username"] == username and goal["goal_type"] == goal_type:
            # update existing goal instead of adding a new one
            goal["target"]  = str(target)
            goal["current"] = "0"   # reset progress to 0
            goal_found = True
            break

    if goal_found:
        # if goal existed, overwrite the file with the updated version
        overwrite_file(GOALS_FILE, "username,goal_type,target,current", goals)
        print("Goal updated successfully!")
    else:
        # if goal is new, just append it to the file
        append_to_file(GOALS_FILE, [username, goal_type, target, 0])
        print("Goal set successfully!")


# this function draws a simple text progress bar
# like [################----] 80%
def draw_progress_bar(percent):
    # figure out how many # symbols to show (max is 20)
    filled_count = int(percent / 5)
    if filled_count > 20:
        filled_count = 20   # can't go more than 20 #'s

    empty_count = 20 - filled_count   # rest are dashes

    # build the bar string character by character
    bar = ""
    for i in range(filled_count):
        bar = bar + "#"   # filled part
    for i in range(empty_count):
        bar = bar + "-"   # empty part

    return "[" + bar + "] " + str(percent) + "%"


# this helper function converts goal_type code to a readable label
def get_goal_label(goal_type):
    if goal_type == "weight_loss_kg":
        return "Weight Loss (kg)"
    elif goal_type == "running_km":
        return "Running Distance (km)"
    elif goal_type == "sessions_per_week":
        return "Workout Sessions Per Week"
    else:
        return goal_type   # if unknown type, just return it as is


# this function shows the user how close they are to their goals
def view_progress(username):
    print("\n--- Progress Towards Fitness Goals ---")

    # read all goals and filter only this user's goals
    goals = read_file(GOALS_FILE)
    user_goals = []
    for goal in goals:
        if goal["username"] == username:
            user_goals.append(goal)

    # if user has no goals yet, tell them to set one
    if len(user_goals) == 0:
        print("You have no goals set yet.")
        print("Select option 4 from the main menu to set a fitness goal.")
        return

    # read activity data to calculate running km and total sessions
    activities = read_file(ACTIVITIES_FILE)
    user_activities = []
    for activity in activities:
        if activity["username"] == username:
            user_activities.append(activity)

    # count total number of workout sessions
    total_sessions = len(user_activities)

    # estimate running distance: assume 0.15 km per minute of running
    total_running_km = 0
    for a in user_activities:
        activity_lower = a["type"].lower()   # lowercase so "Running" and "running" both work
        if "run" in activity_lower:
            distance = int(a["duration_mins"]) * 0.15   # 0.15 km per minute is the estimate
            total_running_km = total_running_km + distance
    total_running_km = round(total_running_km, 2)   # round to 2 decimal places

    # now show progress for each goal
    for goal in user_goals:
        target    = float(goal["target"])   # what the user wants to reach
        goal_type = goal["goal_type"]       # what type of goal it is

        # figure out current progress based on goal type
        if goal_type == "running_km":
            current = total_running_km        # use calculated running distance
        elif goal_type == "sessions_per_week":
            current = total_sessions          # use total session count
        else:
            current = float(goal["current"])  # for weight loss, use saved value

        # calculate percentage done (how far are they from the goal)
        if target > 0:
            percent = round((current / target) * 100, 1)
            if percent > 100:
                percent = 100   # cap at 100% even if they exceeded target
        else:
            percent = 0

        # print the goal info with a progress bar
        label = get_goal_label(goal_type)
        print("\nGoal    : " + label)
        print("Target  : " + str(target))
        print("Current : " + str(current))
        print(draw_progress_bar(percent))


# this function shows a summary of today's activity and all-time stats
def fitness_summary(username):
    print("\n--- Fitness Summary ---")
    today = str(date.today())

    # get all activities for this user
    activities = read_file(ACTIVITIES_FILE)
    user_activities = []
    for a in activities:
        if a["username"] == username:
            user_activities.append(a)

    # filter only today's activities
    today_activities = []
    for a in user_activities:
        if a["date"] == today:
            today_activities.append(a)

    cal_burned        = 0   # total calories burned today
    total_active_mins = 0   # total minutes of exercise today

    # calculate calories burned based on intensity
    for a in today_activities:
        mins = int(a["duration_mins"])
        total_active_mins = total_active_mins + mins

        # different intensities burn different calories per minute
        intensity = a["intensity"]
        if intensity == "Low":
            cal_burned = cal_burned + (mins * 5)    # 5 calories per minute
        elif intensity == "Medium":
            cal_burned = cal_burned + (mins * 8)    # 8 calories per minute
        elif intensity == "High":
            cal_burned = cal_burned + (mins * 11)   # 11 calories per minute
        else:
            cal_burned = cal_burned + (mins * 5)    # default to low if unknown

    # read nutrition data and get today's entries
    nutrition = read_file(NUTRITION_FILE)
    today_nutrition = []
    for n in nutrition:
        if n["username"] == username and n["date"] == today:
            today_nutrition.append(n)

    # add up all calories consumed today
    cal_in = 0
    for n in today_nutrition:
        cal_in = cal_in + float(n["calories"])

    # net calories = calories eaten minus calories burned
    net_calories = cal_in - cal_burned

    # print today's summary
    print("\n  Today (" + today + "):")
    print("    Workouts completed : " + str(len(today_activities)))
    print("    Active time        : " + str(total_active_mins) + " minutes")
    print("    Calories burned    : " + str(cal_burned) + " kcal")
    print("    Calories consumed  : " + str(cal_in) + " kcal")
    print("    Net calories       : " + str(net_calories) + " kcal")

    # calculate all-time total active minutes
    all_time_mins = 0
    for a in user_activities:
        all_time_mins = all_time_mins + int(a["duration_mins"])

    # print all-time totals
    print("\n  All-time totals:")
    print("    Total sessions     : " + str(len(user_activities)))
    print("    Total active time  : " + str(all_time_mins) + " minutes")


# this is the main menu that shows after login
# it keeps running in a loop until user chooses to logout
def main_menu(username):

    while True:
        # print the menu every time
        print("\n=============================")
        print("   Health & Fitness Tracker  ")
        print("   Logged in as: " + username)
        print("=============================")
        print("  1. Log Physical Activity")
        print("  2. Log Nutrition / Calories")
        print("  3. View Progress Towards Goals")
        print("  4. Set Fitness Plan / Goals")
        print("  5. View Fitness Summary")
        print("  6. Logout")
        print("-----------------------------")

        choice = input("Select an option (1-6): ").strip()

        # call the right function based on user's choice
        if choice == "1":
            log_activity(username)
        elif choice == "2":
            log_nutrition(username)
        elif choice == "3":
            view_progress(username)
        elif choice == "4":
            set_fitness_plan(username)
        elif choice == "5":
            fitness_summary(username)
        elif choice == "6":
            # logout means we break out of the while loop
            print("\nGoodbye, " + username + "! Keep up the great work!")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 6.")


# this is the starting function that runs first
# it shows login/register screen before anything else
def main():
    setup_files()   # make sure all files exist before we start

    # welcome message
    print("=================================")
    print("  Welcome to Health and Fitness Tracker")
    print("=================================")

    current_user = None   # no one is logged in at start

    # keep showing login/register until someone logs in
    while current_user is None:
        print("\n  1. Login")
        print("  2. Register")
        print("  3. Exit")

        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            current_user = login()      # login() returns username or None
        elif choice == "2":
            current_user = register()   # register() returns username or None
        elif choice == "3":
            print("Goodbye!")
            return   # exit the whole program
        else:
            print("Invalid option. Please enter 1, 2, or 3.")

    # once logged in, go to the main menu
    main_menu(current_user)


# this is the standard Python thing to run main() when we run this file
# if someone imports this file, main() won't run automatically
if __name__ == "__main__":
    main()