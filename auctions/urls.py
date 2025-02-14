from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("active/", views.active_listings, name="active_listings"),
    path("create/", views.create_listing, name="create_listing"),
    path('listing/<int:listing_id>/', views.listing_page, name='listing_page'),
    path('listing/<int:listing_id>/watchlist/', views.update_watchlist, name='update_watchlist'),
    path("watchlist/", views.watchlist_view, name="watchlist"),
    path('listing/<int:listing_id>/bid/', views.place_bid, name='place_bid'),
    path('listing/<int:listing_id>/close/', views.close_auction, name='close_auction'),
    path('listing/<int:listing_id>/comment/', views.add_comment, name='add_comment'),
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/<str:category_name>/', views.category_listings, name='category_listings'),
    
]


