import re

def extract_number_plate(reader, crop):
    if crop is None or crop.size == 0:
        return None

    results = reader.readtext(crop)
    best_text, best_conf = None, 0

    for (_, text, conf) in results:
        if conf > best_conf:
            best_text, best_conf = text, conf

    if best_text:
        best_text = re.sub(r'[^A-Z0-9]', '', best_text.upper())

    return best_text
