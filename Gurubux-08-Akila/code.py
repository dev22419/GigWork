from tkinter import *

main = Tk()
main.title("tracker while style")

CU = ""

# UI first (functions later)
fA = Frame(main)
fA.pack()

eU = Entry(fA)
eU.pack()

eP = Entry(fA)
eP.pack()

msg = Label(fA,text="")
msg.pack()

fB = Frame(main)

t1 = Entry(fB)
t2 = Entry(fB)
t3 = Entry(fB)

t1.pack()
t2.pack()
t3.pack()

outB = Text(fB,height=15,width=50)
outB.pack()


# functions below (late defined)

def goLogin():

 global CU
 u = eU.get().strip()
 p = eP.get().strip()

 try:
  f = open("users.txt","r")
  d = f.read().strip()
  f.close()

  if u in d and p in d:
    CU = u
    fA.pack_forget()
    fB.pack()
 except:
  msg.config(text="err")


def goSave():

 a = t1.get().strip()
 b = t2.get().strip()
 c = t3.get().strip()

 f = open("data.txt","a")
 f.write(CU + ",DATA," + a + "," + b + "," + c + "\n")
 f.close()

 outB.insert(END,"\nsaved")


def goView():

 outB.delete(1.0,END)

 try:
  f = open("data.txt","r")
  d = f.read().strip()
  f.close()

  lines = d.split("\n")

  i = 0
  while i < len(lines):

    if CU in lines[i]:
        outB.insert(END,lines[i] + "\n")

    i = i + 1

 except:
  outB.insert(END,"none")


Button(fA,text="login",command=goLogin).pack()
Button(fB,text="save",command=goSave).pack()
Button(fB,text="view",command=goView).pack()

if __name__ == "__main__":
    main.mainloop()
