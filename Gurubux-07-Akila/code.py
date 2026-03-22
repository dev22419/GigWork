from tkinter import *

win = Tk()
win.title("fitness mixed")

cur = ""

# function for login
def loginA():

 global cur
 u = uBox.get().strip()
 p = pBox.get().strip()

 try:
  f = open("u.txt","r")
  data = f.read().strip()
  f.close()

  if u in data and p in data:
    cur = u
    fr1.pack_forget()
    fr2.pack()
 except:
  pass


# UI
fr1 = Frame(win)
fr1.pack()

uBox = Entry(fr1)
uBox.pack()

pBox = Entry(fr1)
pBox.pack()

Button(fr1,text="login",command=loginA).pack()


# inline register (no function)
def regX():
 f = open("u.txt","a")
 f.write(uBox.get().strip() + "," + pBox.get().strip() + "\n")
 f.close()

Button(fr1,text="reg",command=regX).pack()


# menu
fr2 = Frame(win)

act = Entry(fr2)
dur = Entry(fr2)
cal = Entry(fr2)

act.pack()
dur.pack()
cal.pack()

txt = Text(fr2,height=15,width=50)
txt.pack()


# save using for loop dummy
def saveX():

 data = [act.get().strip(),dur.get().strip()]

 for i in data:
    pass   # useless loop beginner style

 f = open("d.txt","a")
 f.write(cur + ",X," + act.get().strip() + "," + dur.get().strip() + "\n")
 f.close()

 txt.insert(END,"\ndone")

Button(fr2,text="save",command=saveX).pack()


# view using for
def viewX():

 txt.delete(1.0,END)

 try:
  f = open("d.txt","r")
  lines = f.readlines()
  f.close()

  for x in lines:
    if cur in x:
        txt.insert(END,x)
 except:
  txt.insert(END,"error")

Button(fr2,text="view",command=viewX).pack()

win.mainloop()