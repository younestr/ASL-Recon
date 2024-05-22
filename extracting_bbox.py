import json

# Hand data string
hand_data_str = [{"lmList": [[275, 314, 0], [315, 303, -19], [352, 292, -31], [386, 286, -43], [414, 289, -54], [321, 216, -9], [344, 180, -18], [355, 156, -28], [364, 136, -35], [296, 207, -9], [311, 161, -14], [318, 134, -21], [323, 111, -27], [272, 207, -12], [278, 164, -18], [282, 137, -26], [288, 116, -32], [246, 216, -17], [232, 184, -23], [225, 162, -27], [220, 141, -30]], "bbox": [220, 111, 194, 203], "center": [317, 212], "type": "Right"}]

# Convert the list to a JSON formatted string
hand_data_json_str = json.dumps(hand_data_str)

# Print the JSON string to debug
print("JSON string:", hand_data_json_str)

# Loading JSON
hand_data_json = json.loads(hand_data_json_str)

# Extracting bbox
bbox = hand_data_json[0]['lmList']

print("Bounding box:", bbox)


