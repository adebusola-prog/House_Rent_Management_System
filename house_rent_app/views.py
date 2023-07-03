from django.shortcuts import render
from accounts.serializers import HouseOwnerSerializer
from accounts.models import HouseOwner
from accounts.permissions import IsAdminOrReadOnly
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
# Create your views here.

class HouseOwnerListCreateAPIView(IsAdminOrReadOnly, ListCreateAPIView):
    serializer_class = HouseOwnerSerializer
    queryset = HouseOwner.objects.all()

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['request'] = self.request
    #     return context

    # def perform_create(self, serializer):
    #     serializer.save()


class HouseOwnerRetreiveUpdateAPIView(IsAdminOrReadOnly, RetrieveUpdateAPIView):
    serializer_class = HouseOwnerSerializer
    queryset = HouseOwner.objects.all()

    


# class HouseOwnerListing(ListAPIView):
#     serializer_class = HouseOwnerListingSerializer

