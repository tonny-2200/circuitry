from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import os
from test import process_circuit_image  # This is your image processing pipeline
import markdown
app = Flask(__name__)
app.secret_key = 'ai_tut_22'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = None
    image_path = None
    components = []
    result_html = None   # Initialize here

    if request.method == 'POST':
        file = request.files['photo']
        if file:
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            try:
                response_text, components = process_circuit_image(image_path)
                result_html = markdown.markdown(response_text)
            except ValueError as e:
                flash(str(e))  # "Upload a valid circuit diagram"
            except Exception as e:
                flash("Bro! Upload a valid image, Haven't read the description? Circuit Diagrams!! bro Circuit Diagrams!! ")
    return render_template('index.html', result=result_html, components=components, image_path=image_path)
if __name__ == '__main__':
    app.run(debug=True)
