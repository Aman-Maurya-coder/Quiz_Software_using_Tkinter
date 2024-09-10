import requests
from bs4 import BeautifulSoup
import csv
import random
import time
import mysql.connector as ms
import json
from dotenv import load_dotenv
import os
url = "https://www.gktoday.in/quizbase/computer-awareness-for-ibps-banking-examinations"
path='ques.csv'
load_dotenv()
username=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
db_name=os.getenv("DB_NAME")
def get_data(url):
    try:
        # Step 1 = get the html
        # gets the content of the website in plain text
        r = requests.get(url)
        # getting the html content of the website
        htmlContent = r.content
        # Step 2 = parse the HTML
        soup = BeautifulSoup(htmlContent, "html.parser")
        return soup
    except:
        return 0

def get_ques():
    soup=get_data(url)
    if soup==0:
        return 0
    else:
        ques=soup.findAll('div', class_='wp_quiz_question testclass')
        ques_lis=[]
        for a in ques:
            txt=a.get_text()
            ques_txt=""
            for a in txt:
                if a.isalpha() or a.isspace():
                    ques_txt+=a
            ques_lis.append(ques_txt.strip())
        return ques_lis

def get_options():
    soup=get_data(url)
    if soup==0:
        return 0
    else:
        sp=soup.findAll("div",class_='wp_quiz_question_options')
        options=[]
        for a in sp:
            sp2=a.findAll("p")
            d=str(list(sp2)[0])
            st=d[4:-4].split("<br/>")
            lis=[]
            for a in st:
                txt=a.split()[1:]
                lis.append(" ".join(txt))
            options.append(lis)
        return options

def get_ans():
    soup=get_data(url)
    if soup==0:
        return 0
    else:
        ans=soup.findAll("div",class_='ques_answer')
        ans_lis=[]
        for a in ans:
            txt=str(a.get_text())
            answer=txt.split()[3:]
            ans_lis.append(" ".join(answer))
        return ans_lis

def store_data():
    ques_lis=get_ques()
    option_lis=get_options()
    ans_lis=get_ans()
    if ques_lis==0 and option_lis==0 and ans_lis==0:
        data_lis=[]
        with open(path,"r") as f:
            rdr=csv.reader(f)
            for a in rdr:
                data_lis.append(a)
        if len(data_lis)==0:
            print("please connect to the internet once. It is necessary to fetch the data for quiz. After playing once you can also play it offline")
        else:
            return
    else:
            with open(path,"w",newline="") as f:
                wrtr=csv.writer(f)
                for a in range(len(ques_lis)):
                    wrtr.writerow([a+1,ques_lis[a],option_lis[a],ans_lis[a][1:-1]])
            return

def read_data():
    serial=[a for a in range(1,11)]
    ques_lis=[]
    option_lis=[]
    ans_lis=[]
    with open(path,"r") as f:
        rdr=csv.reader(f,delimiter=",")
        for a in rdr:
            ques_lis.append(a[1])
            option_lis.append(eval(a[2]))
            ans_lis.append(a[3])
    return serial,ques_lis,option_lis,ans_lis

def db():
    con=ms.connect(host="localhost",user=username,passwd=password)
    cr=con.cursor()
    cr.execute("show databases")
    ch=True
    for a in cr:
        if a[0]==db_name:
            ch=True
            break
        else:
            ch=False
    if ch==True:
        for a in cr:
            pass
        cr.execute(f"use {db_name}")
    else:
        cr.execute(f"create database {db_name}")
        cr.execute(f"use {db_name}")
    try:
        cr.execute("create table player(player_name varchar(22) primary key,highest_score int, history varchar(20))")
    except:
        cr.execute("desc player")
        ch=True
        field_list=[]
        for a in cr:
            field_list.append(a)
        if field_list==["player_name","highest_score","history"]:
            pass
        else:
            cr.execute("drop table player")
            cr.execute("create table player(player_name varchar(22) primary key,highest_score int,history varchar(20))")
    con.commit()
    con.close()

def update_score(user,score):
    con=ms.connect(host="localhost",user=username,passwd=password,db=db_name)
    cr=con.cursor()
    cr.execute("select * from player")
    prev_score=0
    his=[]
    for a in cr:
        if a[0]==user:
            prev_score=a[1]
            his=json.loads(a[2])
    if len(his)==10:
        his=his[1:]
        his.append(score)
    else:
        his.append(score)
    his=json.dumps(his)
    if prev_score<score:
        cr.execute(f"update player set highest_score={score} where player_name=\'{user}\'")
        cr.execute(f"update player set history=\'{his}\' where player_name=\'{user}\'")
    else:
        cr.execute(f"update player set history=\'{his}\' where player_name=\'{user}\'")
    con.commit()
    con.close()

def show_score(user):
    con=ms.connect(host="localhost",user=username,passwd=password,db=db_name)
    cr=con.cursor()
    cr.execute("select * from player")
    for a in cr:
        if a[1]==user:
            print(a[2])
    con.commit()
    con.close()

def sign_up():
    user=input("enter player name(type close to exit):-")
    if user=="close":
        return None
    score=0
    his=[]
    con=ms.connect(host="localhost",user=username,passwd=password,db=db_name)
    cr=con.cursor()
    cr.execute("select * from player")
    data=cr.fetchall()
    if len(data)==0:
        cr.execute(f"insert into player values(\'{user}\',{score},\'{his}\')")
        con.commit()
        con.close()
        return user
    else:
        ch=False
        for a in data:
            if a[0]==user:
                ch=True
                break
        if ch==True:
            print("User already exists.")
            sign_up()
        else:
            cr.execute(f"insert into player values(\'{user}\',{score},\"{his}\")")
        con.commit()
        con.close()
        return user

def login():
    user=input("enter user name:-")
    con=ms.connect(host="localhost",user=username,passwd=password,db=db_name)
    cr=con.cursor()
    cr.execute("select * from player")
    ch=False
    for a in cr:
        if a[0]==user:
            ch=True
            break
    if ch==True:
        print("logged in ...")
        return user
    else:
        print("No user with this name, sign up please")
        return None

def chk_score(user):
    con=ms.connect(host="localhost",user=username,passwd=password,db=db_name)
    cr=con.cursor()
    cr.execute(f"select highest_score from player where player_name=\'{user}\'")
    for a in cr:
        return a[0]

def highest_score():
    con=ms.connect(host="localhost",user=username,passwd=password,db=db_name)
    cr=con.cursor()
    cr.execute("select * from player where highest_score in (select max(highest_score) from player)")
    for a in cr:
        return a

def player_highest(user):
    con=ms.connect(host="localhost",user=username,passwd=password,db=db_name)
    cr=con.cursor()
    cr.execute(f"select highest_score from player where player_name=\'{user}\'")
    for a in cr:
        return a[0]


def game(user):
    score=0
    print("Welcome to the game")
    while 1:
        try:
            inpt=int(input("(1):-start the game\n(2):-rules\n(3):-check your highest score\n(4):-back\n-->"))
        except ValueError:
            print("Please enter a number from above options.")
        else:
            if inpt==4:
                return None
            elif inpt==3:
                print(player_highest(user),"is your highest score")
                continue
            elif inpt==1:
                print("are you ready to play:-")
                while 1:
                    try:
                        inp=int(input("(1):-yes\n(2):-no\n-->"))
                        break
                    except ValueError:
                        print("Please enter a number from above options.")
                if inp==2:
                    break
                elif inp==1:
                    print("STARTNG IN")
                    for a in range(1,4):
                        print(a)
                        time.sleep(1)
                    print("\n")
            elif inpt==2:
                print("-:Rules for the game:-")
                print("...")
                continue
            else:
                print("Please enter from given options only.")
                continue
            if inp==2:
                pass
            elif inp==1:
                break
    serial,question,options,answer=read_data()
    for a in range(10):
        while 1:
            no=random.randint(1,10)
            if no not in serial:
                continue
            else:
                break
        serial.remove(no)
        option=options[no-1]
        answr=answer[no-1]
        print(a+1,":-",question[no-1]+":-")
        for a in range(1,5):
            print(a,option[a-1])
        while 1:
            try:
                ans=int(input("enter your answer:-"))
                if ans in [1,2,3,4]:
                    if option[ans-1]==answr:
                        print("you are correct")
                        score+=1
                        print("\n")
                        print("total score:"+str(score))
                        print("\n")
                        break
                    elif option[ans-1]!=answr:
                        print("\n")
                        print("you are wrong")
                        print("\n")
                        break
                else:
                    print("please enter from the options.")
            except ValueError:
                print("enter a number please.")
        time.sleep(1)
    return score

def main():
    print("-:Welcome To Quiz Game:-")
    print("Select from the given options:-")
    while 1:
        try:
            inpt=int(input("(1):-Login:-\n(2):-Sign Up\n(3):-Show highest scorer\n(4):-close\n-->"))
        except ValueError:
            print("Please enter a number from above options.")
        else:
            if inpt==4:
                print("Thank you for playing...")
                return None
            elif inpt==1:
                user=login()
                if user==None:
                    pass
                else:
                    break
            elif inpt==2:
                user=sign_up()
                if user==None:
                    pass
                else:
                    break
            elif inpt==3:
                print(highest_score())
                pass
            else:
                print("Please enter from given options only.")
    t_score=game(user)
    if t_score==None:
        main()
        return None
    elif t_score>chk_score(user):
        print("Congratulations! It's your new highest score.")
    while 1:
        update_score(user,t_score)
        print("Would you like to play again:-")
        try:
            inp=int(input("(1):-yes\n(2):-no\n(3)exit the game\n-->"))
        except ValueError:
            print("Please enter a number from above options.")
        if inp==2:
            main()
            return
        elif inp==1:
            t_score=game(user)
        elif inp==3:
            break
    print("Thank you for playing...")
if __name__=="__main__":
    store_data()
    # db()
    # main()
    # update_score("aman", 11)
