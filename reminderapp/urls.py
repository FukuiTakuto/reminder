from django.urls import path
from .views import calendardef,add_event

app_name = "reminderapp"

urlpatterns = [
    path("calendar/",calendardef,name="calendar"),
    path("add/",add_event,name="add_event"),
]
