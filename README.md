
🧠 Circuitry.ai – Understand Circuit Diagrams with AI

Circuitry.ai is an open-source tool that combines computer vision and large language models to detect, analyze, and explain electronic circuit diagrams. It leverages YOLOv8 for component detection and LLaMA 3 for generating intelligent textual explanations of how the circuit works. The goal is to bridge the gap between visual schematic representations and conceptual understanding, making electronics more accessible to learners, hobbyists, and engineers alike.

How It Works:

1. Component Detection:
   We use a YOLOv8 model trained on annotated data from Roboflow to accurately detect electronic components such as resistors, capacitors, transistors, and more.

2. Wire Detection:
   OpenCV processes the input diagram to detect connecting lines (wires) between components, extracting the circuit's structure visually.

3. Understanding the Circuit:
   The coordinates of detected components and wires are then passed as structured input to an **LLM (LLaMA 3)** using a carefully designed prompt.

4. AI-Powered Explanation:
   The LLM interprets the spatial and functional relationships between components and provides:
   A list of detected components
   An explanation of how the circuit works

![Input Image (2)](https://github.com/user-attachments/assets/2d83e851-ca08-4e50-ac54-35fc40a29786)


## 🛠️ Installation & Setup

### 1. Clone the Repository
```
git clone https://github.com/tonny-2200/circuitry.git
cd circuitry
```
🔍 Model Requirements

This project uses LLaMA 3 via gpt4all for reasoning over detected circuit components.

Steps to Use LLaMA 3:
Download a compatible LLaMA 3 model (e.g., llama3-8b.Q4_0.gguf) from:
👉 https://gpt4all.io/models/

Place the .gguf file in a known directory (e.g., models/llama3/).

In test.py, modify the paths of llama3 model and best.pt (weights of yolo model available in repo) like below:
Edit
```
yolo_model = YOLO(r'\your\actual\path\to\weights\of\yolov8\its provided in repo\best.pt') 
gpt_model = GPT4All(r"\your\actual\path\to\llama3\model\Meta-Llama-3-8B-Instruct.Q4_0.gguf" )
```
## Improvements / contributions
I have detected components(Yolov8) and lines(OpenCV) and created a Prompt which is given to LLM. This is not enough to make it more accurate its necessary to make a JSON file that contains all the nodes,components and not the line but which components is connected to which component. You can run the test.py and print components_data and lines_data variables to understand what i am talking about.
