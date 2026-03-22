from tkinter import *  

# file name
fileNAME = "books.txt"  

# function to show books
def showBOOKS():  

    txtBox.delete(1.0 , END)

    try:
      f = open(fileNAME , "r")
      data = f.read().strip()  
      f.close()

      if data == "":
          txtBox.insert(END , "no books found")
      else:
          txtBox.insert(END , data)

    except:
      txtBox.insert(END , "file not found so no books")  


# function to add book
def addBOOK():  

    t = titleEnt.get().strip()
    a = authorEnt.get().strip()
    d = descEnt.get().strip()

    if t == "" or a == "" or d == "":
        txtBox.insert(END , "\nfill all fields properly pls\n")
        return

    # checking duplicate
    try:
        f2 = open(fileNAME , "r")
        dat = f2.read().strip()
        f2.close()

        if t in dat:
            txtBox.insert(END , "\nduplicate title not allowed\n")
            return
    except:
        pass  

    # writing
    f3 = open(fileNAME , "a")

    f3.write("Title: " + t + "\n")
    f3.write("Author: " + a + "\n")
    f3.write("Desc: " + d + "\n")
    f3.write("-----\n")

    f3.close()

    txtBox.insert(END , "\nbook added done\n")

    # clearing
    titleEnt.delete(0,END)
    authorEnt.delete(0,END)
    descEnt.delete(0,END)


# window
win = Tk()
win.title("book app")  

Label(win , text="enter title").pack()
titleEnt = Entry(win)
titleEnt.pack()

Label(win , text="enter author").pack()
authorEnt = Entry(win)
authorEnt.pack()

Label(win , text="enter desc").pack()
descEnt = Entry(win)
descEnt.pack()

Button(win , text="add book now", command=addBOOK).pack()
Button(win , text="show all books", command=showBOOKS).pack()

txtBox = Text(win , height=15 , width=50)
txtBox.pack()

win.mainloop()