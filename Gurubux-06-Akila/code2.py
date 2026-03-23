from tkinter import *

# create main window
mainApplicationWindow = Tk()
mainApplicationWindow.title("My Simple Fitness Tracker App Without Much Functions")

# this will store current user name
currentlyLoggedInUserNameStorage = ""


# making login frame
loginFrameContainer = Frame(mainApplicationWindow)
loginFrameContainer.pack()

# username input box
Label(loginFrameContainer, text="Enter Your Username Here").pack()
usernameInputEntryFieldBox = Entry(loginFrameContainer)
usernameInputEntryFieldBox.pack()

# password input box
Label(loginFrameContainer, text="Enter Your Password Carefully").pack()
passwordInputEntryFieldBox = Entry(loginFrameContainer)
passwordInputEntryFieldBox.pack()

# this label will show msg
statusMessageLabelForUser = Label(loginFrameContainer, text="")
statusMessageLabelForUser.pack()


# frame after login
menuFrameAfterLogin = Frame(mainApplicationWindow)

# activity inputs
activityNameInputBoxField = Entry(menuFrameAfterLogin)
activityDurationInputBoxField = Entry(menuFrameAfterLogin)
activityIntensityInputBoxField = Entry(menuFrameAfterLogin)

# food inputs
foodNameInputBoxField = Entry(menuFrameAfterLogin)
calorieInputBoxField = Entry(menuFrameAfterLogin)

# output box for showing data
outputDisplayBigTextAreaBox = Text(menuFrameAfterLogin, height=15, width=50)


# function for login
def performLoginButtonOperationVerySimple():

    global currentlyLoggedInUserNameStorage

    # getting input values
    enteredUsernameValue = usernameInputEntryFieldBox.get().strip()
    enteredPasswordValue = passwordInputEntryFieldBox.get().strip()

    try:
        # open file to read users
        userFileReadObject = open("users.txt", "r")
        completeUserFileDataString = userFileReadObject.read().strip()
        userFileReadObject.close()

        # check username and password
        if enteredUsernameValue in completeUserFileDataString and enteredPasswordValue in completeUserFileDataString:
            currentlyLoggedInUserNameStorage = enteredUsernameValue

            # change screen
            loginFrameContainer.pack_forget()
            menuFrameAfterLogin.pack()

        else:
            statusMessageLabelForUser.config(text="Wrong Username or Password Try Again")

    except:
        statusMessageLabelForUser.config(text="Error While Reading User File")


# login button
Button(loginFrameContainer, text="Click Here To Login", command=performLoginButtonOperationVerySimple).pack()


# function to register new user
def performUserRegistrationProcessVeryBasic():

    # take input from user
    newUsernameFromInputBox = usernameInputEntryFieldBox.get().strip()
    newPasswordFromInputBox = passwordInputEntryFieldBox.get().strip()

    # save user in file
    userFileAppendObject = open("users.txt", "a")
    userFileAppendObject.write(newUsernameFromInputBox + "," + newPasswordFromInputBox + "\n")
    userFileAppendObject.close()

    # show success msg
    statusMessageLabelForUser.config(text="Registration Completed Successfully")


# register button
Button(loginFrameContainer, text="Click Here To Register New User", command=performUserRegistrationProcessVeryBasic).pack()


# label for activity
Label(menuFrameAfterLogin, text="Enter Your Daily Activity Details Below").pack()

# show activity inputs
activityNameInputBoxField.pack()
activityDurationInputBoxField.pack()
activityIntensityInputBoxField.pack()

# label for food
Label(menuFrameAfterLogin, text="Enter Your Food Intake Details Below").pack()

# show food inputs
foodNameInputBoxField.pack()
calorieInputBoxField.pack()

# show output box
outputDisplayBigTextAreaBox.pack()


# function to save activity
def saveActivityDataIntoFileFunctionSimple():

    # get activity values
    activityNameValue = activityNameInputBoxField.get().strip()
    activityDurationValue = activityDurationInputBoxField.get().strip()
    activityIntensityValue = activityIntensityInputBoxField.get().strip()

    # write activity in file
    activityFileObject = open("data.txt", "a")
    activityFileObject.write(currentlyLoggedInUserNameStorage + ",A," +
                             activityNameValue + "," +
                             activityDurationValue + "," +
                             activityIntensityValue + "\n")
    activityFileObject.close()

    # show msg
    outputDisplayBigTextAreaBox.insert(END, "\nActivity Saved Successfully")


# button for saving activity
Button(menuFrameAfterLogin, text="Save Activity Data Now", command=saveActivityDataIntoFileFunctionSimple).pack()


# function to save food data
def saveFoodDataIntoFileFunctionSimple():

    # write food data
    foodFileObject = open("data.txt", "a")
    foodFileObject.write(currentlyLoggedInUserNameStorage + ",F," +
                         foodNameInputBoxField.get().strip() + "," +
                         calorieInputBoxField.get().strip() + "\n")
    foodFileObject.close()

    # show msg
    outputDisplayBigTextAreaBox.insert(END, "\nFood Data Saved Successfully")


# button for saving food
Button(menuFrameAfterLogin, text="Save Food Data Now", command=saveFoodDataIntoFileFunctionSimple).pack()


# function to view saved data
def viewSavedDataForCurrentUserFunction():

    # clear old data
    outputDisplayBigTextAreaBox.delete(1.0, END)

    try:
        # read data file
        dataFileReadObject = open("data.txt", "r")
        allLinesFromDataFileList = dataFileReadObject.readlines()
        dataFileReadObject.close()

        # loop through lines
        for singleLineData in allLinesFromDataFileList:
            if currentlyLoggedInUserNameStorage in singleLineData:
                outputDisplayBigTextAreaBox.insert(END, singleLineData)

    except:
        outputDisplayBigTextAreaBox.insert(END, "No Data File Found Or Error Occured")


# button to view data
Button(menuFrameAfterLogin, text="View My Saved Data", command=viewSavedDataForCurrentUserFunction).pack()


# run the app
mainApplicationWindow.mainloop()