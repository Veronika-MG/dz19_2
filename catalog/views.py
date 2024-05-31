from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.forms import VersionForm, ProductForm
from catalog.models import Category, Product, Version


def home(request):
    return render(request, 'catalog/home.html')


def index(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Магазин - Продукты'
    }
    return render(request, 'catalog/index.html', context)

@login_required
def categories(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Магазин - Категории'
    }
    return render(request, 'catalog/categories.html', context)

@login_required
def category_products(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(category_id=pk),
        'title': f'Продукты категории "{category_item.name}"'
    }
    return render(request, 'catalog/products.html', context)

class ProductListView(LoginRequiredMixin, ListView):
    """Класс для вывода списка продуктов"""
    model = Product
    template_name = 'catalog/products.html'
    extra_context = {"title": "Продукты"}

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["Продукты"] = Product.objects.all()
    #     context["title"] = "Продукты"
    #     return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Класс для вывода информации о продукте по его pk"""
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.model.objects.filter(pk=self.kwargs.get('pk'))
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

class ProductCreateView(LoginRequiredMixin, CreateView):
    """ Класс для создания продукта. """
    model = Product
    form_class = ProductForm
    # fields = ('name', 'description', 'category', 'price', 'date_of_creation', 'image')
    success_url = reverse_lazy('catalog:products')
    def form_valid(self, form):
        product = form.save(commit=False)
        product.user = self.request.user
        product.save()
        return redirect(self.success_url)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """ Класс для редактирования продукта. """
    model = Product
    fields = ('name', 'description', 'category', 'price', 'date_of_creation', 'image')
    success_url = reverse_lazy('catalog:products')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """ Класс для удаления продукта. """
    model = Product
    success_url = reverse_lazy('catalog:products')


class VersionListView(LoginRequiredMixin, ListView):
    """Класс для вывода списка версий определенного продукта"""
    model = Version
    extra_context = {"title": "Версии"}

    def get_queryset(self, *args, **kwargs):
        return Version.objects.filter(product=Product.objects.get(pk=self.kwargs.get('pk')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(object_list=object_list, **kwargs)
        context_data['pk'] = self.kwargs.get('pk')
        # context_data['object_list'] = self.model.objects.filter(pk=self.kwargs.get('pk'))
        return context_data

class VersionCreateView(LoginRequiredMixin, CreateView):
    """Класс для создания версии"""
    model = Version
    form_class = VersionForm
    # success_url = reverse_lazy('catalog:versions')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.initial = {'product': Product.objects.get(pk=self.kwargs.get('pk'))}
        return form

    def get_success_url(self):
        return reverse('catalog:versions', kwargs={'pk': self.object.product.pk})

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.product = Product.objects.get(pk=self.kwargs.get('pk'))
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())

class VersionUpdateView(LoginRequiredMixin, UpdateView):
    """Класс для редактирования версии. """
    model = Version
    form_class = VersionForm
    # success_url = reverse_lazy('catalog:versions')
    def get_success_url(self):
        return reverse('catalog:versions', kwargs={'pk': self.object.product.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.product.pk
        return context

class VersionDetailView(LoginRequiredMixin, DetailView):
    """ Класс для вывода информации о версии по его pk"""
    model = Version

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.product.pk
        return context

class VersionDeleteView(LoginRequiredMixin, DeleteView):
    """Класс для удаления версии"""
    model = Version
    # success_url = reverse_lazy('catalog:versions')

    def get_success_url(self):
        return reverse('catalog:versions', kwargs={'pk': self.object.product.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.product.pk
        return context
