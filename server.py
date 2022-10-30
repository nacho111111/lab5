from socket import *
from Crypto.Cipher import DES
from secrets import token_bytes


# funciones
def escribirArchivo(nombre_archivo,cifrado):
    archivo = open(nombre_archivo, "w")
    archivo.write(cifrado+"    "+"\n")
    archivo.close()

def descifrar(nonce,textocifrado,tag):
    cifrado = DES.new(key, DES.MODE_EAX, nonce = nonce)
    textoplano = cifrado.decrypt(textocifrado)

    try:
        cifrado.verify(tag)
        return textoplano.decode('ascii')
    except:
        return False
#/funciones

print("Intercambio de clave segura mediante Diffe y Hellman \n")

print("Hola bienvenido al sistema de generacion de clave de sesion")

nombre=input("\n Ingresa tu nombre: ")

print("Esperando a un cliente :)")


# conexion cliente servidor
direccionServidor = "localhost"
PuertoServidor = 9099

#generar sockets
socketServidor = socket(AF_INET, SOCK_STREAM)
#establecer conexion

socketServidor.bind( ( direccionServidor, PuertoServidor ) )
socketServidor.listen()

while True:
	#establecer conexion
	socketConexion, addr = socketServidor.accept()
	print("conectado con un cliente", addr)
	while True:
		b=int(input(nombre + " ingresa tu clave privada: "))
		#recivir mensaje
		g = socketConexion.recv(4096).decode()
		socketConexion.send("recibido".encode())
		p = socketConexion.recv(4096).decode()
		socketConexion.send("recibido".encode())
		A = socketConexion.recv(4096).decode()
		g = int(g)	
		p = int(p)
		A = int(A)
		B = (g**b)% p # clave publica B
		print(nombre + " tu clave publica es: ",B)
		B = str(B)
		socketConexion.send(B.encode())

		B = int(B)
		k = (A**b)% p
		# terminar programas
		print(nombre+ " la clave de sesion es: ", k)
		k1 = socketConexion.recv(4096).decode()
		socketConexion.send("recibido".encode())
		k1 = int(k1)
		if k != k1:
			print("No se comprovo la igualdad de condiciones")
			break
		
		#mensaje al cliente
		tag = socketConexion.recv(4096)
		socketConexion.send("recibido".encode())
		textocifrado = socketConexion.recv(4096)
		socketConexion.send("recibido".encode())
		nonce = socketConexion.recv(4096)
		socketConexion.send("recibido".encode())
		key = socketConexion.recv(4096)
		socketConexion.send("recibido".encode())

		desifrado = descifrar(nonce,textocifrado,tag)
		print("mensaje -->",desifrado)
		escribirArchivo("mensajerecibido.txt",desifrado)
		
		break
	print("Desconectado el cliente", addr)
	#cerrar conexion
	socketConexion.close()