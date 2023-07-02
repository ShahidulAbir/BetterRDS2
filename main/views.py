from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
import pandas as pd
import json


# Create your views here.
def homepage(request):
    df = pd.read_excel("main/static/original.xlsx")

    df['Split'] = df['Time'].str.split()
    df['Split'].astype('object')

    df['Day'] = 0
    df['Start_Time'] = 0
    df['Finish_Time'] = 0
    for index, row in df.iterrows():
        if len(row['Split']) == 6:
            df['Day'][index] = row['Split'][0]
            df['Start_Time'][index] = f"{row['Split'][1]} {row['Split'][2]}"
            df['Finish_Time'][index] = f"{row['Split'][4]} {row['Split'][5]}"
        else:
            df['Day'][index] = "TBA"
            df['Start_Time'][index] = "TBA"
            df['Finish_Time'][index] = "TBA"

    df = df.drop(['Time', 'Split', 'Unnamed: 0'], axis=1)
    df.rename(columns={'Seats Available': 'Seats_Available'}, inplace=True)
    df.index += 1

    json_records = df.reset_index().to_json(orient='records')
    data = json.loads(json_records)
    print(data[:10])
    return render(request, 'main/homepage.html', {"data": data})
