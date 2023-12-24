from flask import Flask,request,render_template
import pandas as pd
from src.utils import get_schedule
from src.exception import CustomException

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/checkprice', methods= ['GET','POST'])
def predict():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        try:
            trainNumber = int(request.form.get('trainNumber'))
            fromStnCode = request.form.get('fromStnCode')
            toStnCode = request.form.get('toStnCode')
            classCode = request.form.get('classCode')
            superFast = request.form.get('superFast')
            #return render_template('wait.html')
            schedule_df = pd.read_csv('artifacts\\clean_schedule.csv')

            schedule = get_schedule(trainNumber,schedule_df)

            html_table = schedule.to_html(index=False)

            
            return render_template('schedule.html',trainNumber=trainNumber ,my_dataframe=html_table)
        except CustomException as ce:
            # Handle the custom exception
            print(f"Custom Exception: {ce}")
            return render_template('error.html')











if __name__ == "__main__":
    app.run(debug=True,port=5002)
