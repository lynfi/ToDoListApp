#!/usr/bin/env python
import numpy as np
import tkinter
import datetime
from os import path
# Load data

if (path.exists('./db.npz')):
    data = np.load('./db.npz', allow_pickle=True)
    dic = data['dic'].tolist()
    money = data['money']
else:
    dic = []
    money = 0
    np.savez('./db.npz', dic=dic, money=money)


# insert a new item into our table
def newItem():
    global money
    global dic
    # get current time
    date_time = datetime.datetime.now()
    date = date_time.date()  # gives sdate
    time = date_time.time()  # gives times
    print(time)
    if ((not date in dic) and time <= datetime.time(8, 30)):
        print(time)
        dic.append(date)
        money += 5
        if time <= datetime.time(8, 0):
            money += 10
        check = True
        # add $100 if wake up before 8am for 7 days in a row
        for i in range(1, 7):
            pastDate = date - datetime.timedelta(days=i)
            if (not pastDate in dic):
                check = False
                break
        if check:
            money += 100
    np.savez('db.npz', dic=dic, money=money)


def useItem(item):
    global money
    money -= item
    np.savez('db.npz', dic=dic, money=money)


class Todo(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("WakeUp")

        self.todoList = tkinter.Listbox()
        self.todoList.pack(fill=tkinter.BOTH, expand=0)

        entryButton = tkinter.Button(text="Wake up before 8am",
                                     command=self.addToList)
        entryButton.pack(fill=tkinter.BOTH, expand=0)

        # Use money
        self.Money = tkinter.Entry()
        self.Money.pack(fill=tkinter.BOTH, expand=0)

        useButton = tkinter.Button(text="Use money", command=self.useMoney)
        useButton.pack(fill=tkinter.BOTH, expand=0)

        # update the application on startup with items already
        # in the database
        self.refreshList()

    def refreshList(self):
        self.todoList.insert(tkinter.END, "money: " + str(money))
        self.todoList.update_idletasks()
        l = min(len(dic), 7)
        for i in range(l):
            date = dic[l - 1 - i]
            curTime = str(date.day) + '/' + str(date.month) + '/' + str(
                date.year)
            item = curTime + " Succeed!"
            self.todoList.insert(tkinter.END, str(item))
            self.todoList.update_idletasks()

    def addToList(self):
        # add an item to the database
        newItem()
        # delete all entries in the list todoList
        self.todoList.delete(0, tkinter.END)
        # update the list
        self.todoList.update_idletasks()
        # get all the items back again, refreshing them all
        self.refreshList()
        # debugPrint()

    def useMoney(self):
        # deletes an item from the database
        useItem(int(self.Money.get()))
        # deletes everything from the list
        self.todoList.delete(0, tkinter.END)
        # update the list
        self.todoList.update_idletasks()
        # clear the deleteOption entry box
        self.Money.delete(0, 'end')
        # refresh the list by getting them all from the database
        self.refreshList()
        # debugPrint()


if __name__ == "__main__":
    application = Todo()
    application.mainloop()