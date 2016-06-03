from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

testToken = "ABCDEF123456"

@ensure_csrf_cookie
def search(request):
    dict = {}
    if request.method != 'POST':
        dict['error_code'] = 201 
    else:
        dict['error_code'] = 200
        if (request.POST.get('wd', "") != ""):
            ids = [1,4,5,7,6,3]
            dict["ids"] = ids
    return JsonResponse(dict)