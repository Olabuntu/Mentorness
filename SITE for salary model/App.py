from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler

# Load the model
model = pickle.load(open('Model/model_Lcv.pkl', 'rb'))

with open('Model/scaler.pkl', 'rb') as f:
    scale = pickle.load(f)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    input_data1 = request.form['input_data1']
    input_data2 = request.form['input_data2']
    input_data3 = request.form['input_data3']
    input_data4 = request.form['input_data4']
    input_data5 = request.form['input_data5']
    input_data6 = int(request.form['input_data6'])
    input_data7 = int(request.form['input_data7'])
    
    if input_data1 == '' or input_data2 == '' or input_data3 == '' or input_data4 == '' or input_data5 == '' or input_data6 == '' or input_data7 == '':
        return "Please fill in all fields", 400
    Age =float(input_data1)
    leave_used = float(input_data2)
    leave_remaining = float(input_data3)
    rating = float(input_data4)
    past_exp =float(input_data5)
    DESIGNATION_Analyst,DESIGNATION_Associate,DESIGNATION_Director,DESIGNATION_Manager,DESIGNATION_Senior_Analyst,DESIGNATION_Senior_Manager = 0,0,0,0,0,0
    UNIT_Finance,UNIT_IT,UNIT_Management,UNIT_Marketing,UNIT_Operations,UNIT_Web = 0,0,0,0,0,0
    if input_data6 == 1:
        DESIGNATION_Analyst,DESIGNATION_Associate,DESIGNATION_Director,DESIGNATION_Manager,DESIGNATION_Senior_Analyst,DESIGNATION_Senior_Manager =1,0,0,0,0,0
    elif input_data6 == 2:
        DESIGNATION_Analyst,DESIGNATION_Associate,DESIGNATION_Director,DESIGNATION_Manager,DESIGNATION_Senior_Analyst,DESIGNATION_Senior_Manager =0,1,0,0,0,0
    elif input_data6 == 3:
        DESIGNATION_Analyst,DESIGNATION_Associate,DESIGNATION_Director,DESIGNATION_Manager,DESIGNATION_Senior_Analyst,DESIGNATION_Senior_Manager =0,0,1,0,0,0
    elif input_data6 == 4:
        DESIGNATION_Analyst,DESIGNATION_Associate,DESIGNATION_Director,DESIGNATION_Manager,DESIGNATION_Senior_Analyst,DESIGNATION_Senior_Manager =0,0,0,1,0,0
    elif input_data6 == 5:
        DESIGNATION_Analyst,DESIGNATION_Associate,DESIGNATION_Director,DESIGNATION_Manager,DESIGNATION_Senior_Analyst,DESIGNATION_Senior_Manager =0,0,0,0,1,0
    elif input_data6 == 6:
        DESIGNATION_Analyst,DESIGNATION_Associate,DESIGNATION_Director,DESIGNATION_Manager,DESIGNATION_Senior_Analyst,DESIGNATION_Senior_Manager =0,0,0,0,0,1

    

    if input_data7 == 1:
        UNIT_Finance,UNIT_IT,UNIT_Management,UNIT_Marketing,UNIT_Operations,UNIT_Web = 1,0,0,0,0,0
    elif input_data7 == 2:
        UNIT_Finance,UNIT_IT,UNIT_Management,UNIT_Marketing,UNIT_Operations,UNIT_Web = 0,1,0,0,0,0
    elif input_data7 == 3:
        UNIT_Finance,UNIT_IT,UNIT_Management,UNIT_Marketing,UNIT_Operations,UNIT_Web = 0,0,1,0,0,0
    elif input_data7 == 4:
        UNIT_Finance,UNIT_IT,UNIT_Management,UNIT_Marketing,UNIT_Operations,UNIT_Web = 0,0,0,1,0,0
    elif input_data7 == 5:
        UNIT_Finance,UNIT_IT,UNIT_Management,UNIT_Marketing,UNIT_Operations,UNIT_Web = 0,0,0,0,1,0
    elif input_data7 == 6:
        UNIT_Finance,UNIT_IT,UNIT_Management,UNIT_Marketing,UNIT_Operations,UNIT_Web = 0,0,0,0,0,1
    
    input_data1 = pd.DataFrame([[Age,leave_used,leave_remaining,rating,past_exp,DESIGNATION_Analyst,DESIGNATION_Associate,DESIGNATION_Director,DESIGNATION_Manager,DESIGNATION_Senior_Analyst,DESIGNATION_Senior_Manager,UNIT_Finance,UNIT_IT,UNIT_Management,UNIT_Marketing,UNIT_Operations,UNIT_Web]])
    input_data1.columns = [ 'AGE','LEAVES USED','LEAVES REMAINING','RATINGS','PAST EXP','DESIGNATION_Analyst','DESIGNATION_Associate','DESIGNATION_Director','DESIGNATION_Manager','DESIGNATION_Senior Analyst','DESIGNATION_Senior Manager','UNIT_Finance','UNIT_IT','UNIT_Management','UNIT_Marketing','UNIT_Operations','UNIT_Web']
    
    input_data = scale.transform(input_data1)
    input_data = pd.DataFrame(input_data, columns= input_data1.columns) 
    
    print(input_data1)
    prediction = model.predict(input_data)
    prediction =round (prediction[0],2)

   
    
    return f"The Staff will be paid: {prediction}", 200

if __name__ == '__main__':
    app.run(debug=True)
