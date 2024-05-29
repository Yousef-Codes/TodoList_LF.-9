# TodoList_LF.-9


**Netzwerkkonfiguration**  
Öffne die Datei `/etc/dhcpcd.conf` mit einem Texteditor wie `nano`:  
```bash
sudo nano /etc/dhcpcd.conf
```  
Füge folgende Zeilen am Ende der Datei hinzu, um eine statische IP-Adresse zu konfigurieren:  
```plaintext
interface eth0
static ip_address=192.168.24.132
static routers=192.168.1.1
static domain_name_servers=5000
```

**Benutzer erstellen**  
Erstelle den Benutzer "willi" ohne Administratorrechte:  
```bash
sudo adduser willi
```  
Erstelle den Benutzer "fernzugriff" mit sudo-Rechten:  
```bash
sudo adduser fernzugriff
sudo usermod -aG sudo fernzugriff
```

**SSH-Dienst einrichten**  
Installiere den SSH-Server:  
```bash
sudo apt-get update
sudo apt-get install openssh-server
```  
Konfiguriere den SSH-Dienst, um nur den Benutzer "fernzugriff" zuzulassen:  
```bash
sudo nano /etc/ssh/sshd_config
```  
Ändere die Zeile `PermitRootLogin` zu `PermitRootLogin no` und füge `AllowUsers fernzugriff` hinzu.  

Starte den SSH-Dienst neu:  
```bash
sudo systemctl restart sshd
```

**Docker installieren**  
Installiere Docker und Docker Compose:  
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
```

**Web-App deployen**  
Klonen das Git-Repository mit der Web-App:  
```bash
git clone 
```  
Navigiere in das Verzeichnis:  
```bash
cd ToDoList_ifa22
```  
Starte die Web-App mit Docker Compose:  
```bash
sudo docker-compose up -d
```  
Die Web-App ist nun unter `http://192.168.24.132:5000` erreichbar.

**Git-Befehle**  
Klonen des Repositories:  
```bash
git clone https://github.com/FaresCodeDev/ToDoList_ifa22.git
```  
Pullen der neuesten Änderungen:  
```bash
git pull
```  
Committen von Änderungen:  
```bash
git add .
git commit -m "Commit-Nachricht"
```  
Pushen von Änderungen:  
```bash
git push
```
