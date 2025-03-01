from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.
from django.shortcuts import redirect, render
from django.http import HttpResponse

# Index view
def Index(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        return redirect('room', room_name=room_name)
    return render(request, 'index.html')

# Chat room view
def Chatspace(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })

