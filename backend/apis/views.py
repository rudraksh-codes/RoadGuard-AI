from django.shortcuts import render
from detection.models import Detection
from rest_framework import viewsets
from detection.serializers import DetectionSerializer, HazardSerializer
from detection.services.pipeline import process_detection

# Create your views here.

class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all() 
    serializer_class = DetectionSerializer
    http_method_names = ["get", "post", "delete"]


    def perform_create(self, serializer) : 
        detection = serializer.save()
        process_detection(detection)
