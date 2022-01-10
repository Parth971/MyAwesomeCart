from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render

from .models import Product

# Create your views here.
def index(request):
    allProds = []
    category_product = Product.objects.values("category", "id")
    # print(category_product)

    categories = set([cat_dic["category"] for cat_dic in category_product])
    # print(categories)
    for category in categories:
        products = Product.objects.filter(category=category)
        n = len(products)
        nSlides = n // 4 + (n % 4 != 0)

        if n != 0:
            allProds.append([products, nSlides, range(1, nSlides), category])
            print(
                f"\n\ncategory: {category}\n products: {products}\nnSlides: {nSlides} "
            )
    params = {"allProds": allProds}

    return render(request, "shop/index.html", params)


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    return render(request, "shop/contact.html")


def tracker(request):
    return render(request, "shop/tracker.html")


def search(request):
    return render(request, "shop/search.html")


def productView(request):
    return render(request, "shop/productView.html")


def checkout(request):
    return render(request, "shop/checkout.html")
