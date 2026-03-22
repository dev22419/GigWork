# basic import for gui 
from tkinter import *    

# main window making
MainWindow = Tk()
MainWindow.title("expense tracker app")  

# list for storing data
expList = []   

# days list
DaysLIST = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# tracking day
DayIndex = 0  

# label
lbl = Label(MainWindow , text="enter expense for Monday")  
lbl.pack()

# entry
ent = Entry(MainWindow)
ent.pack()

# message label
msgLbl = Label(MainWindow , text="")
msgLbl.pack()

# function for button
def CLICKbtn():   

 global DayIndex   # using global because simple way

 # getting input
 val = ent.get().strip()  

 try:
  num = float(val)  

  if num < 0:  
     msgLbl.config(text="no negative pls enter again")
     return

  expList.append(num)  

  DayIndex = DayIndex + 1  

  ent.delete(0,END)

  if DayIndex < 7:

     nxt = DaysLIST[DayIndex]  
     lbl.config(text="enter expense for " + nxt)
     msgLbl.config(text="")  

  else:

    total = 0  
    i = 0

    # loop for sum
    while i < len(expList):
        total = total + expList[i]
        i = i + 1  

    avg = total / 7  

    # finding max min
    maxVal = expList[0]
    minVal = expList[0]

    j = 0
    while j < len(expList):

        if expList[j] > maxVal:
            maxVal = expList[j]

        if expList[j] < minVal:
            minVal = expList[j]

        j = j + 1  

    # find day names
    maxDay = ""
    minDay = ""

    k = 0
    while k < len(expList):

        if expList[k] == maxVal:
            maxDay = DaysLIST[k]

        if expList[k] == minVal:
            minDay = DaysLIST[k]

        k = k + 1

    # result text
    res = "total = " + str(total) + "\n"
    res = res + "avg = " + str(avg) + "\n"
    res = res + "highest = " + maxDay + "\n"
    res = res + "lowest = " + minDay  

    msgLbl.config(text=res)

 except:
   msgLbl.config(text="wrong input bro enter number")  


# button
btn = Button(MainWindow , text="submit value now", command=CLICKbtn)
btn.pack()

MainWindow.mainloop()