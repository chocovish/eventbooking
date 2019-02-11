from django.shortcuts import HttpResponse

def home(request):
    data = 'API located at <a href="/api/">/api/</a>'
    return HttpResponse(data)