from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Render otomatik PORT verir
PORT = int(os.environ.get("PORT", 10000))
API_TOKEN = "zordo123"

# Veri dosyası (aynı klasörde)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "veri.txt")


def client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    return request.remote_addr


def veri_oku():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8", errors="ignore") as f:
        return f.readlines()


@app.route("/")
def index():
    return jsonify({
        "durum": "API aktif",
        "kullanim": "/sorgu?token=zordo123&gsm=5XXXXXXXXX"
    })


@app.route("/sorgu")
def sorgu():
    ip = client_ip()
    token = request.args.get("token")
    gsm = request.args.get("gsm")

    print(f"[SORGULA] IP={ip} GSM={gsm}")

    if token != API_TOKEN:
        return jsonify({"hata": "gecersiz token"}), 403

    if not gsm:
        return jsonify({"hata": "gsm parametresi gerekli"}), 400

    for satir in veri_oku():
        satir = satir.strip()
        if not satir:
            continue

        # boşluk veya tab ile ayır
        parts = satir.replace("\t", " ").split()
        if len(parts) < 2:
            continue

        gsm_txt, tc_txt = parts[0], parts[1]

        if gsm == gsm_txt:
            return jsonify({
                "gsm": gsm_txt,
                "tc": tc_txt
            })

    return jsonify({"sonuc": "bulunamadi"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
