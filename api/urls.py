from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('products/', views.ProductListCreateApiView.as_view()),
    path('products/info/', views.ProductInfoApiView.as_view()),
    path('products/<int:id>/', views.ProductDetailApiView.as_view(), name='product-detail'),
    path('users/', views.UserInfoApiView.as_view()),
    # path('orders/', views.OrderListApiView.as_view()),
    # path('user-orders/', views.UserOrderListApiView.as_view(), name='user-orders'),
]

router = DefaultRouter()
router.register('orders', views.OrderViewSet)
urlpatterns += router.urls
