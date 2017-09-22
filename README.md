````
                                                       _       _           _   
                        ___ ___  _ __ ___  _   _ _ __ (_) ___ | |__   ___ | |_ 
                       / __/ _ \| '_ ` _ \| | | | '_ \| |/ _ \| '_ \ / _ \| __|
                      | (_| (_) | | | | | | |_| | | | | | (_) | |_) | (_) | |_ 
                       \___\___/|_| |_| |_|\__,_|_| |_|_|\___/|_.__/ \___/ \__|
                      
                 Programm zur automatisierten Vergabe von Prämien nach einem Spieltag.
````

## Installation auf Windows
Auf dem System muss Python 3.x mit den Pythonmodulen requests und wxPython installiert sein.<br>
Zuerst Python 3.x installieren: https://www.python.org/downloads/<br>
Wichtig, den Haken bei 'Add Python 3.x to PATH' setzen:<br>
<img width="50%" src=http://otree.readthedocs.io/en/latest/_images/py-win-installer.png /> <br>
Anschließend cmd Shell öffnen und 'python --version' eingeben, um sicherzustellen, dass Python korrekt installiert ist. Das Ergebnis sollte folgendermaßen aussehen:<br>
<img src="https://raw.githubusercontent.com/nliakm/comuniobot/master/ReadmeImages/cmdPythonVersion.png" /><br>
Als letztes requests und wxPython mit folgendem Befehl installieren:<br>
<img src="https://raw.githubusercontent.com/nliakm/comuniobot/master/ReadmeImages/pythonInstallRequestAndWxPython.png" />
Nun sind alle Voraussetzungen installiert und das Programm kann gestartet werden. 

## Ausführung
Das Projekt klonen und anschließend die Datei ComunioBot.py ausführen
### Login
Zum Login einfach Benutzername und Passwort in die entsprechenden Felder eingeben und einloggen.
Nach ein paar Sekunden wird es eine Rückmeldung geben, ob der Login erfolgreich war.
### Einstellungen vornehmen
#### Modus
Über den Tab Modus kann man folgende Einstellungen vornehmen:<br><br>
1. Feste Praemien<br>
Hier werden pro Platzierung feste Beträge dem jeweiligen Spieler gutgeschrieben.<br><br>
2. Punkte basiert<br>
Hier werden die Punkte mit einem selbst definierbaren Wert multipliziert, dessen Ergebnis die Prämie des jeweiligen Spielers ist.
#### Datei
Über den Tab "Datei" kann man folgende Einstellungen vornehmen:<br><br>
1. Letzte Platzierung fuer Prämie<br>
Dieser Wert legt fest, bis zu welcher Platzierung (ausgehend von Platz 1) Prämien vergeben werden sollen.<br><br>
2. Feste Prämien setzen<br>
Hier lässt sich einstellen, welche Platzierung welchen festen Betrag als Prämie bekommt (sofern der Modus 'Feste Prämien' aktiv ist)<br><br>
3. Multiplikator anpassen<br>
Hier kann man den Multiplikator einstellen, der mit den Punkten eines Spielers multipliziert wird, dessen Ergebnis die Prämie ist (sofern der Modus 'Punkte basiert' aktiv ist))<br><br>
4. Auf Updates prüfen<br>
Checken, ob eine aktuellere Version verfügbar ist. Wenn ja, im Dialogfenster den Download bestätigen. Die neue Version wird als .zip in den aktuellen Ordner gedownloadet. Einfach entpacken (optional die alten Konfigurationsdateien in den neuen Ordner ziehen) und starten.

## Troubleshooting
Sollte in der cmd-Shell der Befehl python nicht gefunden werden, ist normalerweise die Umgebungsvariable für Python nicht (korrekt) gesetzt.<br>
Dies tut man manuell folgendermaßen:<br>
<img src="https://raw.githubusercontent.com/nliakm/comuniobot/master/ReadmeImages/pythonInstallationWin10PS.png" /> <br><br>
