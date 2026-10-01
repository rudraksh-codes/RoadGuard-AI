import cv2

def extract_frames(path, every_seconds=5.0, max_frames=30):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    step = max(int(fps * every_seconds), 1)
    index, taken = 0, 0
    while taken < max_frames:
        ok, frame = cap.read()
        if not ok:
            break
        if index % step == 0:
            yield index, frame
            taken += 1
        index += 1
    cap.release()