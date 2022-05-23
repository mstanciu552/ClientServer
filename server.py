import ast
import uuid
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "localhost"
PORT1 = 8000
PORT2 = 8001

state = {}


class ServerUUID(BaseHTTPRequestHandler):
    def do_POST(self):
        self.server_version = "HTTP/1.1"

        # Get body content from request
        length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(length).decode("utf-8")
        body = ast.literal_eval(body)

        # Extract UUID
        if not body["uuid"]:
            self.send_response(500)
            self.wfile.write(
                str({"success": False, "error": "[!] Invalid uuid sent"}).encode(
                    "utf-8"
                )
            )
            return
        sent_uuid = str(body["uuid"])
        if sent_uuid in state:
            generated_unique = state[sent_uuid]
        else:
            generated_unique = str(uuid.uuid4())

        self.send_response(200)

        # Remember pairs
        if sent_uuid not in state:
            state[sent_uuid] = generated_unique

        self.wfile.write(
            str({"success": True, "unique": generated_unique}).encode("utf-8")
        )


class ServerMessage(BaseHTTPRequestHandler):
    def do_POST(self):
        self.server_version = "HTTP/1.1"

        # Get body content from request
        length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(length).decode("utf-8")
        body = ast.literal_eval(body)

        # Get fields of body
        try:
            uuid = str(body["uuid"])
            unique = str(body["unique"])
            text = str(body["text"])
        except KeyError:
            self.send_response(500)
            self.wfile.write(
                str({"success": False, "error": "[!] Invalid body parameters"}).encode(
                    "utf-8"
                )
            )
            return

        if uuid not in state:
            res = {"success": False, "error": "[!] UUID unrecognized"}
        else:
            if state[uuid] != unique:
                res = {"success": False, "error": "[!] Invalid unique"}
            else:
                res = {"success": True}

                # Save text message to log file
                with open("logs.txt", "a") as file:
                    file.write(text)
                    file.write("\n")

        if res["success"]:
            self.send_response(200)
        else:
            self.send_response(500)

        self.wfile.write(str(res).encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT1), ServerUUID)
    print(f"[*] Server started on socket ({HOST}, {PORT1})")

    server_message = HTTPServer((HOST, PORT2), ServerMessage)
    print(f"[*] Server started on socket ({HOST}, {PORT2})")

    th_8000 = Thread(target=server.serve_forever)
    th_8001 = Thread(target=server_message.serve_forever)

    try:
        th_8000.start()
        th_8001.start()
    except KeyboardInterrupt:
        th_8000.join()
        server.server_close()
        th_8001.join()
        server_message.server_close()
