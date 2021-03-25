from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_item", views.create_item, name="create_item"),
    path("create_storage", views.create_storage, name="create_storage"),
    path("create_location", views.create_location, name="create_location"),
    path("user_inventory", views.user_inventory, name="user_inventory"),
    path("requests", views.requests, name="requests"),
    path("household", views.household, name="household"),

    # API Routes
    path("update_location/<int:item_id>",
         views.update_location, name="update_location"),
    path("search_users", views.search_users, name="search_users"),
    path('send_household_request/<int:user_id>',
         views.send_household_request, name="send_household_request"),
    path('accept_household_request/<int:request_id>',
         views.accept_household_request, name="accept_household_request"),
    path('reject_household_request/<int:request_id>',
         views.reject_household_request, name="reject_household_request"),
    path('remove_from_household/<int:user_id>', views.remove_from_household,
         name="remove_from_household"),
    path('delete_item/<int:item_id>', views.delete_item, name="delete_item")
]
