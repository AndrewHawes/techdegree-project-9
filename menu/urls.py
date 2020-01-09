from django.urls import path
from menu import views

urlpatterns = [
    path('', views.MenuList.as_view(), name='menu_list'),
    path('menu/<int:pk>/', views.MenuDetail.as_view(), name='menu_detail'),
    path('menu/new/', views.MenuCreate.as_view(), name='menu_new'),
    path('menu/<int:pk>/edit/', views.MenuEdit.as_view(), name='menu_edit'),
    path('menu/item/<int:pk>/', views.ItemDetail.as_view(), name='item_detail'),
    path('menu/item/<int:pk>/edit/', views.ItemEdit.as_view(), name='item_edit')
]


