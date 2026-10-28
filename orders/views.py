from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST

from cart.models import Cart
from catalog.models import Product
from .models import Order, OrderItem


@login_required
@require_http_methods(["GET", "POST"])
def checkout(request):
    cart = Cart.objects.filter(
        user=request.user,
    ).first()

    if cart is None:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:cart_detail")

    cart_items = list(
        cart.items.select_related(
            "product",
            "product__store",
        ).all()
    )

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:cart_detail")

    total_price = sum(
        (item.total_price for item in cart_items),
        start=0,
    )

    if request.method == "POST":
        shipping_address = request.POST.get(
            "shipping_address", ""
        ).strip()
        customer_note = request.POST.get(
            "customer_note", ""
        ).strip()

        if not shipping_address:
            messages.error(
                request,
                "Please enter a shipping address.",
            )
            return render(
                request,
                "orders/checkout.html",
                {
                    "items": cart_items,
                    "total_price": total_price,
                },
            )

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    shipping_address=shipping_address,
                    customer_note=customer_note,
                )

                for cart_item in cart_items:
                    product = Product.objects.select_for_update().get(
                        pk=cart_item.product_id,
                    )

                    if not product.is_active:
                        raise ValueError(
                            f"{product.name} is no longer available."
                        )

                    if product.quantity < cart_item.quantity:
                        raise ValueError(
                            f"Not enough stock for {product.name}."
                        )

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        store=product.store,
                        product_name=product.name,
                        store_name=product.store.name,
                        price=product.price,
                        quantity=cart_item.quantity,
                    )

                    product.quantity -= cart_item.quantity
                    product.save(update_fields=["quantity"])

                cart.items.all().delete()

        except ValueError as error:
            messages.error(request, str(error))
            return redirect("cart:cart_detail")

        return redirect(
            "orders:order_detail",
            order_id=order.pk,
        )

    return render(
        request,
        "orders/checkout.html",
        {
            "items": cart_items,
            "total_price": total_price,
        },
    )

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items"),
        pk=order_id,
        user=request.user,
    )

    return render(
        request,
        "orders/order_detail.html",
        {"order": order},
    )

@login_required
@require_POST
def simulate_payment(request, order_id):
    order = get_object_or_404(
        Order,
        pk=order_id,
        user=request.user,
    )

    if order.payment_status == Order.PaymentStatus.PAID:
        messages.info(request, "This order has already been paid.")
    else:
        order.payment_status = Order.PaymentStatus.PAID
        order.save(update_fields=["payment_status"])
        messages.success(
            request,
            "Payment successful! This was a demo payment.",
        )

    return redirect("orders:order_detail", order_id=order.pk)