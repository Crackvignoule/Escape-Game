from kivy.config import Config
from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import sys
import binascii
from math import pow, log
import serial
from functools import partial
Window.size = (500,680)

#Il faut penser à définir comment identifier une trame BLE à partir de quel UUID

def lecture_port():
    ser = serial.Serial(
        port='COM7',
        baudrate=115200,
    )

    while(True):
        ser.close()
        ser.open()
        hexData= ser.readline()
        frame=str(hexData[:-2])[2:-1]
        liste_frame = []
        if frame.startswith("0201041AFF4C0002150005000100001000800000805F9B0131"):
            return frame
            
    ser.close()
def get_rssi(trame_ble):
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
    val = int(val_str, 2)
    b = val.to_bytes(bytes, byteorder=sys.byteorder, signed=False)                                                          
    return int.from_bytes(b, byteorder=sys.byteorder, signed=True)

def get_distance_from_RSSI(RSSI_binaire):
    measured_power=-69     #-61 dVm by default
    RSSI=twos(RSSI_binaire,1)
    N=2 #2(low) à 4(high)
    return 10**((measured_power-RSSI)/(10*N))

def affichage(distance):
    return f'Le capteur BLE est à {round(distance,2)} metres'
        
class Formulaire(Widget):
    txt=ObjectProperty(None)
    img=ObjectProperty(None)

    

    def radar(self, dt):
        trame_ble = lecture_port()
        #print(trame_ble)
        rssi = get_rssi(trame_ble)
        #print(rssi)
        rssi_binaire = convert(rssi,16,2)
        #print(rssi_binaire)
        distance = round(get_distance_from_RSSI(str(rssi_binaire)),2)
        print(distance)
        if distance<1.5:
            self.txt.text="vous êtes très proche!"
            self.img.source="signal4.png"

        elif distance <3:
            self.txt.text="Encore un peu!"
            self.img.source="signal3.png"

        elif distance <4.5:
            self.txt.text="vous vous rapprochez!"
            self.img.source="signal2.png"

        else:
            self.txt.text="vous etes loin!"
            self.img.source="signal1.png"

    
    def update(self):
        Clock.schedule_interval(self.radar,1)
    

class RadarApp(App):
    def build(self):
        return Formulaire()

if __name__ == '__main__':
    RadarApp().run()