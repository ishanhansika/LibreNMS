# LibreNMS


















# LibreNMS Alarm System


## පියවර 1: Python සහ අවශ්‍ය Libraries ඉන්ස්ටෝල් කරගැනීම
ඔබගේ Windows PC එකේ Python ඉන්ස්ටෝල් කරලා නැත්නම් python.org වෙත ගොස් එය ඉන්ස්ටෝල් කරගන්න (ඉන්ස්ටෝල් කරන විට "Add Python to PATH" කියන එක ටික් කරන්න අමතක කරන්න එපා).

දැන් Windows Command Prompt (cmd) හෝ PowerShell විවෘත කර Flask සහ Windows වල සවුන්ඩ් ප්ලේ කිරීමට අවශ්‍ය playsound ලයිබ්‍රරි එක ඉන්ස්ටෝල් කරන්න:

```
pip install flask playsound==1.2.2
```
(සටහන: playsound හි 1.2.2 වර්ෂන් එක Windows වල ඉතා ස්ථාවරව වැඩ කරයි).

## පියවර 2: Alarm Listener Python Script එක සකස් කරගැනීම
ඔබේ පරිගණකයේ ඕනෑම තැනක (උදාහරණයක් ලෙස Desktop එකේ හෝ C Drive එකේ) alarm නමින් ෆෝල්ඩරයක් සාදාගන්න.

ඔබ ඇලට් එකට භාවිත කිරීමට කැමති ශබ්ද ෆයිල් එකක් (උදාහරණයක් ලෙස alarm.wav හෝ alarm.mp3) එකම ෆෝල්ඩරයට දමාගන්න.

ඒ ෆෝල්ඩරය තුළම listener.py නමින් Notepad හෝ VS Code මඟින් අලුත් Python ෆයිල් එකක් සාදා පහත කෝඩ් එක එයට ඇතුළත් කර Save කරන්න:

```
from flask import Flask, request
import winsound
import os

app = Flask(__name__)

# ඔබේ alarm.wav ෆයිල් එක ස්ක්‍රිප්ට් එක තිබෙන ෆෝල්ඩරයේම ඇති බව තහවුරු කරගන්න
SOUND_FILE = "alarm.wav"

@app.route('/alert', methods=['POST'])
def alert_receiver():
    print("-----------------------------------------")
    print("Incoming Alert Request Received!")
    
    try:
        raw_data = request.data.decode('utf-8')
        print(f"Raw Data: {raw_data}")
    except Exception as e:
        print(f"Error reading raw data: {e}")

    print("PLAYING ALARM SOUND FILE (alarm.wav)...")
    try:
        # winsound මඟින් wav ෆයිල් එක ප්ලේ කිරීම (SND_ASYNC යනු සවුන්ඩ් එක යන අතරතුර ප්‍රෝග්‍රෑම් එක බ්ලොක් නොවී තබා ගැනීමටයි)
        if os.path.exists(SOUND_FILE):
            winsound.PlaySound(SOUND_FILE, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            print(f"Error: {SOUND_FILE} not found in the directory!")
    except Exception as e:
        print(f"Sound error: {e}")
            
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
## පියවර 3: Windows Firewall එකෙන් Port 5000 විවෘත කරගැනීම (ඉතා වැදගත්)
LibreNMS සර්වර් එකෙන් එවන Webhook ඉල්ලීම් Windows PC එකට ළඟා වීමට නම් Windows Firewall එක හරහා එම පෝට් එකට ඉඩ දෙන්න ඕන:

Windows Search එකේ Windows Defender Firewall with Advanced Security ටයිප් කර එය විවෘත කරන්න.

වම් පැත්තේ ඇති Inbound Rules මත ක්ලික් කර, දකුණු පැත්තේ ඇති New Rule... තෝරන්න.

Port තෝරා Next කරන්න.

Specific local ports යන්නෙහි 5000 ලෙස දී Next කරන්න.

Allow the connection තෝරා Next කරන්න.

සියලුම ඔප්ෂන්ස් (Domain, Private, Public) ටික් කර තබා Next කරන්න.

නම ලෙස LibreNMS Alarm Port ಎಂದು දී Finish කරන්න.

## පියවර 4: ස්ක්‍රිප්ට් එක Run කිරීම
Command Prompt (cmd) එක විවෘත කර ඔබගේ alarm ෆෝල්ඩරයට යන්න (උදාහරණයක් ලෙස: cd C:\Users\YourName\Desktop\alarm).

ස්ක්‍රිප්ට් එක ක්‍රියාත්මක කරන්න:

```
python listener.py
```

දැන් මෙම Windows PC එකේ Local IP එක (උදාහරණයක් ලෙස 192.168.1.50 වැනි) සහ පෝට් එක (5000) පාවිච්චි කර ඔබට LibreNMS එකෙන් Webhook කනෙක්ට් කරන්න පුළුවන්.

## පියවර 5: LibreNMS හි සැකසීම් කිරීම
ඔබේ LibreNMS Dashboard එකට යන්න.

Alerts -> Alert Transports වෙත ගොස් + Add Transport දෙන්න.

විස්තර පහත පරිදි පුරවන්න:

Transport Name: Windows Local Alarm

Type: Generic Webhook

URL: http://<ඔබේ_Windows_PC_එකේ_IP_ලිපිනය>:5000/alert (උදා: [http://192.168.1.50:5000/alert](http://192.168.1.50:5000/alert))

Save කරන්න.

අවසාන වශයෙන්, ඔබගේ Alert Rules වලට ගොස් අදාළ රූල් එකට මෙම Transport එක සම්බන්ධ (Tick) කරන්න.


