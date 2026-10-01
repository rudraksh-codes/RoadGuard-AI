from django.conf import settings

_model = None

def _get_model():
    global _model
    if _model is None:
        from ultralytics import YOLO
        _model = YOLO(str(settings.YOLO_MODEL_PATH))
        return _model

def run_detection(source) : 
    """source = file path OR an OpenCV frame. Returns a list of dicts"""
    if settings.USE_DUMMY_DETECTOR : 
        return [
            {"hazard_type": "pothole", "confidence": 0.91, "x1": 120, "y1": 80, "x2": 340, "y2": 250},
            {"hazard_type": "debris", "confidence": 0.84, "x1": 400, "y1": 150, "x2": 520, "y2": 300},
        ]

    model = _get_model()
    results = model(source, verbose=False)
    result = results[0] 

    #detection function (from Ai guy)
    found = []
    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        found.append({
            "hazard_type": result.names[int(box.cls[0])],
            "confidence": float(box.conf[0]),
            "x1": x1, "y1": y1, "x2": x2, "y2": y2,
        })
    return found