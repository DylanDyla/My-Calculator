from string import whitespace
import tkinter as tk
import sqlite3 
import keyboard

window = tk.Tk()

operand = "" #stores the last number keyed in
displayNum = "" #stores the value to be displayed
con = sqlite3.connect("database.db")
cur = con.cursor()


def inputNumber(num):
    global displayNum
    global operand
    displayNum += str(num)
    operand += str(num)
    labelDisplay.configure(text=displayNum) #update label

def inputOperator(operator):
    global displayNum
    global operand
    strLen = len(displayNum)
    if strLen > 0:
        lastChar = displayNum[strLen -1]
        if lastChar == "+" or lastChar == "-" or lastChar == "*" or lastChar == "/":
            return
    
    displayNum += operator
    labelDisplay.configure(text=displayNum) #update label

def inputZero():
    global displayNum
    global operand
    strLen = len(displayNum)
    lastChar = displayNum[strLen-1]
    if strLen == 0:
        return
    elif lastChar == "+" or lastChar == "-" or lastChar == "*" or lastChar == "/":
        return 
    
    displayNum += "0"
    operand += "0"
    labelDisplay.configure(text=displayNum)

def inputDecimal():
    global displayNum
    global operand
    
    if "." in operand:
        return

    if len(operand) == 0:
        displayNum += "0"
    
    displayNum += "."
    operand += "."
    labelDisplay.configure(text=displayNum)

def calculateResult():
    global displayNum
    displayNum = str(eval(displayNum))
    labelDisplay.config(text=displayNum)

def inputDelete():
    global displayNum
    global operand
    strLen = len(displayNum)
    lastChar = displayNum[strLen -1]
    if strLen == 0:
        return
    else:
        displayNum = displayNum[0: strLen - 1]
        labelDisplay.config(text=displayNum)
    
def inputClear():
    global displayNum
    global operand
    displayNum = ""
    operand = ""
    labelDisplay.configure(text=displayNum)


def fetchValue():
    cur.execute("select * from calculator")
    rows = cur.fetchall()
    return rows


cur.execute("create table if not exists calculator(id integer primary key, display text)")
rows = fetchValue()
if len(rows) == 0:
    cur.execute("insert into calculator values(1,'')")
    con.commit()

def storeValue():
    global displayNum
    cur.execute("update calculator set display = ? where id = 1", (displayNum,))
    con.commit() 
    
def fetch():
    global displayNum

    rows = fetchValue()
    if len(rows) > 0:
        displayNum += rows[0][1] #[row][col], col 1 is display

    labelDisplay.configure(text=displayNum)







labelDisplay = tk.Label(
    height = 2,
    bg = "white",
    font = ("Helvetica", "20")
)
labelDisplay.grid(row=0, columnspan=5, sticky="ew", padx=5)


for i in range (0,3): # Rows
    window.columnconfigure(i, weight=1)
    window.rowconfigure(i, weight=1)

    for j in range (0,3): # Columns
        buttonDisplay = (3 * i + 1) + 1 * j
        bnNum = tk.Button(                     
            text = buttonDisplay,
            command = lambda buttonDisplay=buttonDisplay: inputNumber(buttonDisplay),
            height = 2,
            width = 2
        )
        bnNum.grid(row=i+1,column=j)

bnZero = tk.Button(
    text = "0",
    command = inputZero,
    height = 2,
    width = 2
)
bnZero.grid(row=4,column=0)

bnDecimal = tk.Button(
    text = ".",
    command = inputDecimal,
    height = 2,
    width = 2
)
bnDecimal.grid(row=4,column=1)

bnAddition = tk.Button(
    text = "+",
    command = lambda operator="+": inputOperator(operator),
    height = 2,
    width = 2
)
bnAddition.grid(row=1,column=3)

bnSubtractraction = tk.Button(
    text = "-",
    command = lambda operator="-": inputOperator(operator),
    height = 2,
    width = 2
)
bnSubtractraction.grid(row=1,column=4)

bnMultiplication = tk.Button(
    text = "x",
    command = lambda operator="*": inputOperator(operator),
    height = 2,
    width = 2
)
bnMultiplication.grid(row=2, column=3)

bnDivision = tk.Button(
    text = "÷",
    command = lambda operator="/":inputOperator(operator),
    height = 2,
    width = 2
)
bnDivision.grid(row=2,column=4)

bnEqual = tk.Button(
    text = "=",
    command = calculateResult,
    height = 2,
    width = 2 
)
bnEqual.grid(row=4,column=2)

bnDelete = tk.Button(
    text = "B",
    command = inputDelete,
    height = 2,
    width = 2
)
bnDelete.grid(row=4,column=3)

bnClear = tk.Button(
    text = "C",
    command = inputClear,
    height = 2,
    width = 2
)
bnClear.grid(row=4,column=4)

bnStore = tk.Button(
    text = "M+",
    command = storeValue,
    height = 2,
    width = 2
)
bnStore.grid(row=3,column=3)

bnFetch = tk.Button(
    text = "M",
    command = fetch,
    height = 2,
    width = 2
)
bnFetch.grid(row=3,column=4)

window.mainloop()