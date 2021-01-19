from django.urls import path

from .api_views import CategoryListAPIView, ResistorAPIView, ResistorDetailAPIView, CustomerListAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories_list'),
    path('customers/', CustomerListAPIView.as_view(), name='customers_list'),
    path('resistors/', ResistorAPIView.as_view(), name='resistors_list'),
    path('resistors/<str:id>/', ResistorDetailAPIView.as_view(), name='resistors_detail')
]
