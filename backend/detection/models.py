from django.db import models


# Create your models here.
class Detection(models.Model) :

    class Status(models.TextChoices):
        PENDING = "pending"
        PROCESSING = "processing"
        COMPLETED = "completed"
        FAILED = "failed"

    class MediaTypes(models.TextChoices):
        IMAGE = 'image'
        VIDEO = 'video'

    file = models.FileField(upload_to="road_media/")
    media_type = models.CharField(
        max_length=20, 
        choices=MediaTypes, 
    )
    latitude = models.FloatField(null=True, blank=True) #validators?+-90
    longitude = models.FloatField(null=True, blank=True) #validators?+-180
    status = models.CharField(
        max_length=20, 
        choices=Status, 
        default=Status.PENDING
    )
    risk_score = models.FloatField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    image_width = models.PositiveIntegerField(null=True, blank=True)
    image_height = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



class Hazard(models.Model):
    detection = models.ForeignKey(Detection, on_delete=models.CASCADE, related_name="hazards")
    hazard_type = models.CharField(max_length=50)
    confidence = models.FloatField()
    x1 = models.FloatField()
    y1 = models.FloatField()
    x2 = models.FloatField()
    y2 = models.FloatField()
    frame_number = models.PositiveIntegerField(null=True, blank=True)  # only for video



