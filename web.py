from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Bot de prisões está ativo!", 200

def iniciar_site():
    app.run(host="0.0.0.0", port=10000)

def manter_site():
    Thread(target=iniciar_site, daemon=True).start()
