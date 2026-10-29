from pickle import NONE
from django.contrib import messages
from django.db import transaction
from django.db.models import Avg, Count
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from reviews.forms import ProductReviewForm


def product_list(request):
    products = Product.objects.filter(
        is_active=True,
    ).select_related(
        "store",
        "category",
    ).annotate(
        average_rating=Avg("reviews__rating"),
        review_count=Count("reviews"),
    )

    context = {
        "products": products,
    }

    return render(
        request,
        "catalog/product_list.html",
        context,
    )



def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related(
            "store",
            "category",
        ).prefetch_related("images"),
        slug=slug,
        is_active=True,
    )

    user_review = None

    if request.user.is_authenticated:
        user_review = product.reviews.filter(
            user=request.user,
        ).first()

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(
                request,
                "Please log in to write a review.",
            )
            return redirect("users:login")

        form = ProductReviewForm(
            request.POST,
            instance=user_review,
        )

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()

            messages.success(
                request,
                "Your review has been saved successfully!",
            )

            return redirect(
                "catalog:product_detail",
                slug=product.slug,
            )
    else:
        form = ProductReviewForm(instance=user_review)

    reviews = product.reviews.select_related(
        "user"
    ).all()

    rating_stats = product.reviews.aggregate(
        average_rating=Avg("rating"),
        review_count=Count("id"),
    )

    context = {
        "product": product,
        "reviews": reviews,
        "average_rating": rating_stats["average_rating"],
        "review_count": rating_stats["review_count"],
        "user_review": user_review,
        "review_form": form,
    }

    return render(
        request,
        "catalog/product_detail.html",
        context,
    )