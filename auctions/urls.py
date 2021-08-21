from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("upload", views.upload, name="upload"),
    path("watch/<int:id>/", views.watch, name='watch'),
    path("watchlist/<int:productid>/", views.watchlist, name='watchlist'),
    path("update", views.update, name="update"),
    path("bids/<int:bidid>/", views.bids, name="bids"),
path("comments/<int:pid>/", views.comments, name="comments"),
path("close/<int:cid>/", views.close, name="close"),
path("win/<str:title>/", views.win, name="win"),
    path("categories/<str:category>", views.filtered, name='filtered'),
    path("categories", views.category, name="category")

]

