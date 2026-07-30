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