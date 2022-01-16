from flask import Flask 
from flask import render_template, request 
import json

app = Flask(__name__) 

@app.route('/') 
def index(): 
    return render_template('practice.html') 

@app.route('/busstop_p.html') 
def index2(): 
    return render_template('busstop_p.html') 

@app.route('/busstop_r.html') 
def index3(): 
    return render_template('busstop_r.html') 

@app.route('/speech.html') 
def index4(): 
    return render_template('speech.html') 

    

@app.route('/result', methods =['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        print(result)
        return render_template("index4.html",result=result)

       
    
#print(result)

if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=8080)

