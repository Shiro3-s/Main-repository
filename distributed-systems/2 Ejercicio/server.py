import socket

host = "10.78.180.33"
port = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    print(f"Servidor escuchando en {host}:{port}")
    conn, addr = s.accept()
    with conn:
        print(f"Conexión establecida con {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Mensaje recibido: {data.decode()}")
            respuesta = f"Mensaje '{data.decode()}' recibido"
            conn.sendall(respuesta.encode())  # Echo back the received message