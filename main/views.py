from django.shortcuts import render
from pandas import read_html, to_datetime
import requests
import json


# Create your views here.
def homepage(request):
   header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    url = "https://rds2.northsouth.edu/index.php/common/showofferedcourses"

    r = requests.get(url, headers=header)
    df = read_html(r.text)[0]

    df['Day'] = df['Split'].apply(lambda x: x[0] if len(x) == 6 else "TBA")
    df['Start_Time'] = df['Split'].apply(lambda x: f"{x[1]} {x[2]}" if len(x) == 6 else "TBA")
    df['Finish_Time'] = df['Split'].apply(lambda x: f"{x[4]} {x[5]}" if len(x) == 6 else "TBA")

    df = df.drop(['Split'], axis=1)

    df['Formatted_Time'] = to_datetime(df['Start_Time'], format='%I:%M %p', errors='coerce')
    df = df.sort_values(['Course', 'Day', 'Formatted_Time', 'Section'])

    df.rename(columns={'Seats Available': 'Seats_Available'}, inplace=True)

    json_records = df.reset_index().to_json(orient='records')
    data = json.loads(json_records)

    return render(request, 'main/homepage.html', {"data": data})


def previous(request):
    return render(request, 'main/previous.html')
