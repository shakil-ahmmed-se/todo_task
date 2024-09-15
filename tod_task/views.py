from django.http import HttpResponse

def Home(req):
    return HttpResponse("Welcome to Work notes Server")