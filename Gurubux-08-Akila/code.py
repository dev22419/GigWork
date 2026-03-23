from tkinter import *

main = Tk()
main.title("tracker")

cur_user = ""    # store current user maybe used later idk

# first screen (login part)
frame = Frame(main)
frame.pack()   # showing frame

Label(frame , text = "Username").pack()   # user name input
e1=Entry(frame)   # entry box 1
e1.pack()

Label(frame,text="Password").pack()  # password field 
e2 = Entry(frame)   # entry box 2
e2.pack()

msgLabel = Label(frame , text = "")   # for showing msg like error
msgLabel.pack()


# second screen (data input stuff)
frameB=Frame(main)   # another frame

Label(frameB,text="Activity").pack()   # what activity
entryA = Entry(frameB)   # activity name
entryA.pack()

Label(frameB , text="Time").pack()   # time taken maybe
entryB=Entry(frameB)
entryB.pack()

Label(frameB,text="Level").pack()   # intensity level i think
entryC = Entry(frameB)
entryC.pack()

out = Text(frameB ,height=15,width=50)   # output box
out.pack()


# login func (simple check not very safe)
def loginFunc( ):
 global cur_user   # using global bcz easy

 u = e1.get()   # get username
 p = e2.get()   # get password

 # try opening file
 try:
    file = open("user_store_data.txt","r")   # open file read mode
    data = file.read()   # read all data
    file.close()   # closing file important

    # checking user exist or not
    if u in data:   # if username found
        if p in data:   # also check password (not best way lol)
            cur_user = u   # set current user
            frame.pack_forget()   # hide first frame
            frameB.pack()   # show second frame
        else:
            msgLabel.config(text="wrong pass")   # wrong password
    else:
        msgLabel.config(text="no user")   # no user found

 except:
    msgLabel.config(text="error")   # some error


# register user (just appending file)
def registerFunc():
 u = e1.get()   # take username
 p = e2.get()   # take password

 # saving into file
 try:
    f=open("user_store_data.txt","a")   # append mode
    f.write(u+","+p+"\n")   # store data comma separated
    f.close()   # close file

    msgLabel.config(text="done")   # show success
 except:
    msgLabel.config(text="fail")   # if error


# save activity data
def saveFunc():

 a = entryA.get()   # activity
 b = entryB.get()   # time
 c = entryC.get()   # level

 # writing data to file
 try:
    f=open("store_data.txt","a")   # open file
    f.write(cur_user + ",DATA," + a + "," + b + "," + c + "\n")   # save line
    f.close()

    out.insert(END,"\nsaved data")   # show saved msg
 except:
    out.insert(END,"\nerror save")   # error msg


# view saved data
def viewFunc():

    out.delete(1.0, END)   # clear old data first (important)

    try:
        f = open("store_data.txt", "r")   # opening file
        data = f.read()   # read all content
        f.close()   # close file after read

        lines = data.split("\n")   # making list of lines

        # printing heading like table (manual)
        out.insert(END, "User\tActivity\tTime\tLevel\n")   # header
        out.insert(END, "--------------------------------------\n")   # line for design

        i = 0   # starting index
        while i < len(lines):   # loop all lines one by one

            line = lines[i]   # current line

            # check if current user present in line
            if cur_user in line and line != "":   # also avoid empty line

                parts = line.split(",")   # split by comma

                # expecting something like [user,DATA,a,b,c]
                if len(parts) >= 5:   # safety check

                    u = parts[0]   # username
                    a = parts[2]   # activity
                    b = parts[3]   # time
                    c = parts[4]   # level

                    # printing in column format using tab
                    out.insert(END, f"{u}\t{a}\t{b}\t{c}\n")   # print row

            i = i + 1   # increase loop counter

    except:
        out.insert(END, "no data found")   # if file missing or error


# buttons for actions
Button(frame,text="login",command=loginFunc).pack()   # login btn
Button(frame,text="register",command=registerFunc).pack()   # register btn

Button(frameB,text="save",command=saveFunc).pack()   # save btn
Button(frameB,text="view",command=viewFunc).pack()   # view btn


# start program
if __name__ == "__main__":
    main.mainloop()   # run app loop