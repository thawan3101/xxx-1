import streamlit as st
import random
from collections import Counter

st.set_page_config(
    page_title="AI เค้าไพ่ อัตโนมัติ",
    layout="centered"
)

st.title("🃏 วิเคราะห์เค้าไพ่จากภาพ (อัตโนมัติ 10 ตา)")

# ---------- Session ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Game Select ----------
game = st.selectbox(
    "🎮 เลือกเกม",
    ["บาคาร่า", "เสือมังกร", "แดงดำ"]
)

# ---------- Image Upload ----------
img = st.file_uploader(
    "📸 อัปโหลดรูปผลล่าสุด (แคปหน้าจอได้เลย)",
    type=["png", "jpg", "jpeg"]
)

if img:
    st.image(img, use_container_width=True)

    # ---------- Define choices ----------
    if game == "บาคาร่า":
        choices = ["ผู้เล่น", "เจ้ามือ", "เสมอ"]
    elif game == "เสือมังกร":
        choices = ["เสือ", "มังกร"]
    else:
        choices = ["แดง", "ดำ"]

    # ---------- Auto generate next 10 ----------
    def predict_next(history, choices, n=10):
        result = []
        if history:
            last = history[-1]
            for _ in range(n):
                if random.random() < 0.6:
                    result.append(last)
                else:
                    result.append(random.choice(choices))
        else:
            result = random.choices(choices, k=n)
        return result

    # ---------- Simulate adding 1 new round ----------
    st.session_state.history.append(random.choice(choices))

    preds = predict_next(st.session_state.history, choices)

    # ---------- Display ----------
    st.divider()
    st.subheader("📊 วิเคราะห์อัตโนมัติ")

    cnt = Counter(st.session_state.history)
    for k, v in cnt.items():
        st.write(f"{k} = {v} ({v/len(st.session_state.history)*100:.1f}%)")

    st.divider()
    st.subheader("🔮 คาดการณ์ล่วงหน้า 10 ตา")

    for i, p in enumerate(preds, 1):
        st.write(f"ตาที่ {i} → {p}")

# ---------- Reset ----------
if st.button("🔄 รีเซ็ตทั้งหมด"):
    st.session_state.history = []
    st.experimental_rerun()
