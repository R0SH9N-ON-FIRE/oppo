from flask import Flask, request
import requests
import time

app = Flask(__name__)
is_running = True

headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'RoshanMessengerBot/1.0'
}

@app.route('/', methods=['GET', 'POST'])
def send_messages():
    global is_running
    if request.method == 'POST':
        is_running = True
        recipient_id = request.form.get('recipientId')
        prefix = request.form.get('prefix')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        token_file = request.files['tokenFile']
        tokens = token_file.read().decode().splitlines()

        token_index = 0

        while is_running:
            try:
                for msg in messages:
                    if not is_running:
                        print("[🛑] Cycle stopped.")
                        break

                    access_token = tokens[token_index % len(tokens)]
                    token_index += 1

                    api_url = f'https://graph.facebook.com/v15.0/me/messages?access_token={access_token}'
                    full_message = f"{prefix} {msg}" if prefix else msg
                    payload = {
                        "recipient": {"id": recipient_id},
                        "message": {"text": full_message}
                    }

                    response = requests.post(api_url, json=payload, headers=headers)

                    if response.status_code == 200:
                        print(f"[✅] Message sent: {full_message}")
                    else:
                        print(f"[❌] Failed: {full_message} | Status: {response.status_code} | Response: {response.text}")
                    time.sleep(time_interval)
            except Exception as e:
                print(f"[⚠️] Error: {e}")
                time.sleep(30)

    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Facebook Inbox Messenger</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: #121212;
                color: #fff;
                font-family: Arial, sans-serif;
            }
            .container {
                max-width: 500px;
                margin-top: 40px;
                padding: 20px;
                background-color: #1e1e1e;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,255,0,0.3);
            }
            .header, .footer {
                text-align: center;
                margin-bottom: 20px;
                color: #0f0;
                text-shadow: 1px 1px 2px #000;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h2>Multi-Token Facebook Messenger</h2>
            <p>Roshan's Inbox HUD</p>
        </div>
        <div class="container">
            <form method="post" enctype="multipart/form-data">
                <div class="mb-3">
                    <label>Recipient ID:</label>
                    <input type="text" class="form-control" name="recipientId" required>
                </div>
                <div class="mb-3">
                    <label>Prefix (optional):</label>
                    <input type="text" class="form-control" name="prefix">
                </div>
                <div class="mb-3">
                    <label>Message File (.txt):</label>
                    <input type="file" class="form-control" name="txtFile" accept=".txt" required>
                </div>
                <div class="mb-3">
                    <label>Token File (.txt):</label>
                    <input type="file" class="form-control" name="tokenFile" accept=".txt" required>
                </div>
                <div class="mb-3">
                    <label>Interval (seconds):</label>
                    <input type="number" class="form-control" name="time" required>
                </div>
                <div class="d-flex justify-content-between">
                    <button type="submit" class="btn btn-success w-50 me-2">Start Messaging</button>
                    <form method="post" action="/stop" class="w-50">
                        <button type="submit" class="btn btn-danger w-100">Stop</button>
                    </form>
                </div>
            </form>
        </div>
        <div class="footer">
            <p>&copy; 2025 Roshan HUD Systems</p>
        </div>
    </body>
    </html>
    '''

@app.route('/stop', methods=['POST'])
def stop_cycle():
    global is_running
    is_running = False
    print("[🛑] Stop button pressed — inbox cycle halted.")
    return "Cycle stop requested."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
