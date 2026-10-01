from django.shortcuts import render
from detection.models import Detection
from rest_framework import viewsets
from detection.serializers import DetectionSerializer, HazardSerializer
from detection.services.pipeline import process_detection

#for stats and map endpt.
from django.db.models import Count, Avg
from rest_framework.decorators import api_view
from rest_framework.response import Response
from detection.models import Hazard

from rest_framework.decorators import action





# Create your views here.

class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all() 
    serializer_class = DetectionSerializer
    http_method_names = ["get", "post", "delete"]


    def perform_create(self, serializer) : 
        detection = serializer.save()
        process_detection(detection)


    @action(methods=['get'], detail=False)
    def map(self, request):
        qs = (
            Detection.objects
            .filter(
                status="completed",


                ##UNCOMMENT THESE WHEN YOU GET LAT, LONG DATA
                # latitude__isnull=False,
                # longitude__isnull=False,

                
            )
            .prefetch_related("hazards")
        )

        return Response([
            {
                "detection_id": d.id,
                "latitude": d.latitude,
                "longitude": d.longitude,
                "risk_score": d.risk_score,
                "hazard_types": sorted({
                    h.hazard_type
                    for h in d.hazards.all()
                }),
            }
            for d in qs
        ])



#stats endpt
@api_view(["GET"])
def stats(request):
    done = Detection.objects.filter(status="completed")
    counts = Hazard.objects.values("hazard_type").annotate(n=Count("id"))
    return Response({
        "total_detections": done.count(),
        "average_risk": round(done.aggregate(a=Avg("risk_score"))["a"] or 0, 1),
        "high_risk_count": done.filter(risk_score__gte=70).count(),
        "hazard_counts": {c["hazard_type"]: c["n"] for c in counts},
    })