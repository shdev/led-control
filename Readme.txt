 _      _____ _____  ______                      
| |    |  __ \_   _|/ __ \ \                    
| |    | |  | || | | |  | \ \                   
| |    | |  | || | | |  | |\ \                  
| |____| |__| || |_| |__| | \ \                 
|______|_____/_____|_____/   \_\                

LED Server - Steuerung eines LED-Strips über einen Raspberry Pi

Voraussetzungen:
- Raspberry Pi mit Raspbian (Debian 11.6)
- Python 3 installiert
- Neopixel-Python-Bibliothek installiert

Installation:
1. Repository klonen oder Dateien kopieren:
    git clone <repository-url> /home/pi/led_strip_server
    cd /home/pi/led_strip_server

2. Python-Abhängigkeiten installieren:
    pip install rpi_ws281x adafruit-circuitpython-neopixel flask

3. Konfigurationsdatei erstellen:
    Erstellen Sie die Datei config.json im Verzeichnis /home/pi/led_strip_server:
    {
        "HOST": "0.0.0.0",
        "PORT": 5000,
        "LED_COUNT": 56,
        "LED_PIN": "D18"
    }

4. Installationsskript ausführen:
    sudo ./install.sh

Verwaltung des Dienstes:
- Dienst starten:
    sudo systemctl start ledserver

- Dienst stoppen:
    sudo systemctl stop ledserver

- Dienst neu starten:
    sudo systemctl restart ledserver

- Dienststatus überprüfen:
    sudo systemctl status ledserver

- Dienst beim Systemstart aktivieren:
    sudo systemctl enable ledserver

- Dienst beim Systemstart deaktivieren:
    sudo systemctl disable ledserver

Verwendung der Web-API:
1. Setzen einer Farbe:
    - Endpunkt: /set_color
    - Methode: POST
    - Daten:
    {
        "color": [255, 0, 0]  // RGB-Wert
    }
    - Beispiel:
    curl -X POST http://<your-ip>:5000/set_color -H "Content-Type: application/json" -d '{"color": [255, 0, 0]}'

2. LED-Strip löschen:
    - Endpunkt: /clear
    - Methode: POST
    - Beispiel:
    curl -X POST http://<your-ip>:5000/clear -H "Content-Type: application/json"

3. Color Wipe Animation:
    - Endpunkt: /color_wipe
    - Methode: POST
    - Daten:
    {
        "color": [0, 255, 0],  // RGB-Wert
        "wait_ms": 50          // Wartezeit in Millisekunden
    }
    - Beispiel:
    curl -X POST http://<your-ip>:5000/color_wipe -H "Content-Type: application/json" -d '{"color": [0, 255, 0], "wait_ms": 50}'

4. Theater Chase Animation:
    - Endpunkt: /theater_chase
    - Methode: POST
    - Daten:
    {
        "color": [0, 0, 255],  // RGB-Wert
        "wait_ms": 50,         // Wartezeit in Millisekunden
        "iterations": 10       // Anzahl der Iterationen
    }
    - Beispiel:
    curl -X POST http://<your-ip>:5000/theater_chase -H "Content-Type: application/json" -d '{"color": [0, 0, 255], "wait_ms": 50, "iterations": 10}'

5. Rainbow Cycle Animation:
    - Endpunkt: /rainbow_cycle
    - Methode: POST
    - Daten:
    {
        "wait_ms": 20,         // Wartezeit in Millisekunden
        "iterations": 5        // Anzahl der Iterationen
    }
    - Beispiel:
    curl -X POST http://<your-ip>:5000/rainbow_cycle -H "Content-Type: application/json" -d '{"wait_ms": 20, "iterations": 5}'

Webinterface:
Eine einfache HTML-Seite zur Steuerung des LED-Servers ist ebenfalls enthalten. Um darauf zuzugreifen, öffnen Sie einen Webbrowser und gehen Sie zu:
http://<your-ip>:5000/

Logs überprüfen:
Um die Logs des Dienstes zu überprüfen, verwenden Sie:
    sudo journalctl -u ledserver

Deinstallation:
Um den Dienst zu entfernen, deaktivieren Sie ihn und löschen Sie die Dienstdatei:
    sudo systemctl disable ledserver
    sudo rm /etc/systemd/system/ledserver.service
    sudo systemctl daemon-reload

Fehlerbehebung:
Falls der Dienst nicht startet oder Fehler auftreten, überprüfen Sie die Logs:
    sudo journalctl -u ledserver