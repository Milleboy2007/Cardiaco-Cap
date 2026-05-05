import time

import board

import busio

from adafruit_ads1x15.ads1115 import ADS1115

from adafruit_ads1x15.analog_in import AnalogIn



# Initialisation de l'I2C et de l'ADS1115

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS1115(i2c)

data = AnalogIn(ads, 0)



# Variables de filtrage

alpha = 0.75

old_value = 0.0



# --- Variables pour le calcul des BPM ---

# ⚠️ ATTENTION : Vous DEVEZ ajuster ce seuil en fonction des valeurs "Filtered"

# que vous avez observées dans le script précédent !

SEUIL_BATTEMENT = 16000



dernier_battement = time.time()

bpm_moyen = 0



print("En attente de battements cardiaques...")

print("Appuyez sur Ctrl+C pour quitter.\n")



try:

    while True:

        # 1. Lecture et Filtrage

        raw_value = data.value

        value = (alpha * old_value) + (1.0 - alpha) * raw_value

        temps_actuel = time.time()



        # 2. Détection du battement (dépassement du seuil)

        if value > SEUIL_BATTEMENT:

           

            # Temps écoulé depuis le dernier pic (en secondes)

            temps_ecoule = temps_actuel - dernier_battement

           

            # Anti-rebond : On ignore les pics trop rapprochés (ex: < 0.3s)

            # 0.3 seconde équivaut à un maximum de 200 BPM, un humain normal ne dépasse pas ça au repos

            if temps_ecoule > 0.3:

               

                # 3. Calcul des BPM (60 secondes divisées par le temps entre 2 battements)

                bpm_instantane = (60.0 / temps_ecoule) - 100

               

                # On s'assure que la valeur est réaliste (entre 40 et 200 BPM)

                if 40 <= bpm_instantane <= 200:

                    print(f"❤️ BATTEMENT ! | Temps: {temps_ecoule:.2f}s | BPM: {bpm_instantane:.0f}")

               

                # Mise à jour du chronomètre pour le prochain battement

                dernier_battement = temps_actuel



        # Mise à jour de l'état pour la boucle suivante

        old_value = value

        time.sleep(0.05) # Pause de 50ms



except KeyboardInterrupt:

    print("\nArrêt du programme.")