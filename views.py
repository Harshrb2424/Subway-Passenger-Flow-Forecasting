from django.shortcuts import render
from .models import TrafficPrediction
import joblib
import pandas as pd
import random

def predict_traffic(request):
    if request.method == 'POST':
        stop_name = request.POST.get('stop_name')
        line = request.POST.get('line')
        hour = request.POST.get('hour')
        day = request.POST.get('day')
        
        try:
            hour = int(hour)
            day = int(day)
        except ValueError:
            return render(request, 'traffic/predict_traffic.html', {
                'error_message': 'Hour and day must be integers.'
            })

        print(f"Stop Name: {stop_name}")
        print(f"Line: {line}")
        print(f"Hour: {hour}")
        print(f"Day: {day}")

        model = joblib.load('traffic_predictor')
        data_new = pd.DataFrame({
            'Stop Name': [int(stop_name)],
            'Line': [int(line)],
            'Hour': [int(hour)],
            'Day': [int(day)]
        })
        result = model.predict(data_new)
        print(result)
        enter_count=(result[0][0])
        leave_count=(result[0][1])

        day_results = []
        for hour in range(24):
            day_data = pd.DataFrame({
                'Stop Name': [int(stop_name)],
                'Line': [int(line)],
                'Hour': [hour],
                'Day': [int(day)]
            })
            result = model.predict(day_data)
            day_results.append([adjust_number(result[0][0]), adjust_number(result[0][1])])
        print(day_results)

        week_results = []
        for day in range(7):
            week_data = pd.DataFrame({
                'Stop Name': [int(stop_name)],
                'Line': [int(line)],
                'Hour': [int(hour)],
                'Day': [day] 
            })
            result = model.predict(week_data)
            week_results.append([adjust_number(result[0][0]), adjust_number(result[0][1])]) 
        print(week_results)

        prediction = TrafficPrediction.objects.create(
            stop_name=(stop_name),
            line=(line),
            hour=hour,
            day=day,
            enter_count=adjust_number(enter_count),
            leave_count=adjust_number(leave_count))
        print(prediction)

        return render(request, 'traffic/prediction_result.html', {'prediction': prediction, 'week_results':week_results, 'day_results': day_results})
    return render(request, 'traffic/predict_traffic.html')

def adjust_number(number):
    if number < 0:
        return random.uniform(0.01, 0.1) 
    else:
        adjustment = number * random.uniform(0.95, 1.05)
        return round(adjustment)
