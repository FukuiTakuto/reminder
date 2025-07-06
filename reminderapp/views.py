import json
import time
from django.template import loader
from django.http import Http404,HttpResponse,JsonResponse
from django.middleware.csrf import get_token
from .forms import EventForm,CalendarForm
from .models import EventModel

def calendardef(request):
    get_token(request)
    template = loader.get_template("calendar.html")
    return HttpResponse(template.render())
    
def add_event(request):
    if request.method == "GET":
        raise Http404()
    
    datas = json.loads(request.body)
    
    eventForm = EventForm(datas)
    if not eventForm.is_valid():
        raise Http404()
    
    start_date = datas["start_date"]
    end_date = datas["end_date"]
    event_name = datas["event_name"]
    
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))
    
    event = EventModel(
        event_name = str(event_name),
        start_date = formatted_start_date,
        end_date = formatted_end_date,
    )
    event.save()
    
    return HttpResponse("")

def get_events(request):
    if request.method == "GET":
        raise Http404()
    
    datas = json.loads(request.body)
    
    calendarForm = CalendarForm(datas)
    if not calendarForm.is_valid:
        raise Http404()
    
    start_date = datas["start_date"]
    end_date = datas["end_date"]
    
    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start_date / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(end_date / 1000))
    
    events = EventModel.objects.filter(
        start_date__lt=formatted_end_date, end_date__gt=formatted_start_date
    )
    
    event_list = []
    for event in events:
        event_list.append(
            {
                "title" : event.event_name,
                "start" : event.start_date,
                "end" : event.end_date,
            }
        )
    
    return JsonResponse(event_list,safe=False)