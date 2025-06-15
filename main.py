from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import qrcode
import sqlite3
import os
from reportlab.pdfgen import canvas

app = Flask(__name__)

os.makedirs("static/qrcodes", exist_ok=True)
os.makedirs("generated/pdfs", exist_ok=True)

def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            info TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    info = request.form['info']

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT INTO documents (name, info) VALUES (?, ?)", (name, info))
    doc_id = c.lastrowid
    conn.commit()
    conn.close()

    verify_url = f"{request.host_url}verify/{doc_id}"
    qr_img = qrcode.make(verify_url)
    qr_path = f"static/qrcodes/qr_{doc_id}.png"
    qr_img.save(qr_path)

    pdf_path = f"generated/pdfs/doc_{doc_id}.pdf"
    c = canvas.Canvas(pdf_path)
    c.drawString(100, 750, f"Nama: {name}")
    c.drawString(100, 730, f"Info: {info}")
    c.drawImage(qr_path, 100, 600, width=150, height=150)
    c.save()

    return redirect(url_for("verify", doc_id=doc_id))

@app.route('/verify/<int:doc_id>')
def verify(doc_id):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT name, info FROM documents WHERE id=?", (doc_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return render_template("verify.html", name=row[0], info=row[1], doc_id=doc_id, valid=True)
    else:
        return render_template("verify.html", valid=False)

@app.route('/download/<int:doc_id>')
def download(doc_id):
    return send_from_directory('generated/pdfs', f'doc_{doc_id}.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
