#!/usr/bin/env python
import numpy as np
import tkinter
import datetime
from os import path
# Load data

if (path.exists('study_time_db.npz')):
    data = np.load('study_time_db.npz', allow_pickle=True)
    dic_date = data['date'].tolist()
    dic_time = data['time'].tolist()
    dic_day = data['day'].tolist()
    money = data['money']
else:
    dic_date = []
    dic_time = []
    dic_day = []
    money = 0
    np.savez('study_time_db.npz',
             date=dic_date,
             time=dic_time,
             day=dic_day,
             money=money)


# insert a new item into our table
def newItem(item):
    global money
    global dic_date, dic_time, dic_day
    # get current time
    date_time = datetime.datetime.now()
    date = date_time.date()  # gives sdate
    if not date in dic_date:
        dic_date.append(date)
        dic_time.append(item)
        if item >= 5:
            # add $10 if study more than 5 hours, $15 if more than 6 hours
            money += 10
            if item >= 6:
                money += 5
            check = True
            # add $100 if study more than 5 hours for 7 days in a row
            for i in range(1, 7):
                pastDate = date - datetime.timedelta(days=i)
                if (not pastDate in dic_day):
                    check = False
                    break
            if check:
                money += 100
                dic_day = []
            else:
                dic_day.append(date)
        else:
            dic_day = []

    np.savez('study_time_db.npz',
             date=dic_date,
             time=dic_time,
             day=dic_day,
             money=money)


def useItem(item):
    global money
    money -= item
    np.savez('study_time_db.npz',
             date=dic_date,
             time=dic_time,
             day=dic_day,
             money=money)


class Todo(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("WakeUp")

        self.todoList = tkinter.Listbox()
        self.todoList.pack(fill=tkinter.BOTH, expand=0)

        # add study time
        self.study_time = tkinter.Entry()
        self.study_time.pack(fill=tkinter.BOTH, expand=0)

        entryButton = tkinter.Button(text="Study Hours",
                                     command=self.addToList)
        entryButton.pack(fill=tkinter.BOTH, expand=0)

        # Use money
        self.Money = tkinter.Entry()
        self.Money.pack(fill=tkinter.BOTH, expand=0)

        useButton = tkinter.Button(text="Use money", command=self.useMoney)
        useButton.pack(fill=tkinter.BOTH, expand=0)

        self.refreshList()

    def refreshList(self):
        self.todoList.insert(tkinter.END, "money: " + str(money))
        self.todoList.update_idletasks()
        l = min(len(dic_date), 7)
        for i in range(l):
            date = dic_date[l - 1 - i]
            time = dic_time[l - 1 - i]
            curDate = str(date.day) + '/' + str(date.month) + '/' + str(
                date.year)
            curTime = str(time)
            item = curDate + " " + curTime + " Hours"
            self.todoList.insert(tkinter.END, str(item))
            self.todoList.update_idletasks()

    def addToList(self):
        # add today
        newItem(int(self.study_time.get()))
        # delete all entries in the list todoList
        self.todoList.delete(0, tkinter.END)
        # update the list
        self.todoList.update_idletasks()
        # get all the items back again, refreshing them all
        self.refreshList()

    def useMoney(self):
        # use money
        useItem(int(self.Money.get()))
        # deletes everything from the list
        self.todoList.delete(0, tkinter.END)
        # update the list
        self.todoList.update_idletasks()
        # clear the deleteOption entry box
        self.Money.delete(0, 'end')
        # refresh the list by getting them all from the database
        self.refreshList()


if __name__ == "__main__":
    application = Todo()
    application.mainloop()