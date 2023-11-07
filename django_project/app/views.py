from django.shortcuts import render

# Create your views here.
def index(request):
        return render(request, 'index.html')

def excel(request):
        return render(request, 'excel.html')

def text(request):
        return render(request, 'text.html')

def csv(request):
        return render(request, 'csv.html')

def url(request):
        return render(request, 'url.html')


def image(request):
        return render(request, 'image.html')