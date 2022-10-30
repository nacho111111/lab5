from socket import *
import sys
from Crypto.Cipher import DES
from secrets import token_bytes

key = token_bytes(8)
#funciones
def cifrar(msg):
    cifrado = DES.new(key, DES.MODE_EAX)
    nonce = cifrado.nonce
    textocifrado, tag = cifrado.encrypt_and_digest(msg.encode('ascii'))
    return nonce,textocifrado,tag

def leer_mensaje(nombre_archivo):
    archivo = open(nombre_archivo, "r")
    lineas = archivo.readlines()
    contador = 0
    while contador < len(lineas):
        lineas[contador] = lineas[contador].strip().split("    ")
        contador += 1
    mensaje = lineas[0][0]
    archivo.close()
    return mensaje

#/funciones


print("Intercambio de clave segura mediante Diffe y Hellman \n")

print("Hola bienvenido al sistema de generacion de clave de sesion")

nombre=input("\n Ingresa tu nombre: ")

p=int(input("Hola " + nombre +" ingresa un numero primo: "))
g=int(input( nombre +" ingresa una raiz primitiva del numero primo ingresado: "))
a=int(input(nombre + " ingresa tu clave privada: "))

A = (g**a)% p
print(nombre + " tu clave publica es: ",A,"\n")

p = str(p)
g = str(g)
A = str(A)

# conexion cliente servidor 
IPServidor = "localhost"
puertoServidor = 9099

socketCliente = socket(AF_INET, SOCK_STREAM)
socketCliente.connect((IPServidor,puertoServidor))


# enviar mensaje
socketCliente.send(g.encode())
socketCliente.recv(4096).decode()
socketCliente.send(p.encode())
socketCliente.recv(4096).decode()
socketCliente.send(A.encode())

# recibir emnsaje
B = socketCliente.recv(4096).decode()
p = int(p)
g = int(g)
A = int(A)
B = int(B)	
K = (B**a)% p
print(nombre+ " la clave de sesion es: ", K)
# mandar mensaje secreto
msg = leer_mensaje("mensajeentrada.txt")
K = str(K)
socketCliente.send(K.encode())
socketCliente.recv(4096).decode()

nonce,textocifrado,tag = cifrar(msg)
socketCliente.send(tag)
socketCliente.recv(4096).decode()
socketCliente.send(textocifrado)
socketCliente.recv(4096).decode()
socketCliente.send(nonce)
socketCliente.recv(4096).decode()
socketCliente.send(key)
socketCliente.recv(4096).decode()
print("mensaje secreto enviado")
#cerrar socket
socketCliente.close()
sys.exit()


