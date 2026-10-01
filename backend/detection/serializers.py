from rest_framework import serializers
from .models import Detection, Hazard
from .services.pipeline import IMAGE_EXT, VIDEO_EXT

class HazardSerializer(serializers.ModelSerializer):

    class Meta : 
        model = Hazard
        fields = "__all__"

class DetectionSerializer(serializers.ModelSerializer):
    hazards = HazardSerializer(many=True, read_only = True)
    class Meta : 
        model = Detection
        fields = "__all__"

        read_only_fields = [
            "id",
            "media_type",
            "status",
            "error_message",
            "risk_score",
            "image_width",
            "image_height",
            "created_at",
            "hazards",
        ]


    #file error handle function 