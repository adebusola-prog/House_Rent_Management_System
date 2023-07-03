from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import HouseOwnerListCreateAPIView, HouseOwnerRetreiveUpdateAPIView

app_name = "rent_app"

urlpatterns = [
    path('house_owner_list_create', HouseOwnerListCreateAPIView.as_view(), \
        name = "house_owner_list_create"),
    path('<int:pk>/house_owner_detail_update', HouseOwnerRetreiveUpdateAPIView.as_view(), \
        name = "house_owner_retreive_update"),
    
    
]
urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

