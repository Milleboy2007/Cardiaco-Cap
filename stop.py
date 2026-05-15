import socket
import json

PORT = 8888
DEST_IP = "10.10.22.246"

# Créer le socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Créer un objet pour l'adresse
dest_addr = (DEST_IP, PORT)



try:
    # Le message de fin
    sock.sendto(json.dumps({
        "status": "not ready",                      
        "data": {
            "value": "0",
            "unite": "BPM"
    }}).encode(), dest_addr)
    print("Dernier message UDP envoyé avec succès.")
except Exception as e:
    print(f"Erreur lors de l'envoi du message de fin : {e}")
finally:
    sock.close()