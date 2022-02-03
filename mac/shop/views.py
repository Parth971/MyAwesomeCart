from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Product, Contact, Order, OrderUpdate
from paytm import Checksum

import json
import datetime

MERCHANT_KEY = "N@kHquL4QGuS4L0m"

# Create your views here.


def index(request):
    allProds = []
    category_product = Product.objects.values("category", "product_id")

    categories = set([cat_dic["category"] for cat_dic in category_product])

    for category in categories:
        products = Product.objects.filter(category=category)
        n = len(products)
        nSlides = n // 4 + (n % 4 != 0)

        if n != 0:
            allProds.append([products, nSlides, range(1, nSlides), category])
    params = {"allProds": allProds}

    return render(request, "shop/index.html", params)


def match(query, item):
    if (
        query.lower() in item.product_name.lower()
        or query in item.desc.lower()
        or query in item.category.lower()
        or query in item.subcategory.lower()
    ):
        return True
    return False


def search(request):
    query = request.GET.get("search")
    allProds = []
    category_product = Product.objects.values("category", "product_id")

    categories = set([cat_dic["category"] for cat_dic in category_product])

    for category in categories:
        products = Product.objects.filter(category=category)
        prod = [item for item in products if match(query, item)]
        n = len(prod)
        nSlides = n // 4 + (n % 4 != 0)

        if n != 0:
            allProds.append([prod, nSlides, range(1, nSlides), category])
    params = {"allProds": allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {"msg": "Please enter relevent search"}
    return render(request, "shop/search.html", params)


def about(request):
    return render(request, "shop/about.html")


def contact(request):
    params = {}
    if request.method == "POST":
        name = request.POST.get("userName")
        email = request.POST.get("userEmail")
        phone = request.POST.get("userPhone")
        desc = request.POST.get("desc")
        contact = Contact(user_name=name, user_email=email, user_phone=phone, desc=desc)
        contact.save()
        params["success"] = 1
    return render(request, "shop/contact.html", params)


def tracker(request):
    params = {}
    if request.method == "POST":
        order_id = request.POST.get("orderId")
        email = request.POST.get("email")
        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    str_date = str(item.timestamp)
                    date = datetime.date(
                        int(str_date[:4]), int(str_date[5:7]), int(str_date[8:])
                    )
                    time = date.ctime()
                    updates.append(
                        {
                            "text": item.update_desc,
                            "time": time[:3] + ", " + time[4:10] + " " + time[-4:],
                        }
                    )
                response = json.dumps(
                    {
                        "status": "success",
                        "updates": updates,
                        "itemsJson": order[0].items_json,
                    },
                    default=str,
                )
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "empty list"}')
        except Exception as e:
            return HttpResponse('{"status": "error"}')

    return render(request, "shop/tracker.html")


def productView(request, myid):
    product = Product.objects.filter(product_id=myid)[0]
    params = {"product": product}
    return render(request, "shop/productView.html", params)


def checkout(request):

    if request.method == "POST":
        items_json = request.POST.get("items_json")
        amount = request.POST.get("totalAmount")
        name = request.POST.get("name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip")

        order = Order(
            name=name,
            total_amount=amount,
            email=email,
            address=address,
            phone=phone,
            city=city,
            state=state,
            zip_code=zip_code,
            items_json=items_json,
        )
        order.save()

        order_update = OrderUpdate(
            order_id=order.order_id, update_desc="Order Inialized, Placed"
        )
        order_update.save()
        params = {"success": 1, "order_id": order.order_id}
        # return render(request, "shop/checkout.html", params)
        # Request paytm to transfer amount  to your account

        param_dict = {
            "MID": "IZpcUt85895021284107",
            "ORDER_ID": str(order.order_id),
            "TXN_AMOUNT": str(amount),  # use str(amount) instead
            "CUST_ID": email,
            "INDUSTRY_TYPE_ID": "Retail",
            "WEBSITE": "WEBSTAGING",
            "CHANNEL_ID": "WEB",
            "CALLBACK_URL": "http://127.0.0.1:8000/shop/handlerequest/",
        }
        param_dict["CHECKSUMHASH"] = Checksum.generateSignature(
            param_dict, MERCHANT_KEY
        )
        return render(request, "shop/paytm.html", {"param_dict": param_dict})
    return render(request, "shop/checkout.html")


@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == "CHECKSUMHASH":
            checksum = form[i]

    verify = Checksum.verifySignature(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict["RESPCODE"] == "01":
            print("order successful")
        else:
            print("order was not successful because" + response_dict["RESPMSG"])
    return render(request, "shop/paymentstatus.html", {"response": response_dict})
