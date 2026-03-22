from tkinter import *

# window
appWin = Tk()
appWin.title("fit app no func")


curUser = ""

# login frame
f1 = Frame(appWin)
f1.pack()

Label(f1,text="user").pack()
uE = Entry(f1)
uE.pack()

Label(f1,text="pass").pack()
pE = Entry(f1)
pE.pack()

msg = Label(f1,text="")
msg.pack()

# menu frame
f2 = Frame(appWin)

# activity inputs
aE = Entry(f2)
dE = Entry(f2)
iE = Entry(f2)

# food inputs
fE = Entry(f2)
cE = Entry(f2)

out = Text(f2,height=15,width=50)


# login button logic inline
def btn1():
 global curUser
 u = uE.get().strip()
 p = pE.get().strip()

 try:
  f = open("users.txt","r")
  d = f.read().strip()
  f.close()

  if u in d and p in d:
    curUser = u
    f1.pack_forget()
    f2.pack()
  else:
    msg.config(text="wrong")
 except:
  msg.config(text="error")

Button(f1,text="login",command=btn1).pack()


# register inline
def btn2():
 u = uE.get().strip()
 p = pE.get().strip()

 f = open("users.txt","a")
 f.write(u + "," + p + "\n")
 f.close()

 msg.config(text="done")

Button(f1,text="reg",command=btn2).pack()


# menu layout
Label(f2,text="activity").pack()
aE.pack()
dE.pack()
iE.pack()

Label(f2,text="food").pack()
fE.pack()
cE.pack()

out.pack()


# save activity inline
def b3():
 a = aE.get().strip()
 d = dE.get().strip()
 i = iE.get().strip()

 f = open("data.txt","a")
 f.write(curUser + ",A," + a + "," + d + "," + i + "\n")
 f.close()

 out.insert(END,"\nsaved act")

Button(f2,text="save act",command=b3).pack()


# save food inline
def b4():
 f = open("data.txt","a")
 f.write(curUser + ",F," + fE.get().strip() + "," + cE.get().strip() + "\n")
 f.close()

 out.insert(END,"\nsaved food")

Button(f2,text="save food",command=b4).pack()


# view inline using for loop
def b5():
 out.delete(1.0,END)

 try:
  f = open("data.txt","r")
  lines = f.readlines()
  f.close()

  for line in lines:
    if curUser in line:
        out.insert(END,line)

 except:
  out.insert(END,"no file")

Button(f2,text="view",command=b5).pack()

appWin.mainloop()