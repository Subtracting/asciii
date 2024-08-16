from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from renderer import process_image

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = "uploads/"
OUTPUT_FOLDER = "output/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        output_path = os.path.join(
            app.config["OUTPUT_FOLDER"], f"output_{file.filename}.png"
        )

        size = int(request.form.get("size"))
        mapping = list(request.form.get("mapping"))
        fontscale = int(request.form.get("fontscale"))
        process_image(
            file_path,
            size=size,
            mapping=mapping,
            output_path=output_path,
            font_scale=fontscale,
        )

        return (
            jsonify(
                {
                    "message": "File successfully uploaded",
                    "filename": f"output_{file.filename}.png",
                }
            ),
            200,
        )
    return jsonify({"error": "Invalid file type"}), 400


@app.route("/api/output/<filename>", methods=["GET"])
def get_file(filename):
    return send_from_directory(app.config["OUTPUT_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
