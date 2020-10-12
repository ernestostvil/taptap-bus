import RPi.GPIO as io
import unirest
import time
import socket
from RestAPI import RestAPI
from GPS import GpsPoller
from entities import Autobus, Chequeo, Coordenada, Parada

io.setmode(io.BCM)
io.setwarnings(False)

# boton_subida = 5
# led_subida = 6

# boton_bajada = 23
# led_bajada = 24
io.setup(5, io.IN, pull_up_down = io.PUD_DOWN)
io.setup(6, io.OUT)

io.setup(23, io.IN, pull_up_down = io.PUD_DOWN)
io.setup(24, io.OUT)

# getting the serial number
def getserial():
    # Extract serial from cpuinfo file

    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial

# autobus = Autobus.Autobus()
numeroSerial = getserial()

# main variable
man = 0
status = 0
restAPI = RestAPI()
chequeos = []
contadorDeNodeteccion = 0

gpsc = GpsPoller()  # create the thread
gpsc.start()  # start it up

cont = 0
estadoActual = True

verificadorDeEstado = 0
currentCoordenada = None

def boton_subida_presionado(channel):
    global man
    global  contadorDeNodeteccion
    global status
    man += 1
    if man > 100:
        man = 100
    print " detecto una subida%d " % (man)

    # registrando un chequeo
    chequeo = Chequeo.Chequeo()
    chequeo._esEntrada = True

    chequeo._fechaRegistrada = int(time.time())
    coordenada = Coordenada.Coordenada()

    gpsd = GpsPoller()
    gpsd.start()
    # time.sleep(1)

    coordenada.latitude = gpsd.fix.latitude
    coordenada.longitud = gpsd.fix.longitude
    gpsd.stopController()
    parada = Parada.Parada()

    parada.coordenada = coordenada
    chequeo.parada = parada
    # chequeo.parada.coordenada.longitud=coordenada.longitud
    # chequeo.parada.coordenada.latitude=coordenada.latitude
    chequeos.append(chequeo)

    status = 1
    contadorDeNodeteccion = 0
    io.output(6, True)
    time.sleep(5)
    io.output(6, False)
def boton_bajada_presionado(channel):
    global status
    global contadorDeNodeteccion
    global man
    man -= 1
    if man < 0:
        man = 0
    print "detecto una bajada %d" % (man)
    # registrando un chequeo
    chequeo = Chequeo.Chequeo()
    chequeo._esEntrada = True

    chequeo._fechaRegistrada = int(time.time())
    coordenada = Coordenada.Coordenada()

    gpsd = GpsPoller()
    gpsd.start()
    # time.sleep(1)

    coordenada.latitude = gpsd.fix.latitude
    coordenada.longitud = gpsd.fix.longitude
    gpsd.stopController()

    parada = Parada.Parada()
    parada.coordenada = coordenada
    chequeo.parada = parada
    chequeos.append(chequeo)
    status = 1
    contadorDeNodeteccion = 0
    io.output(24, True)
    time.sleep(3)
    io.output(24, False)

io.add_event_detect(5, io.RISING, callback=boton_subida_presionado, bouncetime=5000)
io.add_event_detect(23, io.RISING, callback=boton_bajada_presionado, bouncetime=3000)

while 1:
    cont += 1
    verificadorDeEstado += 1
    if (cont == 5):
        try:
            coor = Coordenada.Coordenada()
            coor.latitude = gpsc.fix.latitude
            coor.longitud = gpsc.fix.longitude

            print(gpsc.fix.latitude)

            restAPI.postUbicacion(getserial(), coor, int(time.time()))
            cont = 0
            if verificadorDeEstado == 5:
                currentCoordenada = coor
            if verificadorDeEstado == 300:
                if round(coor.latitude, 4) == round(currentCoordenada.latitude, 4) or round(coor.longitud, 4) == round(
                        currentCoordenada.longitud, 4):
                    estadoActual = False
                    restAPI.postEstadoActualAndRuta(numeroSerial, coor, estadoActual, int(time.time()))
                    verificadorDeEstado = 0
                else:
                    estadoActual = True
                    restAPI.postEstadoActualAndRuta(numeroSerial, coor, estadoActual, int(time.time()))
                    verificadorDeEstado = 0
        except:
            cont = 0
            pass

    # if io.input(5) == True:
    #     man += 1
    #     if man > 100:
    #         man = 100
    #     print " detecto una subida%d " % (man)
    #
    #     # registrando un chequeo
    #     chequeo = Chequeo.Chequeo()
    #     chequeo._esEntrada = True
    #
    #     chequeo._fechaRegistrada = int(time.time())
    #     coordenada = Coordenada.Coordenada()
    #
    #     gpsd = GpsPoller()
    #     gpsd.start()
    #     # time.sleep(1)
    #
    #     coordenada.latitude = gpsd.fix.latitude
    #     coordenada.longitud = gpsd.fix.longitude
    #     gpsd.stopController()
    #     parada = Parada.Parada()
    #
    #     parada.coordenada = coordenada
    #     chequeo.parada.coordenada.longitud=coordenada.longitud
    #     chequeo.parada.coordenada.latitude=coordenada.latitude
    #     chequeos.append(chequeo)
    #     print chequeo.parada.coordenada.latitude
    #     print chequeo.parada.coordenada.longitud
    #
    #     status = 1
    #     contadorDeNodeteccion = 0
    #elif io.input(23) == 1:
        # man -= 1
        # if man < 0:
        #     man = 0
        # print "detecto una bajada %d" % (man)
        # # registrando un chequeo
        # chequeo = Chequeo.Chequeo()
        # chequeo._esEntrada = True
        #
        # chequeo._fechaRegistrada = int(time.time())
        # coordenada = Coordenada.Coordenada()
        #
        # gpsd = GpsPoller()
        # gpsd.start()
        # # time.sleep(1)
        #
        # coordenada.latitude = gpsd.fix.latitude
        # coordenada.longitud = gpsd.fix.longitude
        # gpsd.stopController()
        #
        # parada = Parada.Parada()
        # parada.coordenada = coordenada
        # chequeo.parada = parada
        # chequeos.append(chequeo)
        # status = 1
        # contadorDeNodeteccion = 0
    elif io.input(6) == 0 or io.input(23) == 0:
        print "no dectetado"
        contadorDeNodeteccion += 1
        status = 0
    time.sleep(3)
    print (contadorDeNodeteccion)
    if (contadorDeNodeteccion == 20):
        for chequeodetectado in chequeos:
            restAPI.postChequeos(chequeodetectado, numeroSerial)
        contadorDeNodeteccion = 0
        chequeos = []

        # actualizando cantidad de pasajeros
        restAPI.postCantidadDePasajerosActual(int(time.time()), man, numeroSerial)

