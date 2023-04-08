import tkinter
import ConversionEngine

window = tkinter.Tk()
window.title("Currency Converter")
window.geometry("500x600")

#Chose info to display regarding how old the used data is
def InfoAge():
    ddat = ConversionEngine.ReturnAge(ConversionEngine.GetData()[1])
    if ddat == 0:
        return "Data being used is less than 15 minutes old."
    elif ddat == 1:
        return "Data being used is less than 1 hour old."
    elif ddat == 2:
        return "Data being used is less than 1 day old."
    elif ddat == 3:
        return "Data being used is less than 1 week old."
    elif ddat == 4:
        return "Data being used is less than 1 month old."
    else:
        return "Data being used is over 1 month old."

#popup window in case user tries to refresh currency exchange rates
def PopUpMsg(msg):
    ppup = tkinter.Toplevel(window)
    ppup.title("Info regarding conversion rate update")
    ppup.geometry("400x200")
    def ClosePpup(event):
        ppup.destroy()
    messg = tkinter.Label(ppup, text = msg, font = ("Arial", 16))
    messg.place(x = (400 - messg.winfo_reqwidth()) * 0.5, y = 50)
    okb = tkinter.Button(ppup, text = "OK", font = ("Arial", 16), width = 10, height = 2)
    okb.place(x = (400 - okb.winfo_reqwidth()) * 0.5, y = 125)
    okb.bind("<Button-1>",ClosePpup)

#Handle return from data update(succesfull/not)
def RefreshData(event):
    if ConversionEngine.QueryNewData() == 0:
        #failed to refresh
        PopUpMsg("Exchange rates could not be refreshed!")
    else:
        #refreshed succesfully
        PopUpMsg("Exchange rates refreshed succesfully!")
        agelabel.config(text = "Data has just been refreshed.")
        agelabel.place(x = (500 - agelabel.winfo_reqwidth()) * 0.5, y = 25)

def ExecuteConversion():
    if flist.curselection() == () or tlist.curselection() == ():
        #Case at least one of the two currencies necessary is not selected
        PopUpMsg("Choose the currencies to be converted!")
        return 0
    else:
        cfrm = ConversionEngine.PossibleCurrencies(["CHF", "EUR", "USD"])[flist.curselection()[0]]
        cto = ConversionEngine.PossibleCurrencies(["CHF", "EUR", "USD"])[tlist.curselection()[0]]
        try:
            val = float(txtbx.get("1.0", "end"))
        except:
            #Case nonnumeric value was entered into the textbox
            PopUpMsg("Please insert a number!")
            return 0
        else:
            return round(ConversionEngine.PerformConversion(ConversionEngine.GetData()[0],cfrm,cto,val),4)

def ConvertPressed(event):
    outputlbl.config(text = ExecuteConversion())
    outputlbl.place(x = 450 - outputlbl.winfo_reqwidth(), y = 400)
    agelabel.config(text = InfoAge())
    agelabel.place(x = (500 - agelabel.winfo_reqwidth()) * 0.5, y = 25)

agelabel = tkinter.Label(window, text = InfoAge(), font = ("Arial", 18))
agelabel.place(x = (500 - agelabel.winfo_reqwidth()) * 0.5, y = 25)
rfrshbtn = tkinter.Button(window, text = "Refresh!", font = ("Arial", 18), width = 20, height = 2)
rfrshbtn.place(x = (500 - rfrshbtn.winfo_reqwidth()) * 0.5, y = 75)
rfrshbtn.bind("<Button-1>",RefreshData)

flist = tkinter.Listbox(window, font = ("Arial",16), height = 3, width = 4, selectmode = "single", exportselection = 0)
tlist = tkinter.Listbox(window, font = ("Arial",16), height = 3, width = 4, selectmode = "single", exportselection = 0)
supportedcurrencies = ConversionEngine.PossibleCurrencies(["CHF", "EUR", "USD"])
for eachitem in range(len(supportedcurrencies)):
    flist.insert(eachitem + 1, supportedcurrencies[eachitem])
    tlist.insert(eachitem + 1, supportedcurrencies[eachitem])


flabel = tkinter.Label(window, text = ("Choose how much of which currency to convert!"), font = ("Arial", 16))
flabel.place(x = (500 - flabel.winfo_reqwidth()) * 0.5, y = 175)
flist.place(x = 50, y = 225)
tlabel = tkinter.Label(window, text = ("Choose which currency to convert to!"), font = ("Arial", 16))
tlabel.place(x = (500 - tlabel.winfo_reqwidth()) * 0.5, y = 325)
tlist.place(x = 50, y = 375)

cnvrtbtn = tkinter.Button(window, text = "Convert!", font = ("Arial", 20), width = 28, height = 2)
cnvrtbtn.place(x = (500 - cnvrtbtn.winfo_reqwidth()) * 0.5, y = 475)
cnvrtbtn.bind("<Button-1>", ConvertPressed)

txtbx = tkinter.Text(window, height = 1, width = 15, font = ("Arial",18))
txtbx.place(x = 450 - txtbx.winfo_reqwidth(), y = 250)

outputlbl = tkinter.Label(window, text = "0", font = ("Arial",18))
outputlbl.place(x = 450 - outputlbl.winfo_reqwidth(), y = 400)


window.mainloop()

