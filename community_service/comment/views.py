from django.shortcuts import render

def comment(request):
    return render(request, 'comment.html')
