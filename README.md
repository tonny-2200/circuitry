
Circuitry.ai – Your AI Tutor for Electronic Circuit Diagrams (web application)

Circuitry.ai is an intelligent AI-powered tutor designed to understand and explain electronic circuit diagrams. Built to assist students, hobbyists and educators, Circuitry.ai uses computer vision and large language models to analyze circuit images and teach how they work—step by step.

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

