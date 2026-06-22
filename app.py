import streamlit as st
from pypdf import PdfReader
import time

# ========== إعدادات الصفحة ==========

st.set_page_config(
    page_title="📄 محلل السيرة الذاتية الذكي",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== CSS مخصص للتصميم العصري ==========

st.markdown("""

<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* الخلفية */
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
    }
    
    /* الحاوية الرئيسية */
    .main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 40px 20px;
    }
    
    /* العنوان الرئيسي مع أنميشن */
    .hero-section {
        text-align: center;
        margin-bottom: 50px;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .hero-section h1 {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 900;
        letter-spacing: -1px;
        margin-bottom: 15px;
        animation: slideInUp 0.8s ease-out 0.2s both;
    }
    
    .hero-section p {
        font-size: 1.2rem;
        color: #495057;
        animation: slideInUp 0.8s ease-out 0.4s both;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    /* بطاقة المحتوى */
    .card {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.15);
        margin-bottom: 30px;
        animation: fadeInUp 0.8s ease-out 0.6s both;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 80px rgba(102, 126, 234, 0.25);
    }
    
    /* عنصر الرفع */
    .upload-area {
        border: 3px dashed #667eea;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
    }
    
    .upload-area:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    }
    
    /* الأيقونات */
    .icon-large {
        font-size: 4rem;
        margin-bottom: 20px;
        animation: bounce 2s infinite;
    }
    
    /* النص داخل منطقة الرفع */
    .upload-text {
        color: #667eea;
        font-size: 1.3rem;
        font-weight: 600;
        margin: 15px 0;
    }
    
    .upload-hint {
        color: #adb5bd;
        font-size: 0.95rem;
    }
    
    /* رسالة النجاح */
    .success-message {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        animation: slideInLeft 0.6s ease-out;
        border-left: 5px solid #4fa58d;
    }
    
    .success-icon {
        display: inline-block;
        margin-right: 10px;
        animation: pulse 1s infinite;
    }
    
    /* رسالة المعلومات */
    .info-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 20px 0;
        animation: slideInRight 0.6s ease-out;
    }
    
    /* منطقة النص المستخرج */
    .text-preview {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #667eea;
        margin-top: 20px;
        animation: fadeIn 0.6s ease-out;
    }
    
    /* أزرار مخصصة */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 40px;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* خط فاصل جميل */
    .divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 30px 0;
        animation: slideInRight 0.8s ease-out;
    }
    
    /* الشريط العلوي */
    .top-bar {
        height: 5px;
        background: linear-gradient(90deg, #667eea, #764ba2, #667eea);
        animation: gradient 3s ease infinite;
        margin-bottom: 40px;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    @keyframes gradient {
        0%, 100% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-section h1 {
            font-size: 2.5rem;
        }
        
        .card {
            padding: 25px;
        }
        
        .icon-large {
            font-size: 3rem;
        }
    }
</style>

""", unsafe_allow_html=True)

# ========== المحتوى الرئيسي ==========

# الشريط العلوي

st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)

# قسم البطل (Hero Section)

st.markdown("""

<div class="hero-section">
    <h1>📄 محلل السيرة الذاتية الذكي</h1>
    <p>حلل سيرتك الذاتية واحصل على تقييم شامل وملاحظات قيمة على الفور</p>
</div>
""", unsafe_allow_html=True)

# البطاقة الرئيسية

st.markdown('<div class="card">', unsafe_allow_html=True)

# قسم الرفع

st.markdown("""

<div class="upload-area">
    <div class="icon-large">📤</div>
    <div class="upload-text">اختر ملف السيرة الذاتية</div>
    <div class="upload-hint">PDF بصيغة عالية الجودة</div>
</div>
""", unsafe_allow_html=True)

# زر رفع الملف

uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)

# معالجة الملف المرفوع

if uploaded_file is not None:
    # رسالة النجاح
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        st.markdown(f"""
        <div class="success-message">
            <span class="success-icon">✅</span>
            تم رفع الملف: <strong>{uploaded_file.name}</strong>
        </div>
        """, unsafe_allow_html=True)

    # خط فاصل
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # عرض تقدم معالجة الملف
    progress_bar = st.progress(0)
    status_text = st.empty()

    # محاكاة معالجة الملف
    for i in range(100):
        progress_bar.progress(i + 1)
        time.sleep(0.01)

    # قراءة ملف PDF
    with st.spinner("🔄 جاري قراءة محتوى السيرة الذاتية..."):
        try:
            reader = PdfReader(uploaded_file)
            extracted_text = ""
            total_pages = len(reader.pages)

            for idx, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

            # رسالة النجاح
            st.markdown("""
            <div class="info-message">
                <strong>🎯 تم استخراج النص بنجاح!</strong>
            </div>
            """, unsafe_allow_html=True)

            # عرض المعلومات الأساسية
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📄 عدد الصفحات", total_pages)
            with col2:
                st.metric("📝 عدد الكلمات", len(extracted_text.split()))
            with col3:
                st.metric("📊 عدد الأحرف", len(extracted_text))

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            # عرض النص المستخرج
            st.markdown("""
            <div class="card">
                <h3>📋 النص المستخرج (معاينة)</h3>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="text-preview">
                {extracted_text[:500]}...
            </div>
            """, unsafe_allow_html=True)

            # زر للمتابعة
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <p style="color: #667eea; font-size: 1.1rem; font-weight: 600;">
                    ✨ المحطة الثانية تمت بنجاح!
                </p>
                <p style="color: #adb5bd; margin-top: 10px;">
                    جاهزون للمحطة الثالثة: الربط بالذكاء الاصطناعي والتحليل الشامل
                </p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
                        color: white; padding: 20px; border-radius: 12px;
                        margin: 20px 0; border-left: 5px solid #c92a2a;">
                <strong>❌ خطأ في معالجة الملف</strong><br>
                {str(e)}
            </div>
            """, unsafe_allow_html=True)

else:
    # رسالة عندما لا يكون هناك ملف مرفوع
    st.markdown("""
    <div class="card" style="text-align: center; padding: 60px 40px;">
        <div style="font-size: 3rem; margin-bottom: 20px;">🚀</div>
        <h3 style="color: #667eea; margin-bottom: 10px;">ابدأ الآن</h3>
        <p style="color: #adb5bd; font-size: 1.1rem;">
            قم برفع ملف السيرة الذاتية الخاص بك للحصول على تحليل احترافي شامل
        </p>
    </div>
    """, unsafe_allow_html=True)

# الهامش السفلي

st.markdown("""

<div style="text-align: center; margin-top: 60px; padding: 20px; color: #adb5bd;">
    <p style="font-size: 0.9rem;">
        © 2026 محلل السيرة الذاتية الذكي | تم التطوير بـ ❤️
    </p>
</div>
""", unsafe_allow_html=True)
