from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from menu.forms import MenuForm, ItemForm
from menu.models import Menu, Item


class MenuList(ListView):
    model = Menu
    context_object_name = 'menus'
    template_name = 'menu/index.html'

    def get_queryset(self):
        return Menu.active_menus.all().order_by('-created_date')


class MenuDetail(DetailView):
    model = Menu
    context_object_name = 'menu'
    template_name = 'menu/generic_detail.html'
    extra_context = {'partial_template_name': 'menu/partials/menu.html'}


class MenuCreate(LoginRequiredMixin, CreateView):
    model = Menu
    form_class = MenuForm
    template_name = 'menu/generic_form.html'
    extra_context = {'page_heading': 'New Menu'}


class MenuEdit(LoginRequiredMixin, UpdateView):
    model = Menu
    form_class = MenuForm
    template_name = 'menu/generic_form.html'
    extra_context = {'page_heading': 'Edit Menu'}


class ItemDetail(DetailView):
    model = Item
    context_object_name = 'item'
    template_name = 'menu/generic_detail.html'
    extra_context = {'partial_template_name': 'menu/partials/item.html'}

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('chef')
            .only('name', 'description', 'standard', 'chef__username')
        )


class ItemEdit(LoginRequiredMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'menu/generic_form.html'
    extra_context = {'page_heading': 'Edit Item'}


