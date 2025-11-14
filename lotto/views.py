from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'lotto/index.html')

def my_tickets(request):
    return render(request, 'lotto/my_tickets.html')