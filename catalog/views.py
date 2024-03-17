from django.shortcuts import render

from catalog.models import Category, Product


def home(request):
    return render(request, 'catalog/home.html')

def index(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Магазин - Продукты'
    }
    return render(request, 'catalog/index.html', context)

def categories(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Магазин - Категории'
    }
    return render(request, 'catalog/categories.html', context)

def category_products(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(category_id=pk),
        'title': f'Продукты категории {category_item.name}'
    }
    return render(request, 'catalog/products.html', context)


def contacts(request):
    context = {
        'title': 'Контакты'
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} {phone}: {message}')
    return render(request, 'catalog/contacts.html', context)
