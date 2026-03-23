from tkinter import *

"""
This is my fitnes trakcer app project
i made this for practis and learning tkinter
it stores data in files so its very basic project
maybe some bugs are there but its working ok
"""

# main window create kar rahe hai
mainApplicationWindow = Tk()
mainApplicationWindow.title("My Simple Fitness Tracker App Without Much Functions")

# ye variable current user ko store karega
currentlyLoggedInUserNameStorage = ""


# login frame bana rahe hai
loginFrameContainer = Frame(mainApplicationWindow)
loginFrameContainer.pack()

# user name input lene ke liye
Label(loginFrameContainer, text="Enter Your Username Here").pack()
usernameInputEntryFieldBox = Entry(loginFrameContainer)
usernameInputEntryFieldBox.pack()

# password input field
Label(loginFrameContainer, text="Enter Your Password Carefully").pack()
passwordInputEntryFieldBox = Entry(loginFrameContainer)
passwordInputEntryFieldBox.pack()

# yaha pe msg show hoga login ya error ka
statusMessageLabelForUser = Label(loginFrameContainer, text="")
statusMessageLabelForUser.pack()


# menu frame jo login ke baad dikhega
menuFrameAfterLogin = Frame(mainApplicationWindow)

# activity ke inputs (naam, time, intensity wagere)
activityNameInputBoxField = Entry(menuFrameAfterLogin)
activityDurationInputBoxField = Entry(menuFrameAfterLogin)
activityIntensityInputBoxField = Entry(menuFrameAfterLogin)

# food ke inputs (food name aur calories)
foodNameInputBoxField = Entry(menuFrameAfterLogin)
calorieInputBoxField = Entry(menuFrameAfterLogin)

# output box jisme sab data print hoga
outputDisplayBigTextAreaBox = Text(menuFrameAfterLogin, height=15, width=50)


# ye login ka function hai jo check karega user exist karta hai ya nahi
def performLoginButtonOperationVerySimple():

    global currentlyLoggedInUserNameStorage

    enteredUsernameValue = usernameInputEntryFieldBox.get().strip()
    enteredPasswordValue = passwordInputEntryFieldBox.get().strip()

    try:
        # file open kar rahe hai read ke liye
        userFileReadObject = open("users.txt", "r")
        completeUserFileDataString = userFileReadObject.read().strip()
        userFileReadObject.close()

        # check kar rahe hai username aur password match ho raha hai ya nahi
        if enteredUsernameValue in completeUserFileDataString and enteredPasswordValue in completeUserFileDataString:
            currentlyLoggedInUserNameStorage = enteredUsernameValue

            # frame change kar rahe hai
            loginFrameContainer.pack_forget()
            menuFrameAfterLogin.pack()

        else:
            statusMessageLabelForUser.config(text="Wrong Username or Password Try Again")

    except:
        statusMessageLabelForUser.config(text="Error While Reading User File")


Button(loginFrameContainer, text="Click Here To Login", command=performLoginButtonOperationVerySimple).pack()


# ye register ka function hai jo new user save karega
def performUserRegistrationProcessVeryBasic():

    newUsernameFromInputBox = usernameInputEntryFieldBox.get().strip()
    newPasswordFromInputBox = passwordInputEntryFieldBox.get().strip()

    # file me likh rahe hai data
    userFileAppendObject = open("users.txt", "a")
    userFileAppendObject.write(newUsernameFromInputBox + "," + newPasswordFromInputBox + "\n")
    userFileAppendObject.close()

    statusMessageLabelForUser.config(text="Registration Completed Successfully")


Button(loginFrameContainer, text="Click Here To Register New User", command=performUserRegistrationProcessVeryBasic).pack()


# activity section ka label
Label(menuFrameAfterLogin, text="Enter Your Daily Activity Details Below").pack()
activityNameInputBoxField.pack()
activityDurationInputBoxField.pack()
activityIntensityInputBoxField.pack()

# food section ka label
Label(menuFrameAfterLogin, text="Enter Your Food Intake Details Below").pack()
foodNameInputBoxField.pack()
calorieInputBoxField.pack()

# output box show kar rahe hai
outputDisplayBigTextAreaBox.pack()


# ye function activity save karega file me
def saveActivityDataIntoFileFunctionSimple():

    activityNameValue = activityNameInputBoxField.get().strip()
    activityDurationValue = activityDurationInputBoxField.get().strip()
    activityIntensityValue = activityIntensityInputBoxField.get().strip()

    activityFileObject = open("data.txt", "a")
    activityFileObject.write(currentlyLoggedInUserNameStorage + ",A," +
                             activityNameValue + "," +
                             activityDurationValue + "," +
                             activityIntensityValue + "\n")
    activityFileObject.close()

    outputDisplayBigTextAreaBox.insert(END, "\nActivity Saved Successfully")


Button(menuFrameAfterLogin, text="Save Activity Data Now", command=saveActivityDataIntoFileFunctionSimple).pack()


# ye function food data save karega
def saveFoodDataIntoFileFunctionSimple():

    foodFileObject = open("data.txt", "a")
    foodFileObject.write(currentlyLoggedInUserNameStorage + ",F," +
                         foodNameInputBoxField.get().strip() + "," +
                         calorieInputBoxField.get().strip() + "\n")
    foodFileObject.close()

    outputDisplayBigTextAreaBox.insert(END, "\nFood Data Saved Successfully")


Button(menuFrameAfterLogin, text="Save Food Data Now", command=saveFoodDataIntoFileFunctionSimple).pack()


# ye function data dikhata hai user ka
def viewSavedDataForCurrentUserFunction():

    outputDisplayBigTextAreaBox.delete(1.0, END)

    try:
        dataFileReadObject = open("data.txt", "r")
        allLinesFromDataFileList = dataFileReadObject.readlines()
        dataFileReadObject.close()

        # har line check kar rahe hai
        for singleLineData in allLinesFromDataFileList:
            if currentlyLoggedInUserNameStorage in singleLineData:
                outputDisplayBigTextAreaBox.insert(END, singleLineData)

    except:
        outputDisplayBigTextAreaBox.insert(END, "No Data File Found Or Error Occured")


Button(menuFrameAfterLogin, text="View My Saved Data", command=viewSavedDataForCurrentUserFunction).pack()


# finally app run kar rahe hai
mainApplicationWindow.mainloop()