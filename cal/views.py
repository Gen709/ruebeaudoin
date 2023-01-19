from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

import calendar
from datetime import datetime as dt, timedelta
from dateutil import relativedelta


# Create your views here.

def cal_view(request):
    import calendar
    c = calendar.TextCalendar(calendar.SUNDAY)
    today = dt.today() # this needs to be updated to use a parameter
    dates = [(d, dt.strftime(dt(d[0], d[1], d[2]), '%Y-%m-%d')) for d in c.itermonthdays4(today.year, today.month)] # this needs to be updated to use a parameter
    today_str = dt.strftime(today, '%Y-%m-%d')
    context = {"today": today, 
                "today_str": today_str,
                "dates": dates}
    return render(request, 'cal/calendar.html', context)
