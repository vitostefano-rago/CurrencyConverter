import requests
import json
import datetime

#This handles the access to the api with link and credentials
def HandleAccess():
    try:
        with open("accessdata.txt", "r") as apiaccess:
            ad = apiaccess.readlines()
            myurl = ad[1]
            myid = ad[3]
            return myurl, myid
    except:
        return 0, 0

#This refreshes the json file that is currently being used
#Negative response from server or corrupted access data is also handled. 
def QueryNewData():
    myurl, myid = HandleAccess()
    try:
        response = requests.get(myurl, headers = {"apikey" : myid})
        if response.status_code == 200:
            myjs = response.json()
            with open("exchangerates.json", "w") as ecr:
                json.dump(myjs,ecr)
            return 1
        else:
            return 0
    except:
        return 0

#This retrieves the data from the saved json file
def GetData():
    with open("exchangerates.json","r") as myfile:
        contnt = json.load(myfile)
        mydict = dict(contnt)
        dta = mydict["rates"]
        dta[mydict["base"]] = 1
        tstmp = mydict["timestamp"]
        return dta, tstmp

#This returns how old the data we are about to use is
def ReturnAge(rt):
    cm = datetime.datetime.timestamp(datetime.datetime.now())
    dt = cm - rt
    if dt < 900:
        #Case of less than 15 minutes old data
        return 0
    elif dt < 3600:
        #Case of less than 1 hour old data
        return 1
    elif dt < 86400:
        #Data less than a day old
        return 2
    elif dt < 604800:
        #Data less than a week old
        return 3
    elif dt < 2592000:
        #Data less than a month old
        return 4
    else:
        #Older than a month data, undifferentiated
        return 5

#Inputs: dictionary containing the rates, string of current currency (currency from), string of new currency (currency to), amount
def PerformConversion(rd, cf, ct, am):
    #The conversion factor is the convert to convert from ratio in the dictionary
    fac = rd[ct] / rd[cf]
    #Value in the new currency is factor multiplied the value in the old currency
    nv = am * fac
    return nv

#Returns the possible currencies. The currencies considered to be more frequently used can be taken to the top. Otherwise, alphabetical order is used.
def PossibleCurrencies(viplist):
    mylst = list(GetData()[0].keys())
    retlst = []
    for currency in viplist:
        mylst.remove(currency)
        retlst.append(currency)
    mylst.sort()
    retlst.extend(mylst)
    return retlst