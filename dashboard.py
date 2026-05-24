from flask import Flask, render_template
import socket
import threading

app = Flask(__name__)
attendance_data = []

def receive_data():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen(5)
    while True:
        client, addr = server.accept()
        data = client.recv(1024).decode()
        attendance_data.extend(data.splitlines())
        client.close()

@app.route("/")
def dashboard():
    return render_template("dashboard.html", data=attendance_data)

if __name__ == "__main__":
    threading.Thread(target=receive_data, daemon=True).start()
    app.run(host="0.0.0.0", port=80, debug=True)  # Accessible on network
