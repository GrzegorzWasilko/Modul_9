import json
import requests   #  python -m pip install requests <<---install
from flask import Flask, render_template, request, redirect
import os # do obsługi plików, ładowania i wyładowywania
import csv

app = Flask (__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data=response.json()#data to lista całego request jako słownik
columns=['currency','code','bid','ask']

rates = data[0].get('rates')# wziełem rates/(lista słowników) bo rates to key

print(f'\nzawartość rates to: {rates}\n')#lista słowników kursów walut
#===============================================================================
def currencys():# currency ==waluty
    currency = []
    for i in rates:
        currency.append(i.get('code'))
    return sorted(currency)
#==============================================================================
currency = currencys()#to chyba do wywalenia
print(f'typ currency to: {type(currency)}')
print(f'zawartość currency to: {currency}\n')

#===============================================================================
with open('rates.csv', 'w') as csvfile:
    fieldnames = columns
    writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rates)

with open ("rates.csv") as filecsv:
    writer = csv.reader(filecsv,delimiter=';')
    for i in writer:
        pass
       #print(f'i to == {i}')

#===============================================================================
@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")
#===============================================================================
#================Calculator=====================================================

@app.route('/calculator', methods=["GET", "POST"])
def calkulator():
    if request.method == "GET":
        return render_template("calculator.html",currency=currency)

    if request.method == "POST":
        print(f'\nprint request ===================>> {request.form}')
        form =request.form #całość form z calculator
        print(f'wartosć data to :: {form} ')
        code =form.get('code') #skrót waluty
        amount=form.get('amount',type=float)#ilość waluty

        for key in rates:
            if key==code:
                aask=['ask']
        #ask = rates.get('ask',type=float) #ask to stawki

        #aask =rates.ask
        print (f'wartosc rates aask "{aask}')
        #print(f'wartosć data to :: {ask} ')
        print(amount)


        result = float (aask * amount)#ask nie ma w request form
        print(result)
        return  print(f'{amount} {code} będzie kosztować {result} polskich złotych')
#return render_template("calkulator.html",currency=currency)
#===============================================================================


if __name__ == "__main__":
    app.run(debug=True)

#data=json.dumps(response.json(),indent=2) <-- zwroci tekst jak w linii....todo