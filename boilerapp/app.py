from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

# Load models
with open('xgb_Multivariate.pkl', 'rb') as f:
    model_h = pickle.load(f)

with open('xgb_min.pkl', 'rb') as f:
    model_m = pickle.load(f)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Hourwise manual
@app.route('/hourwise', methods=['GET', 'POST'])
def hourwise_analysis():
    if request.method == 'POST':
        input_data = [
            float(request.form[key]) for key in [
                'EFF_SF_Ratio_lag1', 'EFF_SF_Ratio_avg_window_length2', 'EFF_SF_Ratio_avg_window_length3',
                'EFF_SF_Ratio_lag2', 'EFF_FD_Fan_Out_lag1', 'EFF_Fuel_Flow_lag1', 'EFF_SF_Ratio_avg_window_length4',
                'EFF_Stack_Temp_lag1', 'EFF_Enthalpy_Loss_lag1', 'EFF_Steam_Temp_lag1', 'EFF_Blowdown_Loss_lag1'
            ]
        ]
        prediction_result = model_h.predict(np.array(input_data).reshape(1, -1))[0]
        return render_template('hourwise.html', prediction=prediction_result)
    return render_template('hourwise.html')

# Minutewise manual
@app.route('/minutewise', methods=['GET', 'POST'])
def minutewise_analysis():
    if request.method == 'POST':
        input_data = [
            float(request.form[key]) for key in [
                'EFF_Blowdown_Loss', 'EFF_Enthalpy_Loss', 'EFF_FD_Fan_Out', 'EFF_FeedWater_Temp',
                'EFF_Fuel_Flow', 'EFF_Fuel_Flow_Total', 'EFF_Stack_Loss', 'EFF_Stack_Temp', 'EFF_Steam_Flow'
            ]
        ]
        prediction_result = model_m.predict(np.array(input_data).reshape(1, -1))[0]
        return render_template('minute.html', prediction=prediction_result)
    return render_template('minute.html')

# Prescriptive Analysis
df_p = pd.read_csv("min_max_1.csv", index_col=None)

@app.route('/predict2', methods=['POST'])
def predict2():
    ip = request.form.get("SF_Ratio")
    df1_p = df_p.loc[df_p['SF_Ratio_Pred'] == float(ip)]
    df2_p = df1_p.T
    df2_p.columns = ['Value']
    df2_p['Value'] = df2_p['Value'].apply(lambda x: round(x, 1))
    prediction = df2_p.to_dict()['Value']
    return render_template('index_minx.html', prediction=prediction)

@app.route('/prescriptive')
def prescriptive_analysis():
    return render_template('index_minx.html')

# Dropdown Minute
@app.route("/browse_dropdown_m")
def browse_dropdown_m():
    files = os.listdir("static/data/minute")
    return render_template("browse.html", files=files)

@app.route('/predict_m_dropdown', methods=['POST'])
def predict_m_dropdown():
    file_name = request.form['file_name']
    file_path = os.path.join("static/data/minute", file_name)
    df = pd.read_csv(file_path)
    predictions = model_m.predict(df)
    df['predicted_SF_Ratio'] = predictions

    # Apply yellow background to predicted_SF_Ratio column
    styled_df = df.style.applymap(
        lambda val: 'background-color: yellow', subset=['predicted_SF_Ratio']
    )

    return render_template('browse_m.html', table=styled_df.to_html())

# Dropdown Hour
@app.route("/browse_dropdown_h")
def browse_dropdown_h():
    files = os.listdir("static/data/hour")
    return render_template("browse2.html", files=files)

@app.route('/predict_h_dropdown', methods=['POST'])
def predict_h_dropdown():
    file_name = request.form['file_name']
    file_path = os.path.join("static/data/hour", file_name)
    df = pd.read_csv(file_path)
    predictions = model_h.predict(df)
    df['predicted_SF_Ratio'] = predictions

    # Apply yellow background to the predicted column
    styled_df = df.style.applymap(
        lambda val: 'background-color: yellow', subset=['predicted_SF_Ratio']
    )

    return render_template('browse_h.html', table=styled_df.to_html())


# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

