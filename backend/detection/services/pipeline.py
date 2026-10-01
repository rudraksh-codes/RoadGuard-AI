from PIL import Image
from .yolo import run_detection
from .risk import calculate_risk
from ..models import Hazard


IMAGE_EXT = {"jpg", "jpeg", "png", "webp", "bmp", "tiff", "heic", "heif"}
VIDEO_EXT = {"mp4", "avi", "mov", "mkv", "webm", "m4v", "mpeg", "mpg", "3gp"}

def process_detection(detection):
    detection.status = "processing"
    detection.save(update_fields=["status"])
    try:
        ext = detection.file.name.rsplit(".", 1)[-1].lower()
        if ext in IMAGE_EXT:
            detection.media_type = "image"
            detection.image_width, detection.image_height = Image.open(detection.file.path).size
            found = [dict(h, frame_number=None) for h in run_detection(detection.file.path)]
        
        elif ext in VIDEO_EXT:
            ## REPLACE THE COMMENTED PART (running detection on each frame)
            raise ValueError("Video not supported yet")   
            
            # detection.media_type = "video"
            # found = []
            # for frame_no, frame in extract_frames(detection.file.path):
            #     detection.image_height, detection.image_width = frame.shape[:2]
            #     for h in run_detection(frame):          # run_detection accepts a frame
            #         found.append(dict(h, frame_number=frame_no))

        else : 
            raise ValueError("Unsupported file format")

        Hazard.objects.bulk_create([Hazard(detection=detection, **h) for h in found])
        detection.risk_score = calculate_risk(found)
        detection.status = "completed"
    except Exception as e:
        detection.status = "failed"
        detection.error_message = str(e)
    detection.save()