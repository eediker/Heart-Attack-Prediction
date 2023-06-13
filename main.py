from flask import Flask, render_template,request,jsonify
import pickle
import numpy as np
from flask_mysqldb import MySQL

app = Flask(__name__)
model = pickle.load(open("gaussian_model.pkl","rb"))

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'eediker'
app.config['MYSQL_PASSWORD'] = 'm123456789m'
app.config['MYSQL_DB'] = 'heart_attack_prediction'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route("/predict",methods = ["POST"])
def predict():
    cur = mysql.connection.cursor()

    float_features = [int(x) for x in request.form.values()]
    features = [np.array(float_features)]
    prediction = model.predict(features)

    if prediction == 1:
        label = "Kalp Krizi Riskiniz Bulunmaktadır"
    else:
        label = "Kalp krizi Riskiniz Bulunmamaktadır"

    cur.execute("INSERT INTO mytable (age, sex, exang, ca, cp, trestbps, chol, fbs, rest_ecg, thalach, target) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (float_features[0], float_features[1], float_features[2], 
                float_features[3], float_features[4], float_features[5], 
                float_features[6], float_features[7], float_features[8], 
                float_features[9], prediction[0]))

    mysql.connection.commit()

    cur.close()

    return render_template("index.html",label=label)


if __name__ == '__main__':
    app.run(debug=True)


