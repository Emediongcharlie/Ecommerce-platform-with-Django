from django.db import router
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from store import views
from django.urls import path, include

route = DefaultRouter()
route.register("collections", views.CollectionViewSet, "collections")
route.register("products", views.ProductViewSet, "products")
# route.register('cartitems', views.CartItemViewSet, 'cartitems')
route.register('carts', views.CartViewSet, 'carts')
route.register('orders', views.OrderViewSet, 'orders')

# products/1/reviews

product_router = NestedDefaultRouter(route, 'products', lookup='product')
product_router.register('reviews', views.ReviewViewSet, basename='product-review')

cart_item_router = NestedDefaultRouter(route, 'carts', lookup='cart')
cart_item_router.register('items', views.CartItemViewSet, 'cart-item')


urlpatterns = route.urls + product_router.urls + cart_item_router.urls



# [
#
# path('', include(route.urls)),
# path('', include(product_router.urls)),

# path('products', views.products, name='products'),
# path('products', views.ProductListAPIView.as_view()),

# path('product/<int:pk>/', views.product, name='product'),
# path('product/<int:pk>/', views.ProductDetailAPIView.as_view()),

# path('collection/<int:pk>/', views.CollectionDetailView.as_view()),

# path('collections', views.collections, name='collections')
# path('collections', views.CollectionListView.as_view())

# ]
