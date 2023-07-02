from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
import pandas as pd
import json


# Create your views here.
def homepage(request):
    df = pd.read_excel("main/static/original.xlsx")

    df['Split'] = df['Time'].str.split()

    df['Day'] = df['Split'].apply(lambda x: x[0] if len(x) == 6 else "TBA")
    df['Start_Time'] = df['Split'].apply(lambda x: f"{x[1]} {x[2]}" if len(x) == 6 else "TBA")
    df['Finish_Time'] = df['Split'].apply(lambda x: f"{x[4]} {x[5]}" if len(x) == 6 else "TBA")

    df = df.drop(['Time', 'Split', 'Unnamed: 0'], axis=1)

    df.rename(columns={'Seats Available': 'Seats_Available'}, inplace=True)
    df.index += 1

    json_records = df.reset_index().to_json(orient='records')
    data = json.loads(json_records)
    return render(request, 'main/homepage.html', {"data": data})
