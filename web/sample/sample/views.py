
from django.http import HttpResponse  
from datetime import datetime
from zoneinfo import ZoneInfo

# Get the time in a specific timezone, e.g., 'Asia/Kolkata'
tz_india = ZoneInfo('Asia/Kolkata')
c = datetime.now(tz_india)
c=int(c.strftime("%H"))


def hello(request):
    return HttpResponse("hello,WOrld")

def greet(request):
    if c<12:
        return HttpResponse("good MOrning")
    elif c==12:
        return HttpResponse("good afternoon")
    else:
        return HttpResponse("good evening!!!")


