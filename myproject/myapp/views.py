# ice_cream/views.py
from django.http import HttpResponse


# Главная страница
def index(request):    
    return HttpResponse('Главная страница')


'''
# Страница со списком мороженого
def icecream_list(request):
    return HttpResponse('Список мороженого')


# Страница с информацией об одном сорте мороженого;
# view-функция принимает параметр pk из path()
def icecream_detail(request, pk):
    return HttpResponse(f'Мороженое номер {pk}')
'''
