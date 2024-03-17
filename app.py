import streamlit as st
import cv2
from pyzbar.pyzbar import decode

def read_qr_code(frame):
    decoded_objects = decode(frame)
    for obj in decoded_objects:
        # Desenha um retângulo ao redor do QR code
        (x, y, w, h) = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Decodifica o conteúdo do QR code
        qr_data = obj.data.decode("utf-8")
        
        # Exibe o conteúdo do QR code
        st.write("QR Code:", qr_data)

def main():
    st.title("Leitor de QR Code com Streamlit")

    # Inicia a captura da câmera
    cap = cv2.VideoCapture(0)

    # Captura um único frame
    ret, frame = cap.read()
    if not ret:
        st.error("Erro ao capturar a imagem da câmera.")

    # Chama a função para ler QR codes
    read_qr_code(frame)

    # Exibe o frame na interface do Streamlit
    st.image(frame, channels="BGR", use_column_width=True)

    # Libera a captura da câmera
    cap.release()

if __name__ == "__main__":
    main()
