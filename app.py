import streamlit as st
from pypdf import PdfReader
import time

# ========== 1. إعدادات الصفحة ==========
st.set_page_config(
    page_title="📄 محلل السيرة الذاتية الذكي",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== 2. CSS مخصص متطور (UI/UX) ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');

    /* تطبيق خط ك those على كامل التطبيق */
    * {
        font-family: 'Cairo', sans-serif;
        box-sizing: border-box;
    }
    
    /* خلفية التطبيق العامة */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* الشريط العلوي المتحرك */
    .top-bar {
        height: 6px;
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        background-size: 200% auto;
        animation: gradientBar 3s linear infinite;
        border-radius: 3px;
        margin-bottom: 30px;
    }
    
    /* قسم الرأس (Hero) */
    .hero-section {
        text-align: center;
        margin-bottom: 40px;
        padding: 20px 0;
    }
    
    .hero-section h1 {
        font-size: 3.2rem;
        background: linear-gradient(135deg, #4a00e0 0%, #8e2de2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 12px;
    }
    
    .hero-section p {
        font-size: 1.2rem;
        color: #555b6e;
        font-weight: 500;
    }
    
    /* البطاقة الزجاجية المتطورة (Glassmorphism) */
    .card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 35px;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.08);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.6);
        transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.4s ease;
    }
    
    .card:hover {
        transform: translateY(-6px);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.15);
    }
    
    /* منطقة رفع الملف الاحترافية */
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 18px;
        padding: 45px 20px;
        text-align: center;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.03) 0%, rgba(118, 75, 162, 0.03) 100%);
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.07) 0%, rgba(118, 75, 162, 0.07) 100%);
    }
    
    .icon-large {
        font-size: 3.5rem;
        margin-bottom: 15px;
        display: inline-block;
        animation: float 3s ease-in-out infinite;
    }
    
    .upload-text {
        color: #4a00e0;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    .upload-hint {
        color: #8892b0;
        font-size: 0.95rem;
    }
    
    /* العدادات المخصصة الملونة */
    .metric-container {
        display: flex;
        justify-content: space-around;
        gap: 20px;
        margin: 20px 0;
    }
    
    .custom-metric {
        flex: 1;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid rgba(102, 126, 234, 0.15);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    
    .custom-metric-title {
        font-size: 0.95rem;
        color: #6c757d;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .custom-metric-value {
        font-size: 1.8rem;
        color: #667eea;
        font-weight: 700;
    }
    
    /* التنبيهات والرسائل */
    .success-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 18px;
        border-radius: 14px;
        font-weight: 600;
        box-shadow: 0 10px 20px rgba(56, 239, 125, 0.2);
    }
    
    .info-message {
        background: linear-gradient(135deg, #3a7bd5 0%, #3a6073 100%);
        color: white;
        padding: 15px;
        border-radius: 14px;
        font-weight: 600;
        text-align: center;
    }
    
    /* لوحة معاينة النص المستخرج (Dark Mode Preview) */
    .text-preview {
        background: #1e1e24;
        color: #a5b4fc;
        border-radius: 14px;
        padding: 25px;
        font-family: 'Courier New', Courier, monospace;
        direction: rtl;
        text-align: right;
        white-space: pre-wrap;
        max-height: 250px;
        overflow-y: auto;
        border: 1px solid #312e81;
        box-shadow: inset 0 4px 10px rgba(0,0,0,0.3);
    }
    
    /* تخصيص الفاصل الزمني */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.4), transparent);
        margin: 25px 0;
    }
    
    /* الأنيميشن والأشكال الحركية */
    @keyframes gradientBar {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-8px); }
    }
</style>
""", unsafe_allow_html=True)

# ========== 3. بناء الواجهة الرئيسية ==========
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("""
<div class="hero-section">
    <h1>📄 محلل السيرة الذاتية الذكي</h1>
    <p>ارفع ملفك الآن لتجربة تحليل ذكية، فورية، ومبنية على معايير التوظيف الاحترافية</p>
</div>
""", unsafe_allow_html=True)

# حاوية رفع الملف
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("""
<div class="upload-area">
    <div class="icon-large">📥</div>
    <div class="upload-text">اسحب وأفلت ملف السيرة الذاتية</div>
    <div class="upload-hint">يدعم فقط صيغة PDF بجودة عالية</div>
</div>
""", unsafe_allow_html=True)

# حقل رفع الملف الفعلي (مخفي العنوان بشكل جميل)
uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

# ========== 4. منطق معالجة الملف ==========
if uploaded_file is not None:
    # رسالة نجاح الرفع
    st.markdown(f"""
    <div class="success-message">
        ✨ تم استلام الملف بنجاح: {uploaded_file.name}
    </div>
    """, unsafe_allow_html=True)
        
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # شريط التقدم الأنيميشن
    progress_bar = st.progress(0)
    for i in range(100):
        progress_bar.progress(i + 1)
        time.sleep(0.004)
        
    with st.spinner("🔄 جاري قراءة واستخراج النصوص..."):
        try:
            reader = PdfReader(uploaded_file)
            extracted_text = ""
            total_pages = len(reader.pages)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
                    
            if extracted_text.strip():
                # إشعار نجاح استخراج النص
                st.markdown("""
                <div class="info-message">
                    🎯 المحطة الثانية: تم قراءة محتويات الملف واستخراج النص بدقة!
                </div>
                """, unsafe_allow_html=True)
                
                st.write("") # مساحة فارغة
                
                # العدادات الإحصائية بتصميم CSS مخصص وجذاب
                st.markdown(f"""
                <div class="metric-container">
                    <div class="custom-metric">
                        <div class="custom-metric-title">📄 إجمالي الصفحات</div>
                        <div class="custom-metric-value">{total_pages}</div>
                    </div>
                    <div class="custom-metric">
                        <div class="custom-metric-title">📝 عدد الكلمات</div>
                        <div class="custom-metric-value">{len(extracted_text.split()):,}</div>
                    </div>
                    <div class="custom-metric">
                        <div class="custom-metric-title">📊 عدد الأحرف</div>
                        <div class="custom-metric-value">{len(extracted_text):,}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                # صندوق معاينة النص المستخرج المطور
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<h3 style="color:#4a00e0; margin-bottom:15px;">📋 معاينة النص المكتشف</h3>', unsafe_allow_html=True)
                st.markdown(f"""
                <div class="text-preview">
{extracted_text[:600]}...
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # بطاقة الانتقال للمرحلة القادمة
                st.markdown("""
                <div class="card" style="text-align: center; border-top: 4px solid #764ba2;">
                    <p style="color: #764ba2; font-size: 1.2rem; font-weight: 700; margin-bottom: 5px;">
                        🚀 جاهزون للمحطة الثالثة والأهم!
                    </p>
                    <p style="color: #6c757d; font-size: 0.95rem;">
                        الخطوة التالية هي إرسال هذا النص إلى مستشار الذكاء الاصطناعي لإنشاء التقرير الشامل.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("عذراً، لم نتمكن من استخراج نص واضح من هذا الملف. تأكد أنه ليس ملفاً ممسوحاً ضوئياً كصورة.")
        except Exception as e:
            st.error(f"حدث خطأ أثناء معالجة الملف: {str(e)}")
else:
    # شاشة الترحيب الافتراضية عند عدم وجود ملف
    st.markdown("""
    <div class="card" style="text-align: center; padding: 50px 20px;">
        <div style="font-size: 3.5rem; margin-bottom: 15px;">🚀</div>
        <h3 style="color: #4a00e0; font-weight:700; margin-bottom: 8px;">حلل سيرتك الذاتية بثوانٍ</h3>
        <p style="color: #747d8c; max-width: 500px; margin: 0 auto; font-size: 1rem;">
            نظامنا يقرأ ملفك، يستخرج البيانات، ويهيئها للربط بالذكاء الاصطناعي ليعطيك نقاط القوة والضعف فوراً.
        </p>
    </div>
    """, unsafe_allow_html=True)

# الهامش السفلي الثابت والأنيق
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; color: #a4b0be; font-size: 0.9rem;">
    © 2026 محلل السيرة الذاتية الذكي | صُنع بكل شغف 💻
</div>
""", unsafe_allow_html=True)
