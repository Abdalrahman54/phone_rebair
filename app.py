import streamlit as st
from google import genai
from google.genai import types

# ==========================================
# إعدادات الصفحة
# ==========================================

st.set_page_config(
    page_title="فحص قطع الهواتف",
    page_icon="📱",
    layout="centered"
)

# RTL + تنسيق عربي
st.markdown("""
<style>
    .stApp { direction: rtl; text-align: right; }
    .stRadio > div { direction: rtl; }
    h1, h2, h3, p, div { direction: rtl; text-align: right; }
    .result-box {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 25px;
        margin-top: 15px;
        line-height: 2;
        font-size: 17px;
        white-space: pre-wrap;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# Gemini API
# ==========================================

API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# ==========================================
# Prompt
# ==========================================

PROMPT = """
أنت خبير متخصص في صيانة وإعادة استخدام قطع الهواتف الذكية.

حلل صورة قطعة الهاتف المرفقة بعناية.

حدد المعلومات التالية:
1. اسم القطعة.
2. الحالة الفيزيائية للقطعة.
3. العيوب الظاهرة في الصورة.
4. هل تبدو القطعة صالحة لإعادة الاستخدام؟
5. درجة الثقة في التحليل من 0 إلى 100.
6. سبب القرار.
7. هل تحتاج القطعة إلى اختبار كهربائي أو اختبار عملي؟

ابحث عن علامات مثل:
- الكسور
- الانتفاخ
- الحروق
- الصدأ
- التآكل
- الخدوش
- التشوه
- الموصلات المكسورة
- الأجزاء المفقودة
- آثار السوائل
- التلف الواضح

مهم جدًا:
الصورة وحدها لا يمكنها إثبات أن القطعة تعمل كهربائيًا.
إذا كان من المستحيل التأكد من عمل القطعة من الصورة فقط،
اذكر بوضوح أن هناك حاجة إلى اختبار كهربائي أو اختبار عملي.
لا تخمن وجود عيب غير ظاهر في الصورة.

أجب باللغة العربية فقط.

استخدم هذا التنسيق:
اسم القطعة:
الحالة:
القرار:
درجة الثقة:
العيوب الظاهرة:
سبب القرار:
الاختبارات المطلوبة:
"""

# ==========================================
# واجهة المستخدم
# ==========================================

st.title("📱 نظام فحص قطع الهواتف")
st.caption("تحليل بصري باستخدام Gemini AI")

st.divider()

option = st.radio(
    "اختر طريقة إدخال الصورة:",
    ["📷 التقاط صورة بالكاميرا", "📁 رفع صورة من الجهاز"]
)

image_data = None

if option == "📷 التقاط صورة بالكاميرا":
    camera_image = st.camera_input("التقط صورة للقطعة")
    if camera_image:
        image_data = camera_image.getvalue()

else:
    uploaded_file = st.file_uploader(
        "اختر صورة من جهازك",
        type=["jpg", "jpeg", "png", "webp"]
    )
    if uploaded_file:
        image_data = uploaded_file.getvalue()

if image_data:
    st.image(image_data, caption="الصورة المحددة", use_container_width=True)

    if st.button("🔍 تحليل الصورة", use_container_width=True, type="primary"):
        with st.spinner("جاري تحليل الصورة..."):
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=image_data, mime_type="image/jpeg"),
                    PROMPT
                ]
            )
        st.divider()
        st.subheader("🔍 نتيجة التحليل")
        st.markdown(
            f'<div class="result-box">{response.text}</div>',
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("Powered by Gemini AI")