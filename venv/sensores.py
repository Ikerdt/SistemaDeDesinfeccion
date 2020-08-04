#!/usr/bin/env python3.7
import time,board,adafruit_dht,wiringpi


#GPIO's
DHT11_PIN=26
K1_FAN=20
K2_HUMIDIFIER=21
K2_OZONE=16
K1=19
IN1_MOTOR=12
IN2_MOTOR=13
BEEPER=6



def FAN_ON():
    global dhtDevice
    '''Prender Ventilador'''
    wiringpi.wiringPiSetupGpio()  # For GPIO pin numbering
    wiringpi.pinMode(K1_FAN, 1)       # Set pin 6 to 1 ( OUTPUT )
    wiringpi.pinMode(K2_HUMIDIFIER, 1) 
    wiringpi.pinMode(K2_OZONE, 1) 
    wiringpi.pinMode(K1, 1) 
    wiringpi.pinMode(IN1_MOTOR, 1) 
    wiringpi.pinMode(IN2_MOTOR, 1) 
    wiringpi.pinMode(BEEPER, 1) 
    dhtDevice = adafruit_dht.DHT11(board.D26)
    print("Ventilador ON")
    wiringpi.digitalWrite(K1_FAN, 1)
    return ()
def HUMIDIFIER_ON():
    """Prender humidificador"""
    wiringpi.digitalWrite(K2_HUMIDIFIER, 1)
    print("HUMIDIFICADOR ON")
    return ()
def OZONE_ON():
    """Prender generador de ozono"""
    wiringpi.digitalWrite(K2_OZONE, 1)
    print("OZONE ON")
    return ()
def FAN_OFF():
    '''Apagar Ventilador'''
    wiringpi.digitalWrite(K1_FAN, 0)
    print("Ventilador OFF")
    return ()
def HUMIDIFIER_OFF():
    """Apagar humidificador"""
    wiringpi.digitalWrite(K2_HUMIDIFIER, 0)
    print("HUMIDIFICADOR OFF")
    return ()
def OZONE_OFF():
    """Apagar generador de ozono"""
    wiringpi.digitalWrite(K2_OZONE, 0)
    print("OZONE OFF")
    return ()
def GET_LECTURE():
    global Temp_Measure,Hum_Measure,Ozone_Measure,dhtDevice
    """Obtiene lecturas de los sensores"""
    print("Getting data...")
    Ozone_Measure=21 #TEST VALUE
    try:
        Temp_Measure=dhtDevice.temperature 
        Hum_Measure=dhtDevice.humidity 
    except RuntimeError as error:
        print(error.args[0])
        
    return (Ozone_Measure,Temp_Measure,Hum_Measure)
def Beeper_ON():
    '''Timbra'''
    wiringpi.digitalWrite(BEEPER, 1)
    print("Beep...")
    return()
def Beeper_OFF():
    '''Cancela el timbre'''
    wiringpi.digitalWrite(BEEPER, 0)
    print("...")
    return()  

def Right_Motor():
	wiringpi.digitalWrite (IN1_MOTOR, 1);
	wiringpi.digitalWrite (IN2_MOTOR, 0);
def Left_Motor():
	wiringpi.digitalWrite (IN1_MOTOR, 0);
	wiringpi.digitalWrite (IN2_MOTOR, 1);
def Stop_Motor():
	wiringpi.digitalWrite (IN1_MOTOR, 0);
	wiringpi.digitalWrite (IN2_MOTOR, 0);
def GATE_OPEN():
    ''' Abre la compuerta del filtro de ozono'''
    print("Opening gate...")
    return()
def GATE_CLOSE():
    '''Cierra la compuerta del filtro de ozono'''
    print("Closing gate...")
    return()
