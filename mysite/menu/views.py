from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.utils.timezone import localtime, now
from datetime import datetime
from operator import attrgetter
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from .models import *
from .forms import *


def menu_list(request):
    # original time 266 queries in 40 - 60ms
    past = now() - timedelta(days=365 * 6)

    # new time 2 queries in 5-7ms
    menus = Menu.objects.filter(
        Q(expiration_date__gte=past) |
        Q(expiration_date__isnull=True)).order_by(
        'expiration_date').prefetch_related('items')

    # menus = sorted(menus, key=attrgetter('expiration_date'))
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    menu = Menu.objects.prefetch_related('items').get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try:
        item = Item.objects.select_related('chef').get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def edit_menu(request, pk=None):
    # edit and create menu merged in view
    menu = None
    if pk:
        menu = get_object_or_404(Menu.objects.prefetch_related('items'), pk=pk)

    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            # manytomany not saved if you use commit=False
            form.save_m2m()
            return redirect('menu:menu_detail', pk=menu.pk)
    else:
        form = MenuForm(instance=menu)
    return render(request, 'menu/menu_edit.html', {'form': form})
