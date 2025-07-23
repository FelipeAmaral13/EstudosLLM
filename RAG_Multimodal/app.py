from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
import os, uuid

from analyzer import MultimodalRAGAnalyzer

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

app = Flask(__name__, static_url_path="/static")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SECRET_KEY"] = "sua-chave-secreta"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
rag_analyzer = MultimodalRAGAnalyzer()


def allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file_storage):
    ext = file_storage.filename.rsplit(".", 1)[1].lower()
    fname = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
    file_storage.save(path)
    return fname, path


@app.route("/", methods=["GET", "POST"])
def index():
    resposta = None
    pergunta = None

    if "upload" in request.form:
        file = request.files.get("file")
        if file and allowed(file.filename):
            filename, path = save_file(file)
            session["uploaded_file"] = filename
            return redirect(url_for("index"))

    elif "ask" in request.form:
        pergunta = request.form.get("question", "").strip()
        filename = session.get("uploaded_file")
        if pergunta and filename:
            img_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            with open(img_path, "rb") as f:
                img_bytes = f.read()
            response = rag_analyzer.analyze_invoice(
                query=pergunta,
                image_bytes=img_bytes,
                image_mime_type=f"image/{filename.rsplit('.',1)[1]}"
            )
            resposta = response["final_answer"]

    return render_template(
        "index.html",
        uploaded_filename=session.get("uploaded_file"),
        resposta=resposta,
        pergunta=pergunta
    )


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
