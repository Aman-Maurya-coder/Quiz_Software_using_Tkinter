import random
import mysql.connector as ms
import main
from tkinter import *
import tkinter.messagebox as msg
import csv
from main import username,password,path
from matplotlib.figure import Figure
import json
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#("#222831", '#00ADB5', '#EEEEEE', '#395B64')
# ("#1E1E2C", "#29283D", "#E7F6F2", "#395B64")      #2nd color theme.


background="#222831"
foreground="#00ADB5"
Button_Colour="#EEEEEE"
Notification="#395B64"

head_font="Castellar"
head_font_size=20
head_colour="black"

button_font="Anurati"
button_font_size=16
button_font_colour="black"
button_width=14

notify_font="Consolas"
notify_font_size=14
notify_font_colour="black"

entry_font="Pristina"
entry_font_size=24
entry_font_colour="black"

ques_font="Algerian"
ques_font_size=20

opt_font="Stencil"
opt_font_size=16

pad_heading_x,pad_heading_y=4,2
pad_option_x,pad_option_y=4,2

mar_heading_x,mar_heading_y=2,(4,6)
mar_button_x,mar_button_y=2,3
mar_entry_x,mar_entry_y=2,(10,2)


def goto_page(win,page):
	win.destroy()
	page()

def plot_window(win):
        win.destroy()
        plot=Tk()
        plot.title("Graph")
        plot.geometry("600x400")
        plot.minsize(600,400)
        plot.maxsize(600,400)
        plot.configure(background=background)
        Label(plot,text="Graph",font=f"{notify_font} {notify_font_size}",foreground=notify_font_colour,padx=pad_heading_x,pady=pad_heading_y,borderwidth=10,relief=RIDGE,background=Notification).pack(padx=mar_heading_x,pady=mar_heading_y)
        fig = Figure(figsize = (5, 5),dpi = 100)
        y = [i**2 for i in range(101)]
        con=ms.connect(host="localhost",user=username,passwd=password,db="quiz")
        cr=con.cursor()
        cr.execute(f"select history from player where player_name=\'{user}\'")
        his_lis=[]
        for a in cr:
                his_lis=json.loads(a[0])
        plot1 = fig.add_subplot(111)
        plot1.plot(his_lis)
        canvas = FigureCanvasTkAgg(fig,master = plot)
        canvas.draw()
        canvas.get_tk_widget().pack()
        plot.mainloop()

def final_window():
	game.destroy()
	main.update_score(user,score)
	global final
	final=Tk()
	final.title("Results")
	final.geometry("600x400")
	final.minsize(600,400)
	final.maxsize(600,400)
	final.configure(background=background)
	Label(final,text="Your Score:",font=f"{notify_font} {notify_font_size}",foreground=notify_font_colour,padx=pad_heading_x,pady=pad_heading_y,borderwidth=10,relief=RIDGE,background=Notification).pack(padx=mar_heading_x,pady=mar_heading_y)
	Label(final,text=score,font="Times 20",background=foreground,foreground=head_colour,padx=pad_heading_x,pady=pad_heading_y,width=7).pack(padx=mar_heading_x,pady=mar_heading_y)
	Button(final,text="Home Page",command=lambda:goto_page(final,main_window),font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour).pack(padx=mar_heading_x,pady=mar_heading_y)
	Button(final,text="Retry",command=lambda:goto_page(final,start_window),font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour).pack(padx=mar_heading_x,pady=mar_heading_y)
	Button(final,text="Graph of last 10 games".title(),command=lambda:plot_window(final),font=f"{button_font} {button_font_size}",background=Button_Colour,width=20,foreground=button_font_colour).pack(padx=mar_heading_x,pady=mar_heading_y)
	final.mainloop()

def checker(player_ans,question,options,answer):
    global ques_no,score,correct_answer
    player_answer=player_ans.get()
    if player_answer == correct_answer:
        score+=1
        print('correct')
    elif player_answer != correct_answer:
        print(player_answer)
        print(correct_answer)
        print('incorrect')
    changer(question,options,answer)

def changer(question,options,answer):
    global player_ans,lbl,opt1,opt2,opt3,opt4,next,back,score,ques_no
    
    if ques_no<10:
        option=options[lis[ques_no]]
    
        global correct_answer
        correct_answer=answer[lis[ques_no]]
        # print(ques_no)
        # if len(question[lis[ques_no]])>20:
        #     lbl.config(text=str(ques_no+1)+": "+question[lis[ques_no]],font=f"{ques_font} 10",background=foreground)
        #     opt1.config(text=option[0],value=option[0],width=40,font=f"{opt_font} 8",background=foreground)
        #     opt2.config(text=option[1],value=option[1],width=40,font=f"{opt_font} 8",background=foreground)
        #     opt3.config(text=option[2],value=option[2],width=40,font=f"{opt_font} 8",background=foreground)
        #     opt4.config(text=option[3],value=option[3],width=40,font=f"{opt_font} 8",background=foreground)
        # else:
        lbl.config(text=str(ques_no+1)+": "+question[lis[ques_no]],background=foreground)
        opt1.config(text=option[0],width=40,value=option[0],background=foreground)
        opt2.config(text=option[1],width=40,value=option[1],background=foreground)
        opt3.config(text=option[2],width=40,value=option[2],background=foreground)
        opt4.config(text=option[3],width=40,value=option[3],background=foreground)
        ques_no+=1
        # checker(player_ans,question,options,answer)
        next.config(text="Save & Next",command=lambda:checker(player_ans,question,options,answer),background=Button_Colour)
        back.config(text="Exit",command=lambda:goto_page(game,start_window),background=Button_Colour)
    else:
        final_window()


def game_window(info):
    data=False
    data_lis=[]
    with open(path,"r") as f:
            rdr=csv.reader(f)
            for a in rdr:
                data_lis.append(a)
            if len(data_lis)!=0:
                data=True
    if data==False:
            info.config(text="Please Connect To Internet first. Application needs to access data from web.\n You can play offline after playing once online.\nAfter connecting to the internet click start button again. ".title(),background=Notification)
            main.store_data()
    elif data==True:
            info.config(text="",background=background)
            a=msg.askquestion("Start Game","Are you Ready ?")
            if a=="yes":
                    global lis,player_ans,correct_answer,lbl,opt1,opt2,opt3,opt4,next,back
                    global score,game
                    score=0
                    global ques_no
                    ques_no=0
                    start.destroy()
                    game=Tk()
                    game.title("Quiz game")
                    game.geometry("750x500")
                    game.configure(background=background)
                    global lis
                    lis=[]
                    for a in range(10):
                        while 1:
                            no=random.randint(0,9)
                            if no not in lis:
                                lis.append(no)
                                break
                            else:
                                continue
                    serial,question,options,answer=main.read_data()
                    player_ans=StringVar()
                    player_ans.set("Radio")
                    lbl=Label(game,text="",background=background,justify=CENTER,wraplength=550,font=f"{ques_font} {ques_font_size}")
                    lbl.pack(pady=10,fill=X)
                    opt1=Radiobutton(game,text="",foreground=background,value="",variable=player_ans,justify=CENTER,font=f"{opt_font} {opt_font_size}",padx=pad_option_x,pady=pad_option_y,
                    width=20,wraplength=200,background=Notification)
                    opt2=Radiobutton(game,text="",foreground=background,value="",variable=player_ans,justify=CENTER,font=f"{opt_font} {opt_font_size}",padx=pad_option_x,pady=pad_option_y,
                    width=20,wraplength=200,background=Notification)
                    opt3=Radiobutton(game,text="",foreground=background,value="",variable=player_ans,justify=CENTER,font=f"{opt_font} {opt_font_size}",padx=pad_option_x,pady=pad_option_y,
                    width=20,wraplength=200,background=Notification)
                    opt4=Radiobutton(game,text="",foreground=background,value="",variable=player_ans,justify=CENTER,font=f"{opt_font} {opt_font_size}",padx=pad_option_x,pady=pad_option_y,
                    width=20,wraplength=200,background=Notification)
                    opt1.pack(padx=mar_heading_x,pady=mar_heading_y)
                    opt2.pack(padx=mar_heading_x,pady=mar_heading_y)
                    opt3.pack(padx=mar_heading_x,pady=mar_heading_y)
                    opt4.pack(padx=mar_heading_x,pady=mar_heading_y)
                    next=Button(game,text="",justify=CENTER,font=f"{button_font} {button_font_size}",background=background,width=button_width,foreground=button_font_colour)
                    back=Button(game,text="",justify=CENTER,font=f"{button_font} {button_font_size}",background=background,width=button_width,foreground=button_font_colour)
                    next.pack(padx=mar_heading_x,pady=mar_heading_y,side=RIGHT)
                    back.pack(padx=mar_heading_x,pady=mar_heading_y,side=LEFT)
                    changer(question,options,answer)
                    game.mainloop()
    
def delete_player():
    a=msg.askquestion("Deleting the user","Do you want to delete the user?")
    if a=="yes":
        con=ms.connect(host="localhost",user=username,passwd=password,db="quiz")
        cr=con.cursor()
        cr.execute(f"delete from player where player_name=\'{user}\'")
        con.commit()
        con.close()
        start.destroy()
        main_window()
        
def player_score(info):
        scr=main.player_highest(user)
        info.config(text=f"Your Score Is {scr}",background=Notification)

def start_window():
    global start
    start=Tk()
    start.geometry("600x400")
    start.title("Start Page")
    start.configure(bg=background)
    Label(start,text="Quiz Game",background=foreground,foreground=head_colour,padx=pad_heading_x,pady=pad_heading_y,borderwidth=10,relief=RIDGE,font=f"{head_font} {head_font_size}").pack(padx=mar_heading_x,pady=mar_heading_y)
    Button(start,text="Start",font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour,command=lambda:game_window(info)).pack(padx=mar_button_x,pady=mar_button_y)
    Button(start,text='Delete Player',font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour,command=delete_player).pack(padx=mar_button_x,pady=mar_button_y)
    Button(start,text='Personal Highest',font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour,command=lambda:player_score(info)).pack(padx=mar_button_x,pady=mar_button_y)
    Button(start,text='Graph',font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour,command=lambda:plot_window(start)).pack(padx=mar_button_x,pady=mar_button_y)
    Button(start,text='Home',font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour,command=lambda:goto_page(start,main_window)).pack(padx=mar_button_x,pady=mar_button_y)
    info=Label(start,font=f"{notify_font} {notify_font_size}",background=background,foreground=head_colour)
    info.pack()
    Label(start,text="-:Rules:-\n(1):-There are total of 10 questions\n(2):-All questions are mcq type",background="black",foreground="white",font="Times 8",pady=20).pack(fill=X,side=BOTTOM)
    start.mainloop()

def sign(usr,warn):
    global user
    user=usr.get()
    con=ms.connect(host="localhost",user=username,passwd=password,db="quiz")
    cr=con.cursor()
    cr.execute("select * from player")
    ch=False
    score=0
    his=[]
    for a in cr:
        if a[0]==user.lower():
            ch=True
            break
    if ch==True:
        warn.config(text="User Already Exits Please Use Diffrent Username",background=Notification)
        con.close()
    else:
        cr.execute(f"insert into player values(\'{user}\',{score},\'{his}\')")
        con.commit()           
        con.close()
        signup.destroy()
        start_window()

def login(usr,warn):
    global user
    user=usr.get()
    con=ms.connect(host="localhost",user=username,passwd=password,db="quiz")
    cr=con.cursor()
    cr.execute("select * from player")
    ch=False
    for a in cr:
        if a[0]==user:
            ch=True
            break
    if ch==True:
        newWindow.destroy()
        start_window()
    else:
        warn.config(text="User Not Exist",background=Notification)
        
        
def signup_window():
    root.destroy()
    global signup
    signup=Tk()
    signup.title("Signup Form")
    signup.geometry("600x400")
    signup.maxsize(600,400)
    signup.minsize(600,400)
    signup.configure(bg=background)
    usr=StringVar()
    Label(signup,text="Sign Up",font=f"{head_font} {head_font_size}",padx=pad_heading_x,pady=pad_heading_y,borderwidth=10,relief=RIDGE,background=foreground,foreground=head_colour).pack(padx=mar_heading_x,pady=mar_heading_y)
    Label(signup,text="Enter Player Name",padx=pad_heading_x,pady=pad_heading_y,borderwidth=10,relief=RIDGE,background=foreground,foreground=head_colour,font=f"{head_font} {head_font_size}").pack(padx=mar_heading_x,pady=mar_heading_y)
    entr=Entry(signup,textvariable=usr,font=f"{entry_font} {entry_font_size}",foreground=entry_font_colour)
    entr.focus_set()
    entr.pack(padx=mar_entry_x,pady=mar_entry_y)
    Button(signup,text="Sign Up",font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour,command=lambda:sign(usr,warn)).pack(padx=mar_button_x,pady=mar_button_y)
    Button(signup,text='Home',font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour,command=lambda:goto_page(signup,main_window)).pack(padx=mar_button_x,pady=mar_button_y)
    warn=Label(signup,background=background,font=f"{notify_font} {notify_font_size}",foreground=notify_font_colour)
    warn.pack()
    signup.mainloop()
    
def login_window():
    root.destroy()
    global newWindow,user
    newWindow=Tk()
    newWindow.title("Login Form")
    newWindow.geometry("600x400")
    newWindow.configure(bg=background)
    usr=StringVar()
    Label(newWindow,text="Login Form",padx=pad_heading_x,pady=pad_heading_y,borderwidth=10,relief=RIDGE,background=foreground,foreground=head_colour,font=f"{head_font} {head_font_size}").pack(padx=mar_heading_x,pady=mar_heading_y)
    Label(newWindow,text="Enter Player Name",background=foreground,padx=pad_heading_x,pady=pad_heading_y,foreground=head_colour,borderwidth=10,relief=RIDGE,font=f"{head_font} {head_font_size}").pack(padx=mar_heading_x,pady=mar_heading_y)
    entr = Entry(newWindow,textvariable=usr,font=f"{entry_font} {entry_font_size}",foreground=entry_font_colour)
    entr.focus_set()
    entr.pack(padx=mar_entry_x,pady=mar_entry_y)
    Button(newWindow,text="Login",font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour,command=lambda:login(usr,warn)).pack(padx=mar_button_x,pady=mar_button_y)
    Button(newWindow,text='Home',font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour,command=lambda:goto_page(newWindow,main_window)).pack(padx=mar_button_x,pady=mar_button_y)
    warn=Label(newWindow,background=background,font=f"{notify_font} {notify_font_size}",foreground=notify_font_colour)
    warn.pack()
    newWindow.mainloop()
    
def highest_score(high):
	scr=main.highest_score()
	high.config(text=f"The Highest Score In The Game Is {scr[1]} Of {scr[0].title()}",background=Notification)

def main_window():
	main.store_data()
	global root
	root=Tk()
	root.geometry("600x400")
	root.maxsize(600,400)
	root.minsize(600,400)
	root.title("Quiz Game")
	root.configure(bg=background)
	Label(text="Welcome To Quiz Game",padx=pad_heading_x,pady=pad_heading_y,borderwidth=10,relief=RIDGE,background=foreground,foreground=head_colour,font=f"{head_font} {head_font_size}").pack(padx=mar_heading_x,pady=mar_heading_y)
	Button(root,text="Login",font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour, command=login_window).pack(padx=mar_button_x,pady=mar_button_y)
	Button(root,text="Sign Up",font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour,command=signup_window).pack(padx=mar_button_x,pady=mar_button_y)
	Button(root,text="Highest Score",font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour,command=lambda:highest_score(high)).pack(padx=mar_button_x,pady=mar_button_y)
	Button(root,text="Close",font=f"{button_font} {button_font_size}",background=Button_Colour,width=button_width,foreground=button_font_colour,command=root.destroy).pack(padx=mar_button_x,pady=mar_button_y)
	high=Label(root,background=background,font=f"{notify_font} {notify_font_size}",foreground=notify_font_colour)
	high.pack()
	root.mainloop()
main_window()
#user='aman'
#score=4
#final_window()
