import streamlit as st
import requests
import os
import base64
import streamlit.components.v1 as components
from brazilfiscalreport.danfe import Danfe

# ==============================
# CONFIGURAÇÃO STREAMLIT
# ==============================
st.set_page_config(
    page_title="Download NF-e - DANFE",
    layout="centered"
)

st.title("⬇️ Download automático de NF-e (PDF)")

URL_BASE = "https://prevedello.com.br/nfe/baixar.php?nfe="

# ==============================
# INPUT CHAVE
# ==============================
chave = st.text_input(
    "Chave de Acesso da NF-e (44 dígitos)",
    max_chars=44
)

# ==============================
# BOTÃO
# ==============================
if st.button("Enviar"):
    if not chave or len(chave) != 44 or not chave.isdigit():
        st.error("Informe uma chave válida com 44 números.")
    else:
        try:
            # ==============================
            # Número da NF (posição 26–34)
            # ==============================
            numero_nf = chave[25:34]
            file_name = f"NF{numero_nf}.pdf"
            file_path = os.path.join(os.getcwd(), file_name)

            # ==============================
            # 1️⃣ Baixar XML
            # ==============================
            with st.spinner("Baixando XML da NF-e..."):
                url = f"{URL_BASE}{chave}"
                response = requests.get(url, timeout=30)
                response.raise_for_status()

                xml_content = response.text.strip()

                if not xml_content.startswith("<"):
                    st.error("Resposta não é um XML válido.")
                    st.stop()

            # ==============================
            # 2️⃣ Gerar DANFE (PDF)
            # ==============================
            with st.spinner("Gerando DANFE em PDF..."):
                danfe = Danfe(xml=xml_content)
                danfe.output(file_path)

            # ==============================
            # 3️⃣ Converter PDF para Base64
            # ==============================
            with open(file_path, "rb") as f:
                pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

            # ==============================
            # 4️⃣ DOWNLOAD AUTOMÁTICO
            # ==============================
            html_download = f"""
                <html>
                    <body>
                        <a id="downloadLink"
                           href="data:application/pdf;base64,{pdf_base64}"
                           download="{file_name}">
                        </a>
                        <script>
                            document.getElementById('downloadLink').click();
                        </script>
                    </body>
                </html>
            """

            components.html(html_download, height=0, width=0)

            st.success(f"Download iniciado automaticamente: {file_name}")

            # ==============================
            # 5️⃣ Limpeza (opcional)
            # ==============================
            os.remove(file_path)

        except Exception as e:
            st.error("Erro ao gerar o DANFE")
            st.exception(e)
