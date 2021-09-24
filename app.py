import json
import requests  
from flask import Flask, render_template, request, redirect
import os 
import csv

app = Flask (__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data=response.json()
rates = data[0].get('rates')

#===============================================================================
def get_codes():
    codes = []
    for data in rates:
        codes.append(data.get('code'))
    return sorted(codes)

codes = get_codes()

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
#===============================================================================
@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

#================Calculator=====================================================

@app.route('/calculator', methods=["GET", "POST"])
def calculator():
    if request.method == "GET":
        return render_template("calculator.html",rates=rates)

    if request.method == "POST":
        form =request.form #całość form z calculator
        code =form.get('rates',type=float) #skrót waluty
        amount=form.get('amount',type=float)#ilość waluty
        price = code*amount
        # communicat=print ('% 2 f' % price )
        print(f'\nTo będzie kosztować {price } polskich złotych\n')
        return render_template("/response.html",price = price )
#===============================================================================
if __name__ == "__main__":
    app.run(debug=True)

#data=json.dumps(response.json(),indent=2) <-- zwroci tekst jak w linii....todo