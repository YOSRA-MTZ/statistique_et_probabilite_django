from django.shortcuts import render

# Create your views here.
def index(request):
        return render(request, 'index.html')

def excel(request):
        return render(request, 'excel.html')

def text(request):
        return render(request, 'excel.html')

def csv(request):
        return render(request, 'excel.html')

def url(request):
        return render(request, 'excel.html')