# -*- coding: utf-8 -*-
import streamlit as st
import os
import json
from PyPDF2 import PdfReader

# ➊ 📂 فولڈرز بنائیں (اگر موجود نہ ہوں)
if not os.path.exists("kitaabon_ki_files"):
    os.mkdir("kitaabon_ki_files")

if not os.path.exists("data"):
    os.mkdir("data")

# ➋ 📝 JSON فائل بنائیں (اگر موجود نہ ہو)
kitaabon_ki_record = "data/library_data.json"
if not os.path.exists(kitaabon_ki_record):
    with open(kitaabon_ki_record, "w") as f:
        json.dump([], f)

# ➌ 📖 کتب خانے کا ڈیٹا لوڈ کریں
def kitaabon_ko_load_karein():
    with open(kitaabon_ki_record, "r") as f:
        return json.load(f)

# ➍ 💾 کتب خانے کا ڈیٹا محفوظ کریں
def kitaabon_ko_save_karein(kitaab_list):
    with open(kitaabon_ki_record, "w") as f:
        json.dump(kitaab_list, f, indent=4, ensure_ascii=False)

# ➎ ➕ نئی کتاب شامل کریں
def nayi_kitaab_jodein(kitaab_ka_naam, musannif, file):
    # کتاب کو فولڈر میں محفوظ کریں
    file_ka_rasta = os.path.join("kitaabon_ki_files", file.name)
    with open(file_ka_rasta, "wb") as f:
        f.write(file.getbuffer())
    
    return {
        "kitaab_ka_naam": kitaab_ka_naam,
        "musannif": musannif,
        "file": file.name
    }

# ➏ 🗑️ کتاب کو ڈیلیٹ کریں (مکمل تفصیل)
def kitaab_ko_mitaen(kitaab):
    # JSON سے ڈیٹا ہٹائیں
    sabhi_kitaaben = kitaabon_ko_load_karein()
    nayi_list = [k for k in sabhi_kitaaben if k['file'] != kitaab['file']]
    kitaabon_ko_save_karein(nayi_list)
    
    # فائل ڈیلیٹ کریں
    file_ka_rasta = os.path.join("kitaabon_ki_files", kitaab['file'])
    if os.path.exists(file_ka_rasta):
        os.remove(file_ka_rasta)
    st.success(f"کتاب ڈیلیٹ ہو گئی: {kitaab['kitaab_ka_naam']}")

# ➐ 📄 PDF فائل پڑھیں
def kitaab_padhein(file_ka_rasta):
    try:
        reader = PdfReader(file_ka_rasta)
        pehla_safha = reader.pages[0].extract_text()
        st.text_area("پہلا صفحہ (نمونہ)", pehla_safha, height=300)
    except Exception as e:
        st.error("فائل پڑھنے میں مسئلہ!")

# ➑ 📚 کتب خانہ دکھائیں
def kitaabon_ka_khaana_dikhaein():
    st.subheader("میری کتابیں")
    sabhi_kitaaben = kitaabon_ko_load_karein()
    
    if not sabhi_kitaaben:
        st.warning("ابھی تک کوئی کتاب شامل نہیں کی گئی!")
    
    for kitaab in sabhi_kitaaben:
        st.markdown(f"### {kitaab['kitaab_ka_naam']}")
        st.caption(f"مصنف: {kitaab['musannif']}")
        
        # بٹنز کے کالم
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 پڑھیں", key=f"read_{kitaab['file']}"):
                kitaab_padhein(os.path.join("kitaabon_ki_files", kitaab['file']))
        with col2:
            if st.button("🗑️ ڈیلیٹ", key=f"del_{kitaab['file']}"):
                kitaab_ko_mitaen(kitaab)

# ➒ 🖥️ ایپ کا بنیادی ڈیزائن
st.title("📚 میرا ذاتی کتب خانہ")
menu = st.radio("مینو", ["نئی کتاب شامل کریں", "کتب خانہ دیکھیں"])

if menu == "نئی کتاب شامل کریں":
    st.subheader("نئی کتاب جمع کروائیں")
    naam = st.text_input("کتاب کا نام")
    lekhak = st.text_input("مصنف کا نام")
    uploaded_file = st.file_uploader("PDF فائل اپ لوڈ کریں", type="pdf")
    
    if st.button("محفوظ کریں") and naam and lekhak and uploaded_file:
        nayi_kitaab = nayi_kitaab_jodein(naam, lekhak, uploaded_file)
        sabhi_kitaaben = kitaabon_ko_load_karein()
        sabhi_kitaaben.append(nayi_kitaab)
        kitaabon_ko_save_karein(sabhi_kitaaben)
        st.success("کامیابی سے محفوظ ہو گیا!")

elif menu == "کتب خانہ دیکھیں":
    kitaabon_ka_khaana_dikhaein()


