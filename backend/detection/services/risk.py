
SEVERITY = {"waterlogging": 90, "pothole": 80, "debris": 60, "crack": 50}


def calculate_risk(hazards):
    # keep only the best confidence per hazard type (stops video duplicates from inflating the score)


    best = {}

    for hazard in hazards:
        hazard_type = hazard["hazard_type"]
        confidence = hazard["confidence"]

        if hazard_type not in best:
            best[hazard_type] = confidence
        elif confidence > best[hazard_type]:
            best[hazard_type] = confidence

    scores = []

    for hazard_type in best:
        confidence = best[hazard_type]
        severity = SEVERITY.get(hazard_type, 40)

        score = severity * confidence
        scores.append(score)

    scores.sort(reverse=True)

    if len(scores) == 0:
        return 0.0

    total = scores[0]

    for score in scores[1:]:
        total += score * 0.3

    total = min(100, total)

    return round(total, 1)