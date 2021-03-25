from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import NewItemForm, NewStorage, NewStorageLocation, SearchUsersForm
from .models import User, Category, Location, Item, StorageType, Household_request
from django.http.response import JsonResponse
import logging
import json

from django import forms


from django.db.models import Q

logger = logging.getLogger(__name__)


def index(request):

    try:
        current_user = User.objects.get(id=request.user.pk)
    except User.DoesNotExist:
        return render(request, "inventory/login.html")

    user_household = current_user.household.all()
    household_inventory = []
    inventory = Item.objects.filter(owner=int(request.user.pk))
    # Get household's locations and storage
    location = Location.objects.filter(created_by=request.user.pk)
    storage = StorageType.objects.filter(created_by=request.user.pk)
    for x in user_household:
        # logger.error(x)
        user_inventory = Item.objects.filter(owner=int(x.pk))
        household_inventory.extend(user_inventory)
        household_locations = Location.objects.filter(created_by=int(x.pk))
        location = location | household_locations
        household_storage = StorageType.objects.filter(created_by=int(x.pk))
        storage = storage | household_storage
    household_inventory.extend(inventory)

    location.order_by('location')
    storage.order_by('storage_type')

    categories = Category.objects.order_by('category_name')

    numRequests = Household_request.objects.filter(to_user=request.user.pk)
    return render(request, "inventory/index.html", {
        "inventory": household_inventory,
        "categories": categories,
        "location": location,
        "storage": storage,
        "numRequests": numRequests
    })


def user_inventory(request):
    numRequests = Household_request.objects.filter(to_user=request.user.pk)
    user = User.objects.get(pk=int(request.user.pk))
    user_inventory = Item.objects.filter(owner=int(request.user.pk))
    categories = Category.objects.order_by('category_name')

    user_household = user.household.all()
    # Get household's locations and storage
    location = Location.objects.filter(created_by=request.user.pk)
    storage = StorageType.objects.filter(created_by=request.user.pk)
    for x in user_household:
        household_locations = Location.objects.filter(created_by=int(x.pk))
        location = location | household_locations
        household_storage = StorageType.objects.filter(created_by=int(x.pk))
        storage = storage | household_storage
    location.order_by('location')
    storage.order_by('storage_type')

    return render(request, "inventory/user_inventory.html", {
        "user": user,
        "inventory": user_inventory,
        "categories": categories,
        "location": location,
        "storage": storage,
        "numRequests": numRequests
    })


def create_item(request):
    numRequests = Household_request.objects.filter(to_user=request.user.pk)

    user_storage = StorageType.objects.filter(created_by=int(request.user.pk))
    user = User.objects.get(pk=int(request.user.pk))
    user_household = user.household.all()
    for x in user_household:
        temp = StorageType.objects.filter(created_by=int(x.pk))
        user_storage = user_storage | temp

    logger.error(user_storage.order_by('storage_type'))

    NewItemForm.base_fields['stored_in'] = forms.ModelChoiceField(
        queryset=user_storage.order_by('storage_type'), widget=forms.Select(attrs={'class': 'form-control'}))

    if request.method == "POST":
        form = NewItemForm(request.POST)
        if form.is_valid():
            item_name = form.cleaned_data['item_name']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            img = form.cleaned_data['img']
            owner = User.objects.get(pk=int(request.user.pk))
            stored_in = form.cleaned_data['stored_in']
            item = Item(item_name=item_name, description=description, category=category,
                        img=img, owner=owner, stored_in=stored_in)
            item.save()
            return render(request, "inventory/input_item.html", {
                "form": NewItemForm(),

                "numRequests": numRequests,
            })
    return render(request, "inventory/input_item.html", {
        "form": NewItemForm(),

        "numRequests": numRequests,
    })


def create_storage(request):
    numRequests = Household_request.objects.filter(to_user=request.user.pk)
    user = User.objects.get(pk=int(request.user.pk))
    user_locations = Location.objects.filter(created_by=int(request.user.pk))
    NewStorage.base_fields['location'] = forms.ModelChoiceField(
        queryset=user_locations.order_by('location'), widget=forms.Select(attrs={'class': 'form-control'}))
    if request.method == "POST":
        form = NewStorage(request.POST)
        if form.is_valid():
            storage_type = form.cleaned_data["storageType"]
            location = form.cleaned_data["location"]
            notes = form.cleaned_data["notes"]
            created_by = User.objects.get(pk=int(request.user.pk))
            s = StorageType(storage_type=storage_type,
                            location=location, notes=notes, created_by=created_by)
            s.save()
    return render(request, "inventory/create_storage.html", {
        "form": NewStorage(),
        "numRequests": numRequests
    })


def create_location(request):
    numRequests = Household_request.objects.filter(to_user=request.user.pk)
    if request.method == "POST":
        form = NewStorageLocation(request.POST)
        if form.is_valid():
            location = form.cleaned_data["location"]
            created_by = User.objects.get(pk=int(request.user.pk))
            l = Location(location=location, created_by=created_by)
            l.save()
    return render(request, "inventory/create_location.html", {
        "form": NewStorageLocation(),
        "numRequests": numRequests
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "inventory/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "inventory/login.html")


def logout_view(request):
    logout(request)
    return render(request, "inventory/login.html")


def register(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "inventory/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "inventory/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "inventory/register.html")


@csrf_exempt
@login_required
def update_location(request, item_id):
    try:
        item = Item.objects.get(pk=int(item_id))
    except Item.DoesNotExist:
        return JsonResponse({'message': 'The item does not exist'}, status=404)

    if request.method == "PUT":
        i = json.loads(request.body)
        storage = StorageType.objects.get(pk=i['stored_in'])
        item.stored_in = storage
        item.save()

        logger.error(storage)
        valueOfLocation = storage.location.pk
        logger.error(valueOfLocation)
        return JsonResponse({'location': valueOfLocation}, status=200)
    return HttpResponse(status=200)


def search_users(request):
    numRequests = Household_request.objects.filter(to_user=request.user.pk)
    pendingRequests = Household_request.objects.filter(
        from_user=request.user.pk)
    getToUsers = []
    for x in pendingRequests:
        getToUsers.append(x.to_user)
        # logger.error(x.to_user)
    logger.error(getToUsers)

    if request.method == "POST":
        form = SearchUsersForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            logger.error(user)
            try:
                searching = User.objects.filter(username__icontains=user)
                user = User.objects.get(id=request.user.pk)
                user_household = user.household.all()
                return render(request, "inventory/users.html", {
                    "form": SearchUsersForm(),
                    'users': searching,
                    "numRequests": numRequests,
                    "household": user_household,
                    "numRequests": numRequests,
                    "pendingRequests": getToUsers
                })
            except User.DoesNotExist:
                return render(request, "inventory/users.html", {
                    "form": SearchUsersForm(),
                    'message': 'User does not exist',
                    "numRequests": numRequests
                })

            logger.error(searching)

    return render(request, "inventory/users.html", {
        "form": SearchUsersForm(),
        "numRequests": numRequests

    })


@login_required
def send_household_request(request, user_id):
    from_user = request.user
    to_user = User.objects.get(id=user_id)
    household_request, created = Household_request.objects.get_or_create(from_user=from_user,
                                                                         to_user=to_user)

    if created:
        return HttpResponse(status=200)
        # return HttpResponse('household request send')
    else:
        return HttpResponseRedirect(reverse("users"))


@login_required
def accept_household_request(request, request_id):
    household_request = Household_request.objects.get(id=request_id)
    numRequests = Household_request.objects.filter(to_user=request.user.pk)
    if household_request.to_user == request.user:
        household_request.to_user.household.add(household_request.from_user)
        household_request.from_user.household.add(household_request.to_user)
        household_request.delete()
        return render(request, "inventory/requests.html", {
            "numRequests": numRequests
        })
    else:
        return render(request, "inventory/requests.html", {
            "numRequests": numRequests
        })


@login_required
def reject_household_request(request, request_id):
    household_request = Household_request.objects.get(id=request_id)
    numRequests = Household_request.objects.filter(to_user=request.user.pk)
    if household_request.to_user == request.user:
        household_request.to_user.household.remove(household_request.from_user)
        household_request.from_user.household.remove(household_request.to_user)
        household_request.delete()
        return render(request, "inventory/requests.html", {
            "numRequests": numRequests
        })
    else:
        return render(request, "inventory/requests.html", {
            "numRequests": numRequests
        })


@login_required
def remove_from_household(request, user_id):
    user = User.objects.get(id=user_id)
    current_user = User.objects.get(id=request.user.pk)
    current_user.household.remove(user)
    user.household.remove(current_user)
    user_household = current_user.household.all()
    return render(request, "inventory/household.html", {
        "household": user_household
    })


def requests(request):
    numRequests = Household_request.objects.filter(to_user=request.user.pk)

    return render(request, "inventory/requests.html", {

        "numRequests": numRequests
    })


def household(request):
    user = User.objects.get(id=request.user.pk)
    user_household = user.household.all()
    return render(request, "inventory/household.html", {
        "household": user_household
    })


@login_required
def delete_item(request, item_id):
    try:
        item = Item.objects.get(pk=int(item_id))
    except Item.DoesNotExist:
        return JsonResponse({'message': 'The item does not exist.'}, status=404)
    item.delete()
    return HttpResponse(status=200)
