# main.py for example
import server

@server.route("/home")
def home():
    return "<h1>Reyette Server</h1>", "text/html"

if __name__ == "__main__":
    reyette_server.run(port=8080, directory=".", chunk_size=256 * 1024)
