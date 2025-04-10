import socket
import json
import subprocess

# Configurazioni
UDP_IP = "0.0.0.0"              # IP locale per il binding del socket
UDP_PORT = 1799                 # no change
REPEATER_NAME = "IR5AY  C"      # Nome del ripetitore (max 8 caratteri)
DEST_CALLSIGN = "IR5AY-12"      # Callsign destinatario atteso (esatto)

# Limiti di lunghezza
REPEATER_NAME = REPEATER_NAME[:8]

# Inizializzazione del socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"[INFO] In ascolto su UDP {UDP_IP}:{UDP_PORT}")

while True:
    try:
        data, addr = sock.recvfrom(1024)  # buffer da 1024 byte
        payload = json.loads(data.decode("utf-8"))

        # Controlla se contiene i campi richiesti e se il destinatario è quello atteso
        if (
            payload.get("type") == "msg"
            and payload.get("dst") == DEST_CALLSIGN
            and "msg" in payload
        ):

            # Rimozione della parte dalla "{" in poi, se presente
            full_msg = str(payload["msg"])
            if "{" in full_msg:
                full_msg = full_msg.split("{")[0].strip()

            message_text = full_msg[:20]  # massimo 20 caratteri
            print(f"{full_msg}\n")

            # Chiamata al programma esterno con i due argomenti
            subprocess.run(
                ["/usr/local/bin/texttransmitd", f"{REPEATER_NAME}", "-text", f"{message_text}"], check=True)
            print(f"[OK] Inviato: '{message_text}' da {addr}")
        else:
            print(f"[IGNORATO] Payload non valido o destinatario errato da {addr}")

    except Exception as e:
        print(f"[ERRORE] {e}")
