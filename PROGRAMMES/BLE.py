
#!authors : FOURNIER Jérémy, PAVY Killian

import sys
import binascii
from math import *
import serial
import time
def lecture_port():
    """Lecture des receptions avec correspondance BLE"""
    ser = serial.Serial(
        port='/dev/serial/by-id/usb-Cypress_Semiconductor_Cypress_KitProg_BLE0A190B1702016400-if02',
        #port = "COM7",
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    while(True):
        hexData= ser.readline()
        frame=str(hexData[:-2])[2:-1]
        if len(frame)==60:
            print(frame)
            if frame.startswith("0201041AFF4C00021500050001000010008"):
                return frame

def get_rssi(trame_ble):
    """Déduction du RSSI dans la trame receptionné"""
    rssi = trame_ble[58:]
    return rssi

def convert(nbr, old_base, new_base):
    '''
    Convert a number from one base to another

    :param nbr: the number to convert
    :param old_base: the base of the number we are converting from
    :param new_base: the base you want to convert to
    :return: The converted number.
    '''
    " nbr est un str, old_base et new_base des entiers "
    chiffres = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    nbr_dec = 0
    i = len(nbr) - 1
    for x in nbr:
        nbr_dec += chiffres.index(x) * int(pow(old_base, i))
        i -= 1
    nbr_chars = int(log(nbr_dec)/log(new_base) + 1)
    nbr_final = ""
    for i in range(0, nbr_chars):
        x = int(nbr_dec / pow(new_base, nbr_chars-1-i))
        nbr_dec -= int(x * pow(new_base, nbr_chars-1-i))
        nbr_final += chiffres[x]
    return nbr_final

def twos(val_str, bytes):
    """Complément à 2"""
    val = int(val_str, 2)
    b = val.to_bytes(bytes, byteorder=sys.byteorder, signed=False)                                                          
    return int.from_bytes(b, byteorder=sys.byteorder, signed=True)

def get_distance_from_RSSI(RSSI_binaire):
    """Déduction distance par rapport au RSSI"""
    measured_power=-69     #-61 dVm by default
    RSSI=twos(RSSI_binaire,1)
    N=2 #2(low) à 4(high)
    return 10**((measured_power-RSSI)/(10*N))

def main():
    while True:
        print("SCAN DE L'ENVIRONNEMENT EN COURS")
        trame_ble = lecture_port()
        #print(trame_ble)
        rssi = get_rssi(trame_ble)
        #print(rssi)
        rssi_binaire = convert(rssi,16,2)
        #print(rssi_binaire)
        distance = round(get_distance_from_RSSI(str(rssi_binaire)),2)
        print(">> Vous etes à "+str(distance) + "m de l'émetteur !")
        print(" "*50)

if __name__=='__main__':
    main()