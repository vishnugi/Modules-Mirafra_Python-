from django.shortcuts import render, redirect

def home(request):

    leaves = request.session.get('leaves', [])
    return render(request, 'home.html', {'leaves': leaves})

def apply_leave(request):

    if request.method == "POST":
        name = request.POST.get('name')
        date = request.POST.get('date')
        

        leave = {
            'name': name,
            'date': date,
        }

        leaves = request.session.get('leaves', [])
        leaves.append(leave)
        request.session['leaves'] = leaves

        return redirect('home')

    return render(request, 'apply_leave.html')