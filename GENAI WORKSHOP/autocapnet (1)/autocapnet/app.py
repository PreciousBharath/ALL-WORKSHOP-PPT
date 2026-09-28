import time
import streamlit as st
from PIL import Image
from deep_translator import GoogleTranslator
from fpdf import FPDF
from transformers import BlipProcessor, BlipForConditionalGeneration
from keybert import KeyBERT


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Image Caption Generator",
    page_icon="🖼️",
    layout="centered"
)


# ============================================================
# LOAD AI MODELS
# ============================================================

@st.cache_resource
def load_caption_model():

    processor = BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )

    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )

    return processor, model


@st.cache_resource
def load_keyword_model():

    return KeyBERT()


with st.spinner("Loading AI models..."):
    processor, model = load_caption_model()
    kw_model = load_keyword_model()


# ============================================================
# TITLE
# ============================================================

st.title("🖼️ AI Image Caption Generator")

st.write(
    "Upload an image to generate an AI caption, "
    "semantic tags, and translation."
)


# ============================================================
# LANGUAGE SELECTION
# ============================================================

language = st.selectbox(
    "🌐 Select Language",
    ["English", "Tamil", "Hindi"]
)


# ============================================================
# IMAGE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📤 Upload Image",
    type=["jpg", "jpeg", "png"]
)


# ============================================================
# PDF GENERATOR
# ============================================================

def create_pdf(text):

    pdf = FPDF()

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.add_page()

    pdf.set_margins(
        15,
        15,
        15
    )

    pdf.add_font(
        "DejaVu",
        "",
        "DejaVuSans.ttf",
        uni=True
    )

    pdf.set_font(
        "DejaVu",
        size=12
    )

    page_width = (
        pdf.w - 2 * pdf.l_margin
    )

    for line in text.split("\n"):

        if line.strip() == "":
            pdf.ln(6)

        else:
            pdf.multi_cell(
                page_width,
                8,
                line,
                align="L"
            )

    return bytes(
        pdf.output(dest="S")
    )


# ============================================================
# TRANSLATION FUNCTION
# ============================================================

def translate_text(text, target_language):

    try:

        translator = GoogleTranslator(
            source="en",
            target=target_language
        )

        time.sleep(0.5)

        return translator.translate(text)

    except Exception:

        st.warning(
            "⚠️ Translation service is temporarily unavailable. "
            "Showing English text instead."
        )

        return text


# ============================================================
# TRANSLATE TAGS
# ============================================================

def translate_tags(tags, target_language):

    if not tags:
        return []

    try:

        translator = GoogleTranslator(
            source="en",
            target=target_language
        )

        time.sleep(0.5)

        return translator.translate_batch(tags)

    except Exception:

        st.warning(
            "⚠️ Some tags could not be translated. "
            "Showing English tags instead."
        )

        return tags


# ============================================================
# PROCESS IMAGE
# ============================================================

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    if st.button(
        "🤖 Generate Caption",
        type="primary"
    ):

        with st.spinner(
            "🔄 Processing image with AI..."
        ):

            # =================================================
            # 1. IMAGE CAPTIONING
            # =================================================

            inputs = processor(
                image,
                return_tensors="pt"
            )

            output = model.generate(
                **inputs,
                max_new_tokens=50
            )

            caption_en = processor.decode(
                output[0],
                skip_special_tokens=True
            )


            # =================================================
            # 2. SEMANTIC TAGS
            # =================================================

            try:

                keywords = kw_model.extract_keywords(
                    caption_en,
                    keyphrase_ngram_range=(1, 2),
                    stop_words="english",
                    top_n=8
                )

                tags_en = [
                    keyword[0]
                    for keyword in keywords
                ]

            except Exception:

                tags_en = []


            # =================================================
            # 3. TRANSLATION
            # =================================================

            if language == "Tamil":

                caption = translate_text(
                    caption_en,
                    "ta"
                )

                tags = translate_tags(
                    tags_en,
                    "ta"
                )

            elif language == "Hindi":

                caption = translate_text(
                    caption_en,
                    "hi"
                )

                tags = translate_tags(
                    tags_en,
                    "hi"
                )

            else:

                caption = caption_en
                tags = tags_en


            # =================================================
            # 4. CREATE RESULT
            # =================================================

            result = (
                f"Caption:\n"
                f"{caption}\n\n"
                f"Tags:\n"
                f"{', '.join(tags)}"
            )


        # =====================================================
        # 5. DISPLAY RESULT
        # =====================================================

        st.success(
            "✅ Image processed successfully!"
        )

        st.text_area(
            "📝 Generated Result",
            result,
            height=220
        )


        # =====================================================
        # 6. PDF DOWNLOAD
        # =====================================================

        try:

            pdf_data = create_pdf(
                result
            )

            st.download_button(
                label="📄 Download Result as PDF",
                data=pdf_data,
                file_name="image_caption_result.pdf",
                mime="application/pdf"
            )

        except Exception as e:

            st.error(
                f"❌ PDF creation failed: {e}"
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 Powered by BLIP + KeyBERT + Google Translator"
)
