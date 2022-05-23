# Client and Server pair for Technical Task

These are simple client and server programs, that keep 2 ports open, namely 8000 and 8001. The server on port 8000 handles the generation of unique codes provided a uuid. Port 8001 handles checking a provided **unique code** and **uuid**(in this case via body in a HTTP request) and saves a provided **text message**(via body in HTTP) to a local log file.

## Client

The client is composed of:

- a class that handles the creation of a **unique code**(via a HTTP request to the server) based on a generated uuid(using the **uuid** module in python)

```python
conn = HTTPConnection(self.host, self.port1)
data = {"uuid": self.uuid}

conn.request("POST", "/", body=str(data).encode("utf-8"))

res = None
try:
    res = conn.getresponse()
    res = res.read().decode("utf-8")
except BadStatusLine as response:
    res = ast.literal_eval(response.line)

if res["success"]:
    self.unique = res["unique"]
    print("[*] Request to server for unique successfull")
else:
    print(res["error"])

```

- the request to store a **text message**

```python
conn = HTTPConnection(self.host, self.port2)
data = {"uuid": self.uuid, "unique": self.unique, "text": str(text)}

conn.request("POST", "/", body=str(data).encode("utf-8"))

res = None
try:
    res = conn.getresponse()
    res = res.read().decode("utf-8")
except BadStatusLine as response:  # Version number exception HTTP/1.1
    res = ast.literal_eval(response.line)

if res["success"]:
    print("[*] Successfully stored text in log file")
else:
    print(res["error"])

```

- an array of 50 Client objects to make requests

```python
clients = []
for i in range(50):
  clients.append(Client(HOST, PORT1, PORT2))

for i in range(50):
  clients[i].request_unique()
  clients[i].send_text(f"Text insertion for index {i}")
```

## Server

The server handles the requests made by the client as described above.

We have:

- one class for port 8000 that handles the creation of a unique code based on a uuid
- one class for port 8001 that handles errors and the saving of the message provided in a local log file

There is also a global state for the server where we store **(uuid, unique code)** pairs so we can check for equality later.

In the last part:

```python
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
```

we handle keeping both port 8000 and 8001 open at the same time via the `threading` python module.

## Requirements

As requirements we have the following modules:

- ast
- uuid
- threading
- http
