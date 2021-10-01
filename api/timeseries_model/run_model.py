import os
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Lowered Time step due to it being less data
TIME_STEPS = 1

# Generated training sequences for use in the model.
def create_sequences(values, time_steps=TIME_STEPS):
    output = []
    for i in range(len(values) - time_steps + 1):
        output.append(values[i : (i + time_steps)])
    return np.stack(output)

def predict_anomaly(data):
    df = pd.json_normalize(data)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.set_index('datetime')
    df = df.drop(['id', 'steps', 'temperature'], axis=1)

    #load model
    model = keras.models.load_model(os.path.join("timeseries_model","saved_model"))
    # TODO: Load threshold, training mean and training standard at the moment hard coded
    training_mean = 60.366638
    training_std = 13.195903
    threshold = 0.6135520352243726

    #Prepare data
    df_test_value = (df - training_mean) / training_std
    x_test = create_sequences(df_test_value.values)

    # Get test MAE loss.
    x_test_pred = model.predict(x_test)
    test_mae_loss = np.mean(np.abs(x_test_pred - x_test), axis=1)
    test_mae_loss = test_mae_loss.reshape((-1))

    # Detect all the samples which are anomalies.
    anomalies = test_mae_loss > threshold
    # print(anomalies)
    # print("Number of anomaly samples: ", np.sum(anomalies))
    # print("Indices of anomaly samples: ", np.where(anomalies))
    return np.where(anomalies)



def test_model():
    d = [
        {"datetime":"2021-08-25 14:19:03",	"heartRate":89},
        {"datetime":"2021-08-25 14:20:02",	"heartRate":105},
        {"datetime":"2021-08-25 14:20:10",	"heartRate":111},
        {"datetime":"2021-08-25 14:20:46",	"heartRate":124},
        {"datetime":"2021-08-25 14:20:56",	"heartRate":116},
        {"datetime":"2021-08-25 14:21:13",	"heartRate":118},
        {"datetime":"2021-08-25 14:21:32",	"heartRate":110},
        {"datetime":"2021-08-25 14:21:47",	"heartRate":113},
        {"datetime":"2021-08-25 14:22:09",	"heartRate":106},
        {"datetime":"2021-08-25 14:22:24",	"heartRate":160},
        {"datetime":"2021-08-25 14:23:12",	"heartRate":73},
        {"datetime":"2021-08-25 14:23:42",	"heartRate":73},
        {"datetime":"2021-08-25 14:24:44",	"heartRate":73},
        {"datetime":"2021-08-25 14:24:48",	"heartRate":84},
        {"datetime":"2021-08-25 14:25:06",	"heartRate":70},
        {"datetime":"2021-08-25 14:25:19",	"heartRate":59},
        {"datetime":"2021-08-25 14:25:28",	"heartRate":55},
        {"datetime":"2021-08-25 14:26:05",	"heartRate":65}
    ]

    anomalies = predict_anomaly(d) 
    assert anomalies[0][0] == 8, "failed to pick up anomaly"   
    print("Anomaly detected at: ", d[anomalies[0][0]])