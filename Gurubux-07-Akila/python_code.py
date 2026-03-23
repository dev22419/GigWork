from tkinter import *

# global file names used in whole program
globalUserStorageFileName = "users_data_storage_file.txt"
globalActivityStorageFileName = "daily_activity_records_file.txt"

# creating main application window
mainWindowForFitnessAppProject = Tk()
mainWindowForFitnessAppProject.title("My Personal Fitness Tracking System With Basic Features")

# this variable stores current logged in user name
globalCurrentActiveUserNameHolder = ""


# function for login verification and moving to dashboard
def performLoginVerificationAndEnterDashboardScreen():

    """
    this function checks user credentials from file
    if correct then it will open dashboard screen
    otherwise it shows error message
    """

    global globalCurrentActiveUserNameHolder

    enteredUserNameFromInputBox = usernameInputBoxForLogin.get()
    enteredPasswordFromInputBox = passwordInputBoxForLogin.get()

    try:
        # opening file for reading user data
        userFileReadHandlerObject = open(globalUserStorageFileName, "r")
        completeUsersDataInOneStringFormat = userFileReadHandlerObject.read()
        userFileReadHandlerObject.close()

        # checking username and password in file data
        if enteredUserNameFromInputBox in completeUsersDataInOneStringFormat and enteredPasswordFromInputBox in completeUsersDataInOneStringFormat:
            globalCurrentActiveUserNameHolder = enteredUserNameFromInputBox

            # hiding login frame
            loginFrameContainerSection.pack_forget()

            # showing dashboard frame
            dashboardFrameAfterSuccessfulLogin.pack()

        else:
            loginStatusMessageLabel.config(text="Login Failed Please Check Username And Password Again Properly")

    except:
        loginStatusMessageLabel.config(text="Some Error Happened While Reading User File Data")


# login frame UI
loginFrameContainerSection = Frame(mainWindowForFitnessAppProject)
loginFrameContainerSection.pack()

# username input label and entry box
Label(loginFrameContainerSection, text="Please Enter Your Username In This Input Field Carefully").pack()
usernameInputBoxForLogin = Entry(loginFrameContainerSection)
usernameInputBoxForLogin.pack()

# password input label and entry box
Label(loginFrameContainerSection, text="Please Enter Your Password In This Input Field Properly").pack()
passwordInputBoxForLogin = Entry(loginFrameContainerSection)
passwordInputBoxForLogin.pack()

# message label for login status
loginStatusMessageLabel = Label(loginFrameContainerSection, text="")
loginStatusMessageLabel.pack()

# login button
Button(loginFrameContainerSection,
       text="Click Here To Perform Login Operation And Continue",
       command=performLoginVerificationAndEnterDashboardScreen).pack()


# function for registering new user
def performNewUserRegistrationAndStoreIntoFileSystem():

    """
    this function stores new user credentials into file
    it directly appends username and password without validation
    """

    newUserNameForRegistration = usernameInputBoxForLogin.get()
    newPasswordForRegistration = passwordInputBoxForLogin.get()

    userFileAppendHandlerObject = open(globalUserStorageFileName, "a")
    userFileAppendHandlerObject.write(newUserNameForRegistration + "," + newPasswordForRegistration + "\n")
    userFileAppendHandlerObject.close()

    loginStatusMessageLabel.config(text="New User Registration Completed Successfully You Can Login Now")


Button(loginFrameContainerSection,
       text="Click Here To Register New Account Into System",
       command=performNewUserRegistrationAndStoreIntoFileSystem).pack()


# dashboard frame after login
dashboardFrameAfterSuccessfulLogin = Frame(mainWindowForFitnessAppProject)

# activity input section
Label(dashboardFrameAfterSuccessfulLogin, text="Enter Your Daily Activity Name Below").pack()
activityNameInputFieldBoxForUser = Entry(dashboardFrameAfterSuccessfulLogin)
activityNameInputFieldBoxForUser.pack()

Label(dashboardFrameAfterSuccessfulLogin, text="Enter Duration Of Activity In Minutes Or Hours").pack()
activityDurationInputFieldBoxForUser = Entry(dashboardFrameAfterSuccessfulLogin)
activityDurationInputFieldBoxForUser.pack()

Label(dashboardFrameAfterSuccessfulLogin, text="Enter Calories Burned Or Intensity Level Value").pack()
activityCaloriesOrIntensityInputFieldBoxForUser = Entry(dashboardFrameAfterSuccessfulLogin)
activityCaloriesOrIntensityInputFieldBoxForUser.pack()

# text area to display output data
outputTextAreaForDisplayingUserData = Text(dashboardFrameAfterSuccessfulLogin, height=15, width=55)
outputTextAreaForDisplayingUserData.pack()


# function to save activity data
def performSavingActivityDataIntoFileStorageSystem():

    """
    this function saves activity data into file
    it also stores username with activity details
    includes a useless loop for practice purpose
    """

    activityNameValueFromUserInput = activityNameInputFieldBoxForUser.get()
    activityDurationValueFromUserInput = activityDurationInputFieldBoxForUser.get()
    activityCaloriesValueFromUserInput = activityCaloriesOrIntensityInputFieldBoxForUser.get()

    # dummy loop just for practice not needed
    tempListForNoReason = [activityNameValueFromUserInput, activityDurationValueFromUserInput]
    for itemValue in tempListForNoReason:
        pass

    activityFileAppendHandlerObject = open(globalActivityStorageFileName, "a")
    activityFileAppendHandlerObject.write(globalCurrentActiveUserNameHolder + ",ACTIVITY_RECORD," +
                                          activityNameValueFromUserInput + "," +
                                          activityDurationValueFromUserInput + "," +
                                          activityCaloriesValueFromUserInput + "\n")
    activityFileAppendHandlerObject.close()

    outputTextAreaForDisplayingUserData.insert(END,
        "\nYour Activity Data Has Been Saved Successfully Into The File Storage System")


Button(dashboardFrameAfterSuccessfulLogin,
       text="Click Here To Save Activity Data Into File",
       command=performSavingActivityDataIntoFileStorageSystem).pack()


# function to view saved data
def performViewingAllSavedDataForCurrentUser():

    """
    this function reads file and shows data
    it filters only current user records
    using simple for loop
    """

    outputTextAreaForDisplayingUserData.delete(1.0, END)

    try:
        dataFileReadHandlerObject = open(globalActivityStorageFileName, "r")
        allLinesFromFileListData = dataFileReadHandlerObject.readlines()
        dataFileReadHandlerObject.close()

        for singleLineFromFile in allLinesFromFileListData:
            if globalCurrentActiveUserNameHolder in singleLineFromFile:
                outputTextAreaForDisplayingUserData.insert(END, singleLineFromFile)

    except:
        outputTextAreaForDisplayingUserData.insert(END,
            "Error Occured While Reading Data File Or File Not Found In System")


Button(dashboardFrameAfterSuccessfulLogin,
       text="Click Here To View All Your Saved Activity Records",
       command=performViewingAllSavedDataForCurrentUser).pack()


# running the application window
mainWindowForFitnessAppProject.mainloop()