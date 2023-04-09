from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<str:name>", views.listing, name="listing"),
    path("category", views.category, name="category"),
    path('category/<int:id>', views.c_listings, name="c_listings"),
    path('watchlist', views.watchlist, name="watchlist"),
]
