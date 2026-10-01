from PIL import Image
from .yolo import run_detection
from .risk import calculate_risk
from ..models import Hazard

IMAGE_EXT = {"jpg", "jpeg", "png"}
VIDEO_EXT = {"mp4", "avi", "mov"}

def process_detection(detection):
    detection.status = "processing"
    detection.save(update_fields=["status"])
    try:
        ext = detection.file.name.rsplit(".", 1)[-1].lower()
        if ext in IMAGE_EXT:
            detection.media_type = "image"
            detection.image_width, detection.image_height = Image.open(detection.file.path).size
            found = [dict(h, frame_number=None) for h in run_detection(detection.file.path)]
        else:
            raise ValueError("Video not supported yet")   # replaced in Step 8

        Hazard.objects.bulk_create([Hazard(detection=detection, **h) for h in found])
        detection.risk_score = calculate_risk(found)
        detection.status = "completed"
    except Exception as e:
        detection.status = "failed"
        detection.error_message = str(e)
    detection.save()