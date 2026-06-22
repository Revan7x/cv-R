import streamlit as st
from pypdf import PdfReader

# إعدادات الصفحة
st.set_page_config(page_title="مستشار السيرة الذاتية الذكي", page_icon="📄", layout="centered")

# عنوان الموقع الرئيسي
st.title("📄 مستشار السيرة الذاتية بالذكاء الاصطناعي")
st.subheader("ارفع ملف السيرة الذاتية (CV) الخاص بك واحصل على تحليل دقيق ونقاط التعديل فوراً!")

st.write("---")

# زر رفع الملف
uploaded_file = st.file_uploader("اختر ملف السيرة الذاتية بصيغة PDF", type=["pdf"])

if uploaded_file is not None:
    st.success(f"تم رفع الملف بنجاح: {uploaded_file.name}")
    
    # كود قراءة ملف الـ PDF
    with st.spinner("جاري قراءة محتوى السيرة الذاتية... ⏳"):
        reader = PdfReader(uploaded_file)
        extracted_text = ""
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
        
    # عرض جزء من النص للتأكد من نجاح القراءة
    if extracted_text.strip():
        st.info("🎯 تم استخراج النص بنجاح!")
        st.text_area("النص المستخرج (معاينة أولية):", extracted_text[:300] + "...", height=150)
        st.success("المحطة الثانية تمت بنجاح! جاهزون للمحطة الثالثة والربط بالذكاء الاصطناعي.")
    else:
        st.error("عذراً، لم نتمكن من استخراج نص واضح من هذا الملف. تأكد أنه ليس ملفاً ممسوحاً ضوئياً كصورة.")