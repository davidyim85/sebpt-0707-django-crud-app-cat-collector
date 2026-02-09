from django.urls import path
from . import views  # Import views to connect routes to view functions

urlpatterns = [
    # Routes will be added here
    path("", views.Home.as_view(), name="home"),
    path("about/", views.about, name="about"),
    # route for cats index
    path("cats/", views.cat_index, name="cat-index"),
    path("cats/<int:cat_id>/", views.cat_detail, name="cat-detail"),
    # new route used to create a cat
    path("cats/create/", views.CatCreate.as_view(), name="cat-create"),
    # Add the new routes below
    path("cats/<int:pk>/update/", views.CatUpdate.as_view(), name="cat-update"),
    path("cats/<int:pk>/delete/", views.CatDelete.as_view(), name="cat-delete"),
    path("cats/<int:cat_id>/add-feeding/", views.add_feeding, name="add-feeding"),
    path("toys/create/", views.ToyCreate.as_view(), name="toy-create"),
    path("toys/<int:pk>/", views.ToyDetail.as_view(), name="toy-detail"),
    path("toys/", views.ToyList.as_view(), name="toy-index"),
    #Existing urls above
    path('toys/<int:pk>/update/', views.ToyUpdate.as_view(), name='toy-update'),
    path('toys/<int:pk>/delete/', views.ToyDelete.as_view(), name='toy-delete'),
    path('cats/<int:cat_id>/associate-toy/<int:toy_id>/', views.associate_toy, name='associate-toy'),
    path('cats/<int:cat_id>/remove-toy/<int:toy_id>/', views.remove_toy, name='remove-toy'),
    path('accounts/signup/', views.signup, name='signup'),
]
