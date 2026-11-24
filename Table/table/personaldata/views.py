from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import PersonForm
from .models import Person

def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm()

    return render(request, 'add_person.html', {'form': form})


def person_list(request):
    persons = Person.objects.all()
    return render(request, 'person_list.html', {'persons': persons})