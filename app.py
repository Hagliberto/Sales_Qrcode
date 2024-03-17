import streamlit as st
import cv2
import pandas as pd
from datetime import datetime

# DataFrame para armazenar os QR Codes escaneados
df = pd.DataFrame(columns=['Link', 'Data e Hora'])

def read_qr_code(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    qr_decoder = cv2.QRCodeDetector()
    data, bbox, _ = qr_decoder.detectAndDecodeMulti(gray)
    decoded_objects = []
    for d in data:
        decoded_objects.append({'data': d})
    return decoded_objects

def main():
    global df
    
    st.title("Leitor de QR Code")

    st.markdown(
        """
        Este aplicativo permite que você use a câmera do dispositivo para escanear e ler QR Codes.
        Para começar, clique no botão abaixo para capturar uma imagem. Certifique-se de que o QR Code esteja bem visível na imagem capturada.
        """
    )

    cap = cv2.VideoCapture(0) 

    if not cap.isOpened():
        st.error("Erro ao acessar a câmera.")
        return

    st.write("A inicializar a câmera...")

    brightness = st.slider("Ajustar brilho", min_value=0, max_value=100, value=50)

    if st.button("Capturar"):
        ret, frame = cap.read()

        if ret:
            frame = cv2.convertScaleAbs(frame, alpha=brightness / 100)

            decoded_objects = read_qr_code(frame)
            if decoded_objects:
                st.success("QR Code lido com sucesso!")
                process_qr_code(decoded_objects)

            else:
                st.error("Nenhum QR Code encontrado na imagem.")

    cap.release()

def process_qr_code(decoded_objects):
    global df
    
    for obj in decoded_objects:
        link = obj['data']
        df.loc[len(df)] = [link, datetime.now()]

if __name__ == "__main__":
    main()

    # Exibir DataFrame dos QR Codes escaneados
    if not df.empty:
        st.dataframe(df)

        # Botão de download para baixar a planilha
        if st.button("Baixar Planilha"):
            file_name = "qrcodes_scaneados.xlsx"
            df.to_excel(file_name, index=False)
            with open(file_name, "rb") as file:
                btn = st.download_button(label="Clique para baixar", data=file, file_name=file_name, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
