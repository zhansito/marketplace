from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from django.shortcuts import render

from catalog.models import Product


def product_list(request):
    products = Product.objects.filter(
        is_active=True,
    ).select_related(
        "store",
        "category",
    )

    context = {
        "products": products,
    }

    return render(
        request,
        "catalog/product_list.html",
        context,
    )