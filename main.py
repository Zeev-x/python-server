# main.py for example
import server

target_path = "/reyette"

@server.route("/")
def home():
    return f'<a href="{target_path}" style="text-decoration: none; color: blue;">View Files</a>', "text/html"

if __name__ == "__main__":
    server.run(port=8080, directory=".", chunk_size=256 * 1024, mount_path=target_path)
