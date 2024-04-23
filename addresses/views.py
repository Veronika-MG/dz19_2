from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from addresses.models import Address


class AddressCreateView(CreateView):
    model = Address
    fields = ('title', 'location', 'date_of_creation', 'is_published', 'image')
    success_url = reverse_lazy('addresses:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

class AddressUpdateView(UpdateView):
    model = Address
    fields = ('title', 'location', 'image', 'date_of_creation', 'is_published')
    # success_url = reverse_lazy('addresses:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('addresses:view', args=[self.kwargs.get('pk')])

class AddressListView(ListView):
    model = Address
    extra_context = {"title": "Адреса магазинов"}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=False)
        return queryset

class AddressDetailView(DetailView):
    model = Address

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

class AddressDeleteView(DeleteView):
    model = Address
    success_url = reverse_lazy('addresses:list')


def toggle_activity(request, pk):
    address_item = get_object_or_404(Address, pk=pk)
    if address_item.is_published:
        address_item.is_published = False
    else:
        address_item.is_published = True

    address_item.save()

    return redirect(reverse('addresses:list'))
