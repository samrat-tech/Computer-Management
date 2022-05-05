import json, pytz

from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import Serializer
from django.db import IntegrityError
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import smart_text
from django.views.decorators.csrf import csrf_exempt

from .models import *


class JSONSerializer(Serializer):
    def get_dump_object(self, obj):
        self._current["id"] = smart_text(obj._get_pk_val(), strings_only=True)
        return self._current

def register(request):
    if request.method == "POST":
        full_name = request.POST["full_name"].split(" ")
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=full_name[0], last_name=full_name[-1])
            user.save()
        except IntegrityError:
            return render(request, "inventory/register.html", {
                "message": "Email address is already registered."
            })
        login(request, user)
        return redirect("index")

    return render(request, "inventory/register.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "inventory/login.html", {
                "message": "Invalid credentials."
            })

    return render(request, "inventory/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def index(request):
    return render(request, "inventory/app.html", {
        "item_names": [item.name for item in ComputerItem.objects.all()]
    })

@login_required
def contact(request):
    return render(request, "inventory/contact.html")

@csrf_exempt
@login_required
def app(request, feature):
    if feature == "inventory":
        parts = Part.objects.all()
        return JsonResponse(JSONSerializer().serialize(parts), safe=False)
    elif feature == "computer":
        items = ComputerItem.objects.all()
        return JsonResponse(JSONSerializer().serialize(items), safe=False)
    elif feature == "sales":
        sales = Sale.objects.all().order_by("-timestamp")
        all_sales = []
        for sale in sales:
            all_sales.append({
                "computer_item": sale.computer_item.name,
                "timestamp": f"{datetime.strftime(sale.timestamp, '%b %d, %Y at %I:%M %p %Z')}"
            })
        return JsonResponse(all_sales, safe=False)
    elif feature == "finances":
        sales = Sale.objects.all()
        parts = Part.objects.all()
        revenue = 0
        expenses_item = 0
        expenses = 0
        for sale in sales:
            computer_item = sale.computer_item
            revenue += float(computer_item.price)
            # for part in parts:
                # expenses_item += float(part.unit_price)
        for part in parts:
            expenses += float((part.quantity * part.unit_price))
        profit = float(revenue) - expenses
        return JsonResponse({
                "revenue": "{:,.2f}".format(round(revenue, 2)),
                "profit": "{:,.2f}".format(round(profit, 2)),
                # "expenses_item": "{:,.2f}".format(round(expenses_item, 2)),
                "expenses": "{:,.2f}".format(round(expenses, 2))
            })
    else:
        return JsonResponse({"error": "Invalid app feature."}, status=400)

@login_required
def detailss(request, details_id):
    try:
        item = ComputerItem.objects.get(pk=details_id)
    except ComputerItem.DoesNotExist:
        return JsonResponse({"error": "Invalid request."}, status=400)
    return JsonResponse({
            "details_name": item.name,
            "details_price": item.price,
            "details_image": item.details_image,
            "details_link": item.details_link
        })

@csrf_exempt
@login_required
def new_item(request):
    if request.method == "POST":
        item_name = request.POST["item_name"]
        price = request.POST["price"]
        image_url = request.POST["image_url"]
        details_url = request.POST["details_url"]
        item = ComputerItem.objects.create(name=item_name, price=price, details_image=image_url, details_link=details_url)
        item.save()
        return redirect("index")

@csrf_exempt
@login_required
def new_part(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    part_name = data.get("part_name")
    quantity = data.get("quantity")
    unit_price = data.get("unit_price")
    part = Part.objects.create(name=part_name, quantity=quantity, unit_price=unit_price)
    part.save()
    return JsonResponse({"message": "Part successfully added."}, status=201)

@csrf_exempt
@login_required
def new_sale(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    saled_item = data.get("saled_item")
    date_time = datetime.strptime(data.get("date_time"), "%Y-%m-%dT%H:%M")
    date_time = date_time.replace(tzinfo=pytz.UTC)
    item = get_object_or_404(ComputerItem, name=saled_item)
    sale = Sale.objects.create(user=request.user, computer_item=item, timestamp=date_time)
    sale.save()
    return JsonResponse({"message": "Sale successfully added."}, status=201)

@csrf_exempt
@login_required
def delete_part(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("part_id") is not None:
            part_id = data.get("part_id")
            part = get_object_or_404(Part, pk=part_id)
            if data.get("remove") == True:
                part.delete()
            return JsonResponse({"success": "Part successfully deleted"})
        else:
            return JsonResponse({"error": "Invalid request."}, status=400)

