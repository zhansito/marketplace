from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from catalog.models import Product
from .models import Cart, CartItem


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user,
    )

    items = cart.items.select_related(
        "product",
        "product__store",
    ).all()

    total_price = sum(
        (item.total_price for item in items),
        start=0,
    )

    context = {
        "cart": cart,
        "items": items,
        "total_price": total_price,
    }

    return render(
        request,
        "cart/cart_detail.html",
        context,
    )


@login_required
def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("cart:cart_detail")

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
    )

    if product.quantity < 1:
        messages.error(
            request,
            "This product is out of stock.",
        )
        return redirect("cart:cart_detail")

    cart, created = Cart.objects.get_or_create(
        user=request.user,
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": 1},
    )

    if not created:
        if cart_item.quantity >= product.quantity:
            messages.error(
                request,
                "Not enough stock for this product.",
            )
            return redirect("cart:cart_detail")

        cart_item.quantity += 1

    cart_item.save()

    messages.success(
        request,
        "Product added to your cart.",
    )

    return redirect("cart:cart_detail")


@login_required
def update_cart_item(request, item_id):
    if request.method != "POST":
        return redirect("cart:cart_detail")

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user,
    )

    try:
        quantity = int(request.POST.get("quantity", ""))
    except (TypeError, ValueError):
        messages.error(
            request,
            "Please enter a valid quantity.",
        )
        return redirect("cart:cart_detail")

    if quantity < 1:
        messages.error(
            request,
            "Quantity must be at least 1.",
        )
        return redirect("cart:cart_detail")

    if quantity > cart_item.product.quantity:
        messages.error(
            request,
            "Not enough stock for this product.",
        )
        return redirect("cart:cart_detail")

    cart_item.quantity = quantity
    cart_item.save()

    messages.success(
        request,
        "Cart quantity updated",
    )

    return redirect("cart:cart_detail")


@login_required
def remove_from_cart(request, item_id):
    if request.method != "POST":
        return redirect("cart:cart_detail")

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user,
    )

    cart_item.delete()

    messages.success(
        request,
        "Product removed from your cart.",
    )

    return redirect("cart:cart_detail")