import socket

Host = "10.78.180.33"
Port = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((Host, Port))
    while True:
        mensaje = input("Ingrese un mensaje (o 'salir' para terminar): ")
        if mensaje.lower() == 'salir':
            break
        s.sendall(mensaje.encode())
        data = s.recv(1024)
        print(f"Respuesta del servidor: {data.decode()}")
