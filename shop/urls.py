from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('auth/', auth_request, name="login_request"),
    path('login/', LoginView.as_view(), name="login"),
    path('ProtectedView', ProtectedView.as_view(), name="ProtectedView"),
    path('user/info/', UserInfoView.as_view(), name='user-info'),  # Get user info
    path('user/update/', UserUpdateView.as_view(), name='user-update'),  # U
]
