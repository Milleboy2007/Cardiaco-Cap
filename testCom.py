import socket

PORT = 8888
DEST_IP = "10.10.22.246"
MESSAGE = "abcdefg!\n"

# Créer le socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Créer un objet pour l'adresse
dest_addr = (DEST_IP, PORT)

# Envoyer le message
sock.sendto(MESSAGE.encode(), dest_addr)

# Fermer le socket
sock.close()