from rest_framework import serializers
from .models import Detection, Hazard
from .services.pipeline import IMAGE_EXT, VIDEO_EXT

class HazardSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Hazard
        fields = "__all__"

class DetectionSerializer(serializers.ModelSerializer):
    
    class Meta : 
        model = Detection
        fields = "__all__"

    #file error handle function 