
"""
This is the main code file for the fitness tracker program. 
It includes functions for creating accounts, logging in, adding workout and food entries, setting goals, 
showing progress, and more. The program uses text files to save user data and allows users to track their 
fitness activities and goals over time.
"""
user_data_var = None

# this makes file if it is not there
def make_file(name_of_file,header):
    try:
        # try opening first .. if yes then file is already there
        with open(name_of_file,"r"):
            pass
    except FileNotFoundError:
        # if file not found ; make new one with heading
        with open(name_of_file,"w") as file:
            file.write(header + "\n")


# this starts all the text files
def start_files():
    make_file("members.txt","user_name,password")
    make_file("workout_log.txt","user_name,activity,minutes,level")
    make_file("food_entries.txt","user_name,meal,calories,carbs,protein,fat")
    make_file("targets.txt","user_name,goal_name,target,current")


# this reads all rows from file
def read_table(name_of_file):
    with open(name_of_file,"r") as file:
        lines = file.readlines()

    # start from 1 because line 0 is header ..
    i = 1
    rows = []
    while i < len(lines):
        line = lines[i].strip()
        if line != "":
            # split comma values ; then keep in rows list
            parts = line.split(",")
            rows.append(parts)
        i = i + 1
    return rows


# this adds one row in file
def write_row(name_of_file,values):
    line = ""
    i = 0
    while i < len(values):
        # making one csv line slowly ..
        if i == 0:
            line = str(values[i])
        else:
            line = line + "," + str(values[i])
        i = i + 1

    # now save line at the end of file ;
    with open(name_of_file,"a") as file:
        file.write(line + "\n")


# this writes full file again
def write_full_file(name_of_file,header,rows):
    with open(name_of_file,"w") as file:
        file.write(header + "\n")

        i = 0
        while i < len(rows):
            row = rows[i]
            line = ""
            j = 0
            while j < len(row):
                # this builds each row again .. value by value
                if j == 0:
                    line = str(row[j])
                else:
                    line = line + "," + str(row[j])
                j = j + 1
            file.write(line + "\n")
            i = i + 1


# this gets number from user
def get_number(message):
    while True:
        raw = input(message)
        try:
            value = float(raw)
            if value >= 0:
                # send number back if it is okay ;
                return value
            else:
                print("Please enter a value that is 0 or greater so it can be saved correctly.")
        except ValueError:
            print("That input was not read as a number. Please type the value again.")


def create_account():
    """
    This function allows a new user to create an account for the fitness tracker.
    """
    print("\nCreate a new account for the fitness tracker.")
    user_name = input("Username: ")

    # check all old users first ..
    users_data = read_table("members.txt")
    i = 0
    while i < len(users_data):
        if len(users_data[i]) >= 1 and users_data[i][0] == user_name:
            print("That user_name is already being used,so please choose a different one.")
            return None
        i = i + 1

    password = input("Password: ")
    # save new user_name and password ;
    write_row("members.txt",[user_name,password])
    print("Your account has been created successfully and is ready to use...")
    return user_name


# this checks login details
def login_account():
    """
    This function allows an existing user to log in to their fitness tracker account by verifying their user_name and password.
    """
    print("\nLogin to continue into your fitness tracker account.")
    user_name = input("Username:")
    password = input("Password:").strip()

    # compare entered details with saved users ..
    users = read_table("members.txt")
    i = 0
    while i < len(users):
        row = users[i]
        if len(row) >= 2:
            if row[0] == user_name and row[1] == password:
                print("Login successful. Your tracker menu will open now.")
                return user_name
        i = i + 1

    print("The user_name or password did not match our records. Please try again carefully!!")
    return None


# this adds workout data
def add_activity(user_name):
    """This function allows the user to add a workout or physical activity entry to their fitness tracker log, 
    including details such as activity name, duration, and intensity level.
    """
    print("\nAdd a workout or physical activity entry.")
    name = input("Activity name: ")

    # keep asking if user leaves it blank ;
    while name == "":
        print("The activity name was left empty,so please type something before continuing.")
        name = input("Activity name: ")

    minutes = -1
    while minutes <= 0:
        # only positive whole minutes should be saved ..
        raw = input("Minutes: ")
        try:
            minutes = int(raw)
            if minutes <= 0:
                print("Minutes need to be greater than 0 so the activity makes sense.")
        except ValueError:
            print("Please enter the minutes as a whole number,for example 20 or 45.")
            minutes = -1

    print("Choose the activity intensity level from the list below.")
    print("a. Low intensity")
    print("b. Medium intensity")
    print("c. High intensity")

    level = ""
    while level == "":
        # convert menu letter into text level ;
        choice = input("Option: ")
        if choice == "a":
            level = "Low"
        elif choice == "b":
            level = "Medium"
        elif choice == "c":
            level = "High"
        else:
            print("Please choose a valid option by entering a,b,or c.")

    write_row("workout_log.txt",[user_name,name,minutes,level])
    print("The activity entry has been saved to your workout log.")


# this adds food data
def add_food(user_name):
    """This function allows the user to add a food or meal entry to their fitness tracker log,
    including details such as meal name, calories, carbohydrates, protein, and fat content.
    """
    print("\nAdd a food or meal entry.")
    meal = input("Meal name: ")
    if meal == "":
        # simple default name .. if user types nothing
        meal = "Meal"

    # get all food numbers one by one ;
    calories = get_number("Calories: ")
    carbs = get_number("Carbs: ")
    protein = get_number("Protein: ")
    fat = get_number("Fat: ")

    write_row("food_entries.txt",[user_name,meal,calories,carbs,protein,fat])
    print("The food entry has been saved successfully in your daily log.")


# this is for setting goal
def set_goal(user_name):
    """
    This function allows the user to set or update a fitness goal in their account, such as a weight loss target,
    walking streak goal, or gym visits goal.
    """
    print("\nSet or update one of your fitness goals.\na. Weight loss goal\nb. Walking streak goal\nc. Gym visits goal")

    choice = input("Choose option: ")

    # turn menu choice into goal name ..
    if choice == "a":
        goal_name = "weight_loss"
    elif choice == "b":
        goal_name = "walking_streak"
    elif choice == "c":
        goal_name = "gym_visits"
    else:
        print("That option is not part of the goal menu. Please choose one of the listed letters.")
        return

    target = 0
    while target <= 0:
        raw = input("Target value: ")
        try:
            target = float(raw)
            if target <= 0:
                print("The target value must be greater than 0 to be useful.")
        except ValueError:
            print("That target was not a valid number. Please type it again.")
            target = 0

    goals = read_table("targets.txt")
    found = False
    i = 0
    while i < len(goals):
        # if same user goal is there ; update it
        row = goals[i]
        if len(row) >= 4:
            if row[0] == user_name and row[1] == goal_name:
                row[2] = str(target)
                row[3] = "0"
                found = True
                break
        i = i + 1

    if found:
        write_full_file("targets.txt","user_name,goal_name,target,current",goals)
        print("Your existing goal was found and updated with the new target value.")
    else:
        write_row("targets.txt",[user_name,goal_name,target,0])
        print("A new goal has been added to your goals file.")


# this shows better goal name
def goal_title(goal_name):
    """
    This function takes a goal name code and returns a more user-friendly title for display purposes.
    """
    if goal_name == "weight_loss":
        return "Weight Loss"
    elif goal_name == "walking_streak":
        return "Walking Streak"
    elif goal_name == "gym_visits":
        return "Gym Visits"
    else:
        return goal_name


# this shows user progress
def show_progress(user_name):
    """
    This function calculates and displays the user's current progress towards their fitness goals,
    including the percentage of completion and a visual progress bar, based on their logged activities and food entries.
    """
    print("\nHere is the current progress for the goals saved under your account.")
    goals = read_table("targets.txt")
    activities = read_table("workout_log.txt")

    my_goals = []
    i = 0
    while i < len(goals):
        # keep only this user goals ..
        if len(goals[i]) >= 4 and goals[i][0] == user_name:
            my_goals.append(goals[i])
        i = i + 1

    if len(my_goals) == 0:
        print("No goals were found for this account,so there is no progress to show yet...")
        return

    session_count = 0
    walking_count = 0.0
    i = 0
    while i < len(activities):
        row = activities[i]
        if len(row) >= 4 and row[0] == user_name:
            # count visits and track walking entries
            session_count = session_count + 1
            if len(row) >= 5:
                activity_name = row[2].lower()
            else:
                activity_name = row[1].lower()
            if "walk" in activity_name:
                walking_count = walking_count + 1
        i = i + 1

    i = 0
    while i < len(my_goals):
        row = my_goals[i]
        goal_name = row[1]
        target = float(row[2])

        if goal_name == "walking_streak":
            current = walking_count
        elif goal_name == "gym_visits":
            current = float(session_count)
        else:
            current = float(row[3])

        percent = 0.0
        if target > 0:
            # make progress into percent .. max 100
            percent = (current / target) * 100
            if percent > 100:
                percent = 100.0

        print("\nGoal name: " + goal_title(goal_name))
        print("Target value set: " + str(target))
        print("Current progress value: " + str(round(current,2)))
        print("Overall completion: " + str(round(percent,1)) + "%")

        stars = ""
        count = int(percent / 20)
        j = 0
        # this makes a small progress bar with stars ;
        while j < count:
            stars = stars + "*"
            j = j + 1
        while j < 5:
            stars = stars + "-"
            j = j + 1
        print("[" + stars + "]")

        i = i + 1


# this shows workout history
def show_history(user_name):
    """
    This function retrieves and displays the user's recent workout history from their fitness tracker log, 
    showing details such as activity name, duration, and intensity level for the last five entries.
    """
    print("\nShowing the recent workout history saved for your account.")
    activities = read_table("workout_log.txt")
    my_rows = []

    i = 0
    while i < len(activities):
        # take only rows for this user ..
        row = activities[i]
        if len(row) >= 4 and row[0] == user_name:
            my_rows.append(row)
        i = i + 1

    if len(my_rows) == 0:
        print("There is no workout history saved yet for this user.")
        return

    start = 0
    if len(my_rows) > 5:
        # only last 5 records ; if more are there
        start = len(my_rows) - 5

    number = 1
    i = start
    while i < len(my_rows):
        row = my_rows[i]
        if len(row) >= 5:
            activity_name = row[2]
            minutes = row[3]
            level = row[4]
        else:
            activity_name = row[1]
            minutes = row[2]
            level = row[3]
        print(str(number) + ". " + activity_name + " | " + minutes + " mins | " + level)
        number = number + 1
        i = i + 1


# this shows summary
def show_summary(user_name):
    """
    This function provides a summary of the user's fitness activities and food details, including total workouts logged,
    total active minutes, estimated calories burned, total calories eaten, and net calorie balance.
    """
    print("\nHere is a summary of your activity and food details.")
    activities = read_table("workout_log.txt")
    foods = read_table("food_entries.txt")

    total_minutes = 0
    total_burned = 0
    workout_count = 0

    i = 0
    while i < len(activities):
        row = activities[i]
        if len(row) >= 4 and row[0] == user_name:
            if len(row) >= 5:
                minutes = int(row[3])
                level = row[4]
            else:
                minutes = int(row[2])
                level = row[3]
            # count workout and add minutes ..
            workout_count = workout_count + 1
            total_minutes = total_minutes + minutes

            # calories change by level ; low medium high
            if level == "Low":
                total_burned = total_burned + (minutes * 5)
            elif level == "Medium":
                total_burned = total_burned + (minutes * 8)
            elif level == "High":
                total_burned = total_burned + (minutes * 11)
            else:
                total_burned = total_burned + (minutes * 5)
        i = i + 1

    total_food = 0.0
    i = 0
    while i < len(foods):
        row = foods[i]
        if len(row) >= 6 and row[0] == user_name:
            if len(row) >= 7:
                calories = float(row[3])
            else:
                calories = float(row[2])
            # add saved food calories ..
            total_food = total_food + calories
        i = i + 1

    # net means eaten minus burned ;
    net = total_food - total_burned

    print("Total workouts logged: " + str(workout_count))
    print("Total active minutes: " + str(total_minutes))
    print("Estimated calories burned: " + str(total_burned))
    print("Total calories eaten: " + str(total_food))
    print("Net calorie balance: " + str(round(net,1)))


# this shows main menu
def user_menu(user_name):
    """
    This function displays the main menu for the logged-in user, allowing them to manage their fitness activities and goals,
    and handles the user's menu choices to perform various actions such as adding entries, showing progress, and logging out.
    """
    while True:
        print("\nFitness Tracker Main Menu")
        print("You are currently logged in as: " + user_name)
        print("a. Add a workout activity entry")
        print("b. Add a food entry")
        print("c. Set or update a goal")
        print("d. Show progress for goals")
        print("e. Show recent workout history")
        print("f. Show summary")
        print("g. Logout from this account")

        choice = input("Enter option: ")

        # run function based on menu letter ..
        if choice == "a":
            add_activity(user_name)
        elif choice == "b":
            add_food(user_name)
        elif choice == "c":
            set_goal(user_name)
        elif choice == "d":
            show_progress(user_name)
        elif choice == "e":
            show_history(user_name)
        elif choice == "f":
            show_summary(user_name)
        elif choice == "g":
            print("You have been logged out and returned from the main menu...")
            break
        else:
            print("That menu option was not valid. Please enter a letter from the menu.")


"""
This is the main program execution block for the fitness tracker application. 
It initializes necessary files, welcomes the user, and manages the initial login or 
registration process before directing the user to the main menu.
"""
# first make sure files are ready ;
start_files()

print("Welcome to the Fitness Tracker program. Please login or register to continue.")

while user_data_var is None:
    print("\na. Login to an existing account")
    print("b. Register a new account")
    print("c. Exit the program")

    choice = input("Enter option: ")

    # stay here until user logs in .. or exits
    if choice == "a":
        user_data_var = login_account()
    elif choice == "b":
        user_data_var = create_account()
    elif choice == "c":
        print("The program has been closed. Goodbye.")
        exit()
    else:
        print("That was not a valid starting option. Please choose a,b,or c.")

user_menu(user_data_var)
