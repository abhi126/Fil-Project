import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import pandas as pd;
from tensorflow.keras.models import model_from_json

from sklearn.metrics import *
from sklearn.metrics import mean_squared_error

import yfinance as yf


# import yfinance as yf
import datetime as dt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Bidirectional, Dropout, Activation, Dense, LSTM
from tensorflow.keras.models import Sequential

#from CryptOS.home.views import prediction_data
def data12():
    crypto_currency = 'USDT-USD'

    # start = dt.datetime(2014,1,1)
    # end = dt.datetime.now()
    # data1 = yf.download(crypto_currency,start=start, end=end)
    # print(data1)
    # data1.to_excel('C:/Users/BHAVYA NANGIA/Desktop/FIL Training bitbucket/CryptOS/home/tether.xlsx')

    data1=pd.read_excel("C:/Users/BHAVYA NANGIA/Desktop/FIL Training bitbucket/CryptOS/home/tether.xlsx")
    data = data1.reset_index()
    #Preparing data
    print(data.tail())
    print(data.columns)
    print(data['Date'].tail())
    l=list(data['Date'])
    #data1.to_excel("E:\FIL-Project\CryptOS\home\data_bitc.xlsx")

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))
    print(len(scaled_data))
    #print(scaled_data)

    prediction_days = 10
    future_day = 5

    x_train, y_train = [], []

    for x in range(prediction_days, len(scaled_data)- future_day):
        x_train.append(scaled_data[x-prediction_days:x, 0])
        y_train.append(scaled_data[x + future_day, 0])

    #print(x_train)
    x_train, y_train = np.array(x_train), np.array(y_train)
    print(x_train.shape[0], x_train.shape[1])
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    #neural network
    # model = Sequential()

    # model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    # model.add(Dropout(0.2))

    # model.add(LSTM(units=50, return_sequences=True))
    # model.add(Dropout(0.2))

    # model.add(LSTM(units=50))
    # model.add(Dropout(0.2))

    # model.add(Dense(units=1))
    # model.compile(optimizer='adam', loss='mean_squared_error')

    # history = model.fit(
    #     x_train, 
    #     y_train, 
    #     epochs=25, 
    #     batch_size=32
    # )

    # model_json = model.to_json()
    # print(model_json)
    # with open("C:/Users/BHAVYA NANGIA/Desktop/FIL Training bitbucket/CryptOS/home/model_tether.json", "w") as json_file:
    #     json_file.write(model_json)
    # # serialize weights to HDF5
    # model.save_weights("C:/Users/BHAVYA NANGIA/Desktop/FIL Training bitbucket/CryptOS/home/model_tether.h5")
    # print("Saved model to disk")

    json_file = open('C:/Users/BHAVYA NANGIA/Desktop/FIL Training bitbucket/CryptOS/home/model_tether.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("C:/Users/BHAVYA NANGIA/Desktop/FIL Training bitbucket/CryptOS/home/model_tether.h5")
    print("Loaded model from disk")

    # evaluate loaded model on test data
    # model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    # score = model.evaluate(x_train, y_train, verbose=0)
    # print("%s: %.2f%%" % (model.metrics_names[1], score[1]*100))
    #testing the model
    test_start = dt.datetime(2020,1,1)
    test_end = dt.datetime.now()

    #test_data = yf.download(crypto_currency, test_start, test_end)
    #test_data.to_excel("E:\FIL-Project\CryptOS\home\data_bitc1.xlsx")
    test_data=pd.read_excel("C:/Users/BHAVYA NANGIA/Desktop/FIL Training bitbucket/CryptOS/home/tether.xlsx")
    test_data1=test_data.reset_index()
    l1=list(test_data1['Date'])
    actual_prices = list(test_data['Close'].values)
    #print(actual_prices)

    total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)
    model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.fit_transform(model_inputs)


    x_test = []
    y_test=[]
    for x in range(prediction_days, len(model_inputs) - future_day):
        x_test.append(model_inputs[x-prediction_days:x, 0])
        y_test.append(model_inputs[x + future_day, 0])



    x_test = np.array(x_test)
    p=x_test
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    y_test = np.array(y_test)
    prediction_prices = model.predict(x_test)
    R2=r2_score(prediction_prices,y_test)
    MAE=mean_squared_error(prediction_prices,y_test)
    print(R2,MAE)
    model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    score = model.evaluate(x_test,y_test,verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], score[1]*100))
    # print(classification_report(y_test, prediction_prices))
    # print(confusion_matrix(y_test, prediction_prices))

    # rfc_f1 = round(f1_score(y_test, prediction_prices, average= 'weighted'), 3)
    # rfc_accuracy = round((accuracy_score(y_test, prediction_prices) * 100), 2)

    # print("Accuracy : " , rfc_accuracy , " %")
    # print("f1_score : " , rfc_f1)
    prediction_prices = scaler.inverse_transform(prediction_prices)

    # model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
    # score = model.evaluate(p,y_test , verbose=0)
    # print(score)
    # print("%s: %.2f%%" % (model.metrics_names[1], score[1]*100))
    # R2=r2_score(prediction_prices,y_test)
    # MAE=mean_squared_error(prediction_prices,y_test)
    # print(R2,MAE)
    # print(y_test,prediction_prices)

    plt.plot(l[0:len(actual_prices)],actual_prices)
    plt.plot(l[0:len(actual_prices)],actual_prices, color='black', label='Actual Prices')
    plt.plot(l[0:len(prediction_prices)],prediction_prices, color='green', label='Predicted Prices')
    # plt.xticks(l)
    plt.title(f'{crypto_currency} price prediction')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend(loc='upper left')
    plt.show()

    #Predict next day
    print(len(x_test),len(prediction_prices))
    real_data = [model_inputs[len(model_inputs) + 1 -prediction_days: len(model_inputs) + 1, 0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

    
    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)
    print(f"{future_day}th Day Tether Price:")
    print(prediction)
    #print(list(prediction_prices[0:,0]))
    t23=[]
    for i in l1[prediction_days+future_day+1:]:
        i=str(i)
        t23.append(i[0:10])
       
    # print(t23)
    return list(actual_prices[prediction_days+future_day+1:]),list(prediction_prices[0:,0]),t23,prediction[0,0]
    #print(actual_prices)
data12()