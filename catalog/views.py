from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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
        'title': f'Продукты категории "{category_item.name}"'
    }
    return render(request, 'catalog/products.html', context)

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/products.html'
    extra_context = {"title": "Продукты"}

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["Продукты"] = Product.objects.all()
    #     context["title"] = "Продукты"
    #     return context


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context

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

class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'description', 'category', 'price', 'date_of_creation', 'image')
    success_url = reverse_lazy('catalog:products')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name', 'description', 'category', 'price', 'date_of_creation', 'image')
    success_url = reverse_lazy('catalog:products')

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')

