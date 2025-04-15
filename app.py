from flask import Flask, request, send_file, jsonify
import os
from PIL import Image

app = Flask(__name__)

# Upload folder configuration
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return '''
        <html>
        <body>
            <h2>Upload a PNG file to convert it to JPG</h2>
            <form method="POST" enctype="multipart/form-data" action="/upload">
                <input type="file" name="file" accept=".png" required>
                <input type="submit" value="Upload">
            </form>
        </body>
        </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Check if the uploaded file is a PNG file
    if not file.filename.lower().endswith('.png'):
        return jsonify({"error": "This is not a valid file"}), 400

    # Save the file
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)

    # Open the image and convert to JPG
    try:
        img = Image.open(filename)
        jpg_filename = os.path.splitext(filename)[0] + '.jpg'
        img.convert('RGB').save(jpg_filename, 'JPEG')

        # Return the converted JPG file to the user
        return send_file(jpg_filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
