# Cardiaco-Cap

May 15 13:40:04 rasp25 start.sh[872]: Traceback (most recent call last):
May 15 13:40:04 rasp25 start.sh[872]:   File "/home/pi/Cardiaco-Cap/btn.py", line 90, in <module>
May 15 13:40:04 rasp25 start.sh[872]:     sock.sendto(json.dumps({
May 15 13:40:04 rasp25 start.sh[872]: OSError: [Errno 101] Network is unreachable
May 15 13:40:04 rasp25 systemd[1]: start.service: Deactivated successfully.
May 15 13:40:05 rasp25 systemd[1]: start.service: Scheduled restart job, restart counter is at 5.
May 15 13:40:05 rasp25 systemd[1]: Stopped start.service - Script de démarrage.
May 15 13:40:05 rasp25 systemd[1]: start.service: Start request repeated too quickly.
May 15 13:40:05 rasp25 systemd[1]: start.service: Failed with result 'start-limit-hit'.
May 15 13:40:05 rasp25 systemd[1]: Failed to start start.service - Script de démarrage.
