from django.shortcuts import render


def index(request):
    '''Main_page view'''
    return render(request, 'index.html')


def faq(request):
    '''FAQ view'''
    return render(request, 'faq.html')


def boxes(request):
    '''Boxes view'''
    return render(request, 'boxes.html')


def my_rent(request):
    '''My rent view'''
    return render(request, 'my-rent.html')
