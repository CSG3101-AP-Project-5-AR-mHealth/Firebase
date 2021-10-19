from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, recall_score, accuracy_score, precision_score

import pandas as pd
from zipfile import ZipFile
import os
from os.path import exists
import json

json_path = "heart_rate.json"

# Retrieved from Kaggle
# TODO: share link where data was retrieved from
if not exists(json_path):
    zip_path = "heart_rate.json.zip"
    zip_file = ZipFile(zip_path)
    zip_file.extractall()

with open(json_path) as f:
    d = json.load(f)

# Normalize Json
df = pd.json_normalize(d)

# Convert dateTime object
df['dateTime'] = pd.to_datetime(df['dateTime'])

# Remove confidence
df = df.drop(['value.confidence'], axis=1)

# Show the data we are working with
df.shape
df.info()
print(df.head(-10))

df.sort_values(by="dateTime")
df = df.set_index('dateTime')

df_test_data = df.loc[(df.index > '2020-01-10 00:00:00') & (df.index <= '2020-01-10 23:59:59')]
df_training = df.loc[(df.index > '2020-01-14 00:00:00') & (df.index <= '2020-01-18 23:59:59')]

# fig1, ax1 = plt.subplots()
# df_training.plot(legend=False, ax=ax1)
# plt.title("Visualize Training Data")
# plt.show()

# fig2, ax2 = plt.subplots()
# df_test_data.plot(legend=False, ax=ax2)
# plt.title("Visualize Testing Data")
# plt.show()

# TODO: Need to save this data to predict anomalies later
training_mean = df_training.mean()
training_std = df_training.std()
df_training_value = (df_training - training_mean) / training_std
print("\nMean:", str(training_mean), "Standard: ", str(training_std))
print("\nNumber of training samples:", len(df_training_value))

TIME_STEPS = 1

# This is used to predict anomalies later with time steps being reduced to 1.
def create_sequences(values, time_steps=TIME_STEPS):
    output = []
    for i in range(len(values) - time_steps + 1):
        output.append(values[i : (i + time_steps)])
    return np.stack(output)


x_train = create_sequences(df_training_value.values)
print("Training input shape: ", x_train.shape)
print(x_train[:10])

model = keras.Sequential(
    [
        keras.layers.Input(shape=(x_train.shape[1], x_train.shape[2])),
        keras.layers.Conv1D(
            filters=256, kernel_size=7, padding="same", strides=2, activation="relu"
        ),
        keras.layers.Dropout(rate=0.2),
        keras.layers.Conv1D(
            filters=128, kernel_size=7, padding="same", strides=2, activation="relu"
        ),
        keras.layers.Dropout(rate=0.2),
        keras.layers.Conv1D(
            filters=64, kernel_size=7, padding="same", strides=2, activation="relu"
        ),
        keras.layers.Conv1DTranspose(
            filters=64, kernel_size=7, padding="same", strides=2, activation="relu"
        ),
        keras.layers.Dropout(rate=0.2),
        keras.layers.Conv1DTranspose(
            filters=128, kernel_size=7, padding="same", strides=2, activation="relu"
        ),
        keras.layers.Dropout(rate=0.2),
        keras.layers.Conv1DTranspose(
            filters=256, kernel_size=7, padding="same", strides=2, activation="relu"
        ),
        keras.layers.Conv1DTranspose(filters=1, kernel_size=7, padding="same"),
    ]
)
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001), loss="mse")
model.summary()

history = model.fit(
    x_train,
    x_train,
    epochs=50,
    batch_size=256,
    validation_split=0.1,
    callbacks=[
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=5, mode="min", verbose=1)
    ],
)

# Plotting loss to check for overfitting
fig = plt.figure()
plt.plot(history.history['loss'], label='Training loss')
plt.plot(history.history['val_loss'], label='Validation loss')
plt.ylabel('Loss')
plt.xlabel('No. Epochs')
plt.legend()
plt.show()


# Get train MAE loss.
x_train_pred = model.predict(x_train, verbose=1)
train_mae_loss = np.mean(np.abs(x_train_pred - x_train), axis=1)

plt.hist(train_mae_loss, bins=10)
plt.xlabel("Train MAE loss")
plt.ylabel("No of samples")
plt.title("Reconstruction Error Threshold")
plt.show()

# Get reconstruction loss threshold.
threshold = np.max(train_mae_loss)
print("Reconstruction error threshold: ", threshold)

#Prepare test data
df_test_value = (df_test_data - training_mean) / training_std
# fig, ax = plt.subplots()
# df_test_value.plot(legend=False, ax=ax)
# plt.title("Prepared Test Data")
# plt.show()

# Create sequences from test values.
x_test = create_sequences(df_test_value.values)
print("Test input shape: ", x_test.shape)

# Get test MAE loss.
x_test_pred = model.predict(x_test, verbose=1)
test_mae_loss = np.mean(np.abs(x_test_pred - x_test), axis=1)
test_mae_loss = test_mae_loss.reshape((-1))

plt.hist(test_mae_loss, bins=10)
plt.xlabel("Test MAE loss")
plt.ylabel("No of samples")
plt.show()

# Detect all the samples which are anomalies.
anomalies = test_mae_loss > threshold
print("Number of anomaly samples: ", np.sum(anomalies))
# print("Indices of anomaly samples: ", np.where(anomalies))
actualAnomalies = df_test_data > 150
print("Number of anomaly samples: ", np.sum(actualAnomalies))
# print("Indices of anomaly samples: ", np.where(actualAnomalies))

conf_matrix = confusion_matrix(actualAnomalies, anomalies)
plt.figure(figsize=(4, 4))
sns.heatmap(conf_matrix, annot=True, fmt="d");
plt.title("Confusion matrix")
plt.ylabel('True class')
plt.xlabel('Predicted class')
plt.show()
# print Accuracy, precision and recall
print(" Accuracy: ",accuracy_score(actualAnomalies, anomalies))
print(" Recall: ",recall_score(actualAnomalies, anomalies))
print(" Precision: ",precision_score(actualAnomalies, anomalies))

# data i is an anomaly if samples [(i - timesteps + 1) to (i)] are anomalies
# anomalous_data_indices = []
# for data_idx in range(TIME_STEPS - 1, len(df_test_value) - TIME_STEPS + 1):
#     if np.all(anomalies[data_idx - TIME_STEPS + 1 : data_idx]):
#         anomalous_data_indices.append(data_idx)

df_subset = df_test_data.iloc[np.where(anomalies)]
# df_subset1 = df_test_data.iloc[np.where(actualAnomalies)]
fig, ax = plt.subplots()
df_test_data.plot(legend=False, ax=ax)
df_subset.plot(legend=False, ax=ax, color="r")
# df_subset1.plot(legend=False, ax=ax, color="g")
plt.xlabel("Date Time")
plt.ylabel("Heart Rate")
plt.show()

model.save("saved_model")

# reconstructed_model = keras.models.load_model("saved_model")

# # Let's check:
# # np.testing.assert_allclose(
# #     model.predict(x_test), reconstructed_model.predict(x_test)
# # )