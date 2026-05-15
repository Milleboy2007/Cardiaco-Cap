import pigpio
import time
import socket
import json

# --- CONFIGURATION ---
BROCHE_BOUTON = 22 
PORT = 8888
DEST_IP = "192.168.26.1"

# Créer le socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Créer un objet pour l'adresse
dest_addr = (DEST_IP, PORT)

class CalculateurBPMHardware:
    def __init__(self, pi, pin):
        self.pi = pi
        self.pin = pin
        self.historique_clics = []
        self.delai_reinitialisation = 2.5 # Réinitialise après 2.5s sans appui
        
        self.temps_dernier_clic = time.time()
        self.zero_envoye = False 

        # Configuration de la broche
        self.pi.set_mode(self.pin, pigpio.INPUT)
        
        # On active la résistance Pull-Up interne (le bouton connecte à la masse)
        self.pi.set_pull_up_down(self.pin, pigpio.PUD_UP) 
        
        # Filtre anti-rebond (glitch filter) : ignore les changements de moins de 50 ms
        self.pi.set_glitch_filter(self.pin, 50000)

        # Création de l'interruption (callback)
        self.callback_bouton = self.pi.callback(self.pin, pigpio.FALLING_EDGE, self.clic_tap)
        print(f"Système prêt sur le GPIO {self.pin}. Tapote le bouton en rythme !")

    def clic_tap(self, gpio, level, tick):
        temps_actuel = time.time()

        self.temps_dernier_clic = temps_actuel
        self.zero_envoye = False

        # Si le dernier clic est trop vieux, on recommence à zéro
        if self.historique_clics and (temps_actuel - self.historique_clics[-1]) > self.delai_reinitialisation:
            self.historique_clics = []
            print("--- Remise à zéro ---")

        self.historique_clics.append(temps_actuel)

        # On garde les 8 derniers clics pour une moyenne réactive
        if len(self.historique_clics) > 8:
            self.historique_clics.pop(0)

        # Calcul du BPM si on a au moins 2 clics
        if len(self.historique_clics) >= 2:
            differences_temps = []
            for i in range(1, len(self.historique_clics)):
                ecart = self.historique_clics[i] - self.historique_clics[i-1]
                differences_temps.append(ecart)

            moyenne_ecart = sum(differences_temps) / len(differences_temps)
            bpm = 60.0 / moyenne_ecart
            
            print(f"❤️ BPM: {int(bpm)}")
            d = {
                "status": "ready",
                "data": {
                    "value": f"{int(bpm)}",
                    "unite": "BPM"
                }
            }
            sock.sendto(json.dumps(d).encode('utf-8'), dest_addr)
        else:
            print("BPM: -- (Appuie encore)")
            d = {
                "status": "ready",
                "data": {
                    "value": "0",
                    "unite": "BPM"
                }
            }
            sock.sendto(json.dumps(d).encode('utf-8'), dest_addr)

    def verifier_inactivite(self):
        # Si on dépasse 2.5s ET qu'on n'a pas encore envoyé le 0
        if not self.zero_envoye and (time.time() - self.temps_dernier_clic) > self.delai_reinitialisation:
            self.historique_clics = [] # On vide l'historique
            self.zero_envoye = True    # On mémorise l'envoi pour ne pas spammer le réseau
            
            print("--- Timeout : Aucun battement. Envoi BPM 0 ---")
            d = {
                "status": "ready",
                "data": {
                    "value": "0",
                    "unite": "BPM"
                }
            }
            sock.sendto(json.dumps(d).encode('utf-8'), dest_addr)


# --- LANCEMENT ---
if __name__ == "__main__":
    sock.sendto(json.dumps({
        "status": "ready",                          
        "data": {
            "value": "0",
            "unite": "BPM"
        }}).encode(), dest_addr)

    pi = pigpio.pi()
    
    if not pi.connected:
        print("ERREUR : Impossible de se connecter à pigpio.")
        print("As-tu oublié de lancer 'sudo pigpiod' dans le terminal ?")
        exit()

    # Initialisation de notre classe
    calculateur = CalculateurBPMHardware(pi, BROCHE_BOUTON)

    try:
        # Boucle infinie pour garder le programme ouvert
        while True:
            calculateur.verifier_inactivite()
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nArrêt du programme...")
        calculateur.callback_bouton.cancel()
        sock.sendto(json.dumps({
        "status": "not ready",                          
        "data": {
            "value": "0",
            "unite": "BPM"
        }}).encode(), dest_addr)
        pi.stop()
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        sock.sendto(json.dumps({
        "status": "not ready",                          
        "data": {
            "value": "0",
            "unite": "BPM"
        }}).encode(), dest_addr)
        pi.stop()