# circuit_processor.py

import cv2
import numpy as np
from ultralytics import YOLO
from gpt4all import GPT4All

# Load only once globally
yolo_model = YOLO(r'C:\Users\tanma\OneDrive\Desktop\Project_work\AI_Tutor\runs\detect\train\weights\best.pt')
gpt_model = GPT4All(r"C:\Users\tanma\AppData\Local\nomic.ai\GPT4All\Meta-Llama-3-8B-Instruct.Q4_0.gguf" )

comp_name = ['and', 'antenna', 'capacitor-polarized', 'capacitor-unpolarized', 'crossover', 'diac', 'diode',
             'diode-light_emitting', 'fuse', 'gnd', 'inductor', 'integrated_circuit', 'integrated_cricuit-ne555',
             'lamp', 'microphone', 'motor', 'nand', 'nor', 'not', 'operational_amplifier', 'optocoupler', 'or',
             'probe-current', 'relay', 'resistor', 'resistor-adjustable', 'resistor-photo', 'schmitt_trigger',
             'socket', 'speaker', 'switch', 'terminal', 'thyristor', 'transformer', 'transistor', 'transistor-photo',
             'triac', 'varistor', 'voltage-dc', 'voltage-dc_ac', 'voltage-dc_regulator', 'vss', 'xor']


def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(image, (3, 3), 0)
    edges = cv2.Canny(blurred, 50, 150)
    return image, edges


def create_mask_from_boxes(image_shape, box_coords):
    height, width = image_shape
    mask = np.ones((height, width), dtype=np.uint8) * 255
    for box in box_coords:
        x1, y1, x2, y2 = map(int, box[:4])
        pts = np.array([[x1, y1], [x2, y1], [x2, y2], [x1, y2]], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.fillPoly(mask, [pts], color=0)
    return mask


def detect_and_filter_lines(masked_edges):
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, 100, minLineLength=30, maxLineGap=80)

    def are_lines_similar(l1, l2, pos_thresh=10, angle_thresh=5):
        x1, y1, x2, y2 = l1
        x3, y3, x4, y4 = l2
        angle1 = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        angle2 = np.degrees(np.arctan2(y4 - y3, x4 - x3))
        if abs(angle1 - angle2) > angle_thresh:
            return False
        mid1 = ((x1 + x2) // 2, (y1 + y2) // 2)
        mid2 = ((x3 + x4) // 2, (y3 + y4) // 2)
        return abs(mid1[0] - mid2[0]) <= pos_thresh and abs(mid1[1] - mid2[1]) <= pos_thresh

    filtered = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if not any(are_lines_similar((x1, y1, x2, y2), existing) for existing in filtered):
                filtered.append((x1, y1, x2, y2))
    return filtered


def prepare_dict_outputs(box_coords, class_ids, comp_name, filtered_lines):
    components_summary = []
    for b, cls in zip(box_coords, class_ids):
        x1, y1, x2, y2 = map(int, b[:4])
        comp = f"{comp_name[cls]}: ({x1}, {y1}, {x2}, {y2})"
        components_summary.append(comp)

    lines_summary = []
    for i, (x1, y1, x2, y2) in enumerate(filtered_lines):
        line = f"line{i+1}: ({x1}, {y1}) - ({x2}, {y2})"
        lines_summary.append(line)

    return components_summary, lines_summary

def comp_found(box_coords, class_ids, comp_name, filtered_lines):
    components_summary2 = []
    for b, cls in zip(box_coords, class_ids):
        x1, y1, x2, y2 = map(int, b[:4])
        comp = f"{comp_name[cls]}"
        components_summary2.append(comp)
    return components_summary2


def process_circuit_image(image_path):
    results = yolo_model(image_path)
    image, edges = preprocess_image(image_path)
    boxes = results[0].boxes
    box_coords = boxes.xyxy.cpu().numpy()
    class_ids = boxes.cls.cpu().numpy().astype(int)
    mask = create_mask_from_boxes(image.shape, box_coords)
    masked_edges = cv2.bitwise_and(edges, mask)
    filtered_lines = detect_and_filter_lines(masked_edges)
    components_data, lines_data = prepare_dict_outputs(box_coords, class_ids, comp_name, filtered_lines)
    if not components_data or len(components_data) == 0 or not lines_data or len(lines_data) == 0:
        raise ValueError("No components or lines detected")
    component_names = comp_found(box_coords, class_ids, comp_name, filtered_lines)
    prompt = (
    "You are an expert electronics engineer.\n"
    "Below is the list of detected components with their positions and the lines (wires) connecting them.\n"
    "Each component has a bounding box represented by (x1, y1, x2, y2).\n"
    "Each line shows two endpoints: (x1, y1) - (x2, y2).\n"
    "Based on this information, understand the circuit, dont give me co-ordinates, connections or bounding boxes\n"
    "Identify the type of electronic circuit and describe its working and provide information \n"
    "Components:\n"
    + "\n".join(components_data) + "\n\n"
    "Lines:\n"
    + "\n".join(lines_data) + "\n"
)

    with gpt_model.chat_session():
        response = gpt_model.generate(prompt, max_tokens=500)

    return response, component_names



