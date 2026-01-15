import streamlit as st
import numpy as np
import cv2
import pytesseract
from PIL import Image
from collections import Counter
import random
from pyzbar.pyzbar import decode

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI วิเคราะห์เค้าไพ่", layout="centered")
st.title("🧠 AI วิเคราะห์เค้าไพ่จากรูป (อัตโนมัติ)")

# ---------------- SESSION ----------------
if "results" not in st.session_state:
    st.session_state.results = []

# ---------------- GAME SELECT ----------------
game = st.selectbox("🎮 เลือกเกม", ["บาคาร่า", "เสือมังกร", "แดงดำ"])

# ---------------- IMAGE UPLOAD ----------------
img_file = st.file_uploader(
    "📸 อัปโหลดรูป (รองรับรูปใหญ่ / แคปหน้าจอ)",
    type=["png", "jpg", "jpeg"]
)

# ---------------- FUNCTIONS ----------------
def read_qr(image):
    qr_data = decode(image)
    return [q.data.decode("utf-8") for q in qr_data]

def ocr_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray, lang="eng+tha")

def extract_result(text, game):
    text = text.lower()

    if game == "บาคาร่า":
        if "player" in text or "p" in text:
            return "P"
        if "banker" in text or "b" in text:
            return "B"
        if "tie" in text or "t" in text:
            return "T"

    if game == "เสือมังกร":
        if "tiger" in text:
            return "T"
        if "dragon" in text:
            return "D"

    if game == "แดงดำ":
        if "red" in text:
            return "R"
        if "black" in text:
            return "B"

    return None

def predict_next(results, game, n=10):
    if not results:
        return []

    counter = Counter(results)
    last = results[-1]

    probs = {}
    for k in counter:
        probs[k] = counter[k] / len(results)

    # bias ถ้าติดยาว
    run = 1
    for i in range(len(results) - 1, 0, -1):
        if results[i] == results[i - 1]:
            run += 1
        else:
            break

    if run >= 3:
        probs[last] = probs.get(last, 0) + 0.15

    total = sum(probs.values())
    probs = {k: v / total for k, v in probs.items()}

    choices = list(probs.keys())
    weights = list(probs.values())

    return random.choices(choices, weights=weights, k=n)

# ---------------- PROCESS IMAGE ----------------
if img_file:
    image = Image.open(img_file)
    st.image(image, use_column_width=True)

    img_np = np.array(image)

    # QR
    qr = read_qr(img_np)
    if qr:
        st.success("📷 พบ QR Code")
        for q in qr:
            st.write(q)

    # OCR
    text = ocr_text(img_np)
    result = extract_result(text, game)

    if result:
        st.session_state.results.append(result)
        st.success(f"✅ ตรวจพบผลล่าสุด: {result}")
    else:
        st.warning("⚠️ ไม่สามารถอ่านผลจากรูปได้ชัดเจน")

# ---------------- ANALYSIS ----------------
results = st.session_state.results
total = len(results)

if total > 0:
    st.divider()
    st.subheader(f"📊 ข้อมูลทั้งหมด {total} ตา")

    cnt = Counter(results)
    for k, v in cnt.items():
        st.write(f"{k} = {v} ({v/total*100:.1f}%)")

    preds = predict_next(results, game, n=10)
    if preds:
        st.divider()
        st.subheader("🔮 คาดการณ์ล่วงหน้า 10 ตา")
        st.write(" → ".join(preds))

# ---------------- RESET ----------------
if st.button("🔄 รีเซ็ตทั้งหมด"):
    st.session_state.results = []
