import streamlit as st
import requests
import time
import base64
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Download NF-e - Meu Danfe",
    layout="centered"
)

st.title("⬇️ Download automático de NF-e (PDF)")

API_KEY = "38a1c60c-75e1-452c-aa8f-91b1493440b7"

HEADERS = {
    "accept": "application/json",
    "Api-Key": API_KEY
}

chave = st.text_input(
    "Chave de Acesso da NF-e (44 dígitos)",
    max_chars=44
)

if st.button("Enviar"):
    if not chave or len(chave) != 44 or not chave.isdigit():
        st.error("Informe uma chave válida com 44 números.")
    else:
        # ==============================
        # Número da NF-e (posições 26–34)
        # ==============================
        numero_nf = chave[25:34]

        # ==============================
        # 1️⃣ Solicita NF-e
        # ==============================
        url_add = f"https://api.meudanfe.com.br/v2/fd/add/{chave}"

        with st.spinner("Solicitando NF-e..."):
            response_add = requests.put(url_add, headers=HEADERS)
            time.sleep(1)

        if response_add.status_code != 200:
            st.error("Erro ao solicitar NF-e")
            st.text(response_add.text)
        else:
            # ==============================
            # 2️⃣ Baixar PDF
            # ==============================
            url_pdf = f"https://api.meudanfe.com.br/v2/fd/get/da/{chave}"

            with st.spinner("Baixando PDF..."):
                response_pdf = requests.get(url_pdf, headers=HEADERS)

            if response_pdf.status_code != 200:
                st.error("Erro ao baixar PDF")
                st.text(response_pdf.text)
            else:
                json_pdf = response_pdf.json()
                pdf_base64 = json_pdf.get("data")

                if not pdf_base64:
                    st.error("PDF não encontrado na resposta da API.")
                else:
                    # ==============================
                    # DOWNLOAD AUTOMÁTICO (JS)
                    # ==============================
                    file_name = f"NF{numero_nf}.pdf"

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