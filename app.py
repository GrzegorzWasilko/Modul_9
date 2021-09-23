import json
import requests   #  python -m pip install requests <<---install
from flask import Flask, render_template, request, redirect
import os # do obsługi plików, ładowania i wyładowywania
import csv

app = Flask (__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data=response.json()#data to lista całego request jako słownik
rates = data[0].get('rates')# wziełem rates/(lista słowników) bo rates to key
#print(f'\nzawartość rates to: {rates}\n')#lista słowników kursów walut
#===============================================================================
def get_codes():
    codes = []
    for data in rates:
        codes.append(data.get('code'))
    return sorted(codes)

codes = get_codes()#codes to lista ['AUD', 'CAD', 'CHF', 'CZK', ....

#print(f'typ codes to: {type(codes)}')
print(f'zawartość codes to: {codes}\n')
#==============================================================================
columns=['currency','code','bid','ask']
#==============================================================================
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
def calculator():
    if request.method == "GET":
        return render_template("calculator.html",rates=rates)

    if request.method == "POST":
        print(f'\nprint request ==========>> {request.form}')
        form =request.form #całość form z calculator
        print(f'\nform to  ==========>> {form}')
        code =form.get('rates',type=float) #skrót waluty
        print(f'\ncode to  ==========>> {code}')
        amount=form.get('amount',type=float)#ilość waluty
        print(f'\namount to  ==========>> {amount}')
        price = code*amount
        return  print(f'\n{amount} {code} będzie kosztować {price} polskich złotych\n')
#return render_template("calculator.html",currency=currency)
#===============================================================================


if __name__ == "__main__":
    app.run(debug=True)

#data=json.dumps(response.json(),indent=2) <-- zwroci tekst jak w linii....todo