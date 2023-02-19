from django.shortcuts import render, redirect
from .forms import RainfallForm
from django.http import HttpResponse
from jalali_date import datetime2jalali, date2jalali
from datetime import date, timedelta
from .models import Station, Rainfall
import jdatetime


def rainfall_input_view(request):
    stations = Station.objects.all()
    rainfall_data = Rainfall()
    if request.method == "POST":
        rain_form = RainfallForm(request.POST, request.FILES)
        if rain_form.is_valid():
            rain_form.save()
            # return HttpResponse('اطلاعات با موفقیت وارد شد')
            return redirect('input_view')

        else:

            context = {
                'form': rain_form,
                'stations': stations,
                'rainfall_data_ave': rainfall_data.average(),
            }

            return render(request, "home/data_input.html", context)
    else:
        rain_form = RainfallForm()
        context = {
            'form': rain_form,
            'stations': stations,
            'rainfall_data_ave': rainfall_data.average(),
        }
        return render(request, "home/data_input.html", context)


def rainfall_info_view(request):
    # ///////////////////////////////////////////////////////
    start_of_month = date(2022, 9, 23)  # '2022-09-23'
    end_of_month = date(2022, 10, 22)  # '2022-10-22'

    # initializing dictionary
    dic = dict()
    stations = Station.objects.values_list('id', 'name').order_by('id')
    for station in stations:
        dic[station[1]] = [0] * 31

    rainfalls = Rainfall.objects.select_related('station').filter(submit_date__gte=start_of_month,
                                                                  submit_date__lte=end_of_month)

    for rainfall in rainfalls:
        jtoday = jdatetime.date.fromgregorian(date=rainfall.submit_date)
        dic[rainfall.station.name][jtoday.day - 1] = rainfall.value

    # /////////////////////////////////////////////////////////////////////

    colors = [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 255, 50, 1)',
        'rgba(20, 159, 64, 1)',
        'rgba(250, 100, 64, 1)',
        'rgba(50, 100, 255, 1)',
    ]
    counter = 0
    station_color = {}
    for station in stations:
        if counter <= len(stations):
            station_color[station[1]] = colors[counter]
            counter += 1
        else:
            break

    context = {
        'dics': dic,
        'headers': list(range(1, 32)),
        'station_colors': station_color,
    }

    return render(request, 'home/data_show.html', context)

# date2jalali(request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')
