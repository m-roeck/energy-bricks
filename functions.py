# Total_Load  == https://www.iso-ne.com/ws/wsclient?_ns_requestType=threedayforecast == API JSON 
# lag24 == SKIP
# lag48 == https://www.iso-ne.com/isoexpress/web/reports/pricing/-/tree/lmps-rt-hourly-final == csv, requires datetime code
# last_day_LMP == https://www.iso-ne.com/isoexpress/web/reports/pricing/-/tree/lmps-rt-hourly-final == csv, requires datetime code
# month == datetime 
# day == datetime
# tot_solar_mwh == SKIP
# tot_wind_mwh == https://www.iso-ne.com/isoexpress/web/reports/operations/-/tree/seven-day-wind-power-forecast == csv, requires datetime code


import requests
import json
import pandas as pd
from datetime import date, timedelta
from pycaret.regression import *
from pycaret.classification import load_config

def retrieve_forecast():
    node = ['LD.NEW_HAVN46']

    response = requests.get('https://www.iso-ne.com/ws/wsclient?_ns_requestType=threedayforecast')
    list = response.json()

    Total_Load = []
    for x in range(0,24):
        Total_Load.append(list[0]['data']['day2'][x]['AdjustedMw'])

    tomorrow = date.today() + timedelta(1)
    yesterday = date.today() - timedelta(2)

    month = []
    day = []
    for x in range(0,24):
        month.append(tomorrow.strftime("%m"))
        day.append(tomorrow.strftime("%d"))

    date_code = str(yesterday.strftime("20%y")) + str(yesterday.strftime("%m")) + str(yesterday.strftime("%d"))

    url = "https://www.iso-ne.com/static-transform/csv/histRpts/rt-lmp/lmp_rt_final_" + date_code + ".csv"
    main_df = pd.read_csv(url, skiprows=4, usecols=range(1,10))

    main_df = main_df[main_df['Location Name'].isin(node)]
    main_df = main_df.reset_index(drop=True)

    main_df['Locational Marginal Price'] = pd.to_numeric(main_df['Locational Marginal Price'], downcast="float")
    average = main_df['Locational Marginal Price'].mean()

    last_day_LMP = []
    for x in range(0,24):
        last_day_LMP.append(average)

    main_df = main_df.drop(['Location ID', 'Location Name',
                'Location Type', 'Energy Component', 'Congestion Component', 
                'Marginal Loss Component', 'Hour Ending'], axis=1)

    main_df.rename(columns = {'Locational Marginal Price':'lag48'}, inplace = True)

    Hour_Ending = []
    for x in range(0,24):
        Hour_Ending.append(x)

    main_df['last_day_LMP'] = last_day_LMP
    main_df['month'] = month
    main_df['day'] = day
    main_df['Total_Load'] = Total_Load
    main_df['Hour_Ending'] = Hour_Ending

    main_df['Hour_Ending'] = main_df['Hour_Ending'].astype(int)
    main_df['Date'] = pd.to_datetime(main_df['Date']) + pd.to_timedelta(main_df['Hour_Ending'], unit='h')
    main_df = main_df.drop(['Hour_Ending'], axis=1)

    main_df.to_csv('testing_per_usual.csv')
    main_df = pd.read_csv('testing_per_usual.csv')
    main_df = main_df.drop(['Unnamed: 0'], axis=1)


    main_df['LMP'] = main_df['lag48']

    columns = ['Date', 'LMP', 'Total_Load', 'lag48', 'last_day_LMP', 'month', 'day']

    main_df = main_df[columns]

    load_config('models/model_config')


    final_et = load_model('models/et_model');
    final_rf = load_model('models/rf_model');
    final_xgboost = load_model('models/xgboost_model');
    final_catboost = load_model('models/catboost_model');
    final_lightgbm = load_model('models/lightgbm_model');
    final_dt = load_model('models/dt_model');

    et_predictions = predict_model(final_et, data=main_df)[['Label']]
    rf_predictions = predict_model(final_rf, data=main_df)[['Label']]
    xgboost_predictions = predict_model(final_xgboost, data=main_df)[['Label']]
    catboost_predictions = predict_model(final_catboost, data=main_df)[['Label']]
    lightgbm_predictions = predict_model(final_lightgbm, data=main_df)[['Label']]
    dt_predictions = predict_model(final_dt, data=main_df)[['Label']]

    et_predictions.rename(columns = {'Label':'et'}, inplace = True)
    rf_predictions.rename(columns = {'Label':'rf'}, inplace = True)
    xgboost_predictions.rename(columns = {'Label':'xgboost'}, inplace = True)
    catboost_predictions.rename(columns = {'Label':'catboost'}, inplace = True)
    lightgbm_predictions.rename(columns = {'Label':'lightgbm'}, inplace = True)
    dt_predictions.rename(columns = {'Label':'dt'}, inplace = True)

    prediction = pd.concat([et_predictions, rf_predictions, xgboost_predictions, catboost_predictions, lightgbm_predictions, dt_predictions], axis=1)
    # print(prediction)
    # prediction.to_csv('prediction_testing.csv')
    
    return prediction
