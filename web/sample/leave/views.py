from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.
def apply_leave(request):
    return HttpResponse("Apply Leave")

def leave(request):
    return HttpResponse("<button>apply leave</button><button>apply leave</button> ")

def status(request):
    return HttpResponse("<h1>Leave Status</h1>")

def personal_info(request):
    persons = [
        {"name":"Hello","dep":"cde"}
    ]
    render()