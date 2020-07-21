#!/usr/bin/env python3.7


#GPIO's
DHT11_PIN=26
K1_FAN=20
K2_HUMIDIFIER=21
K2_OZONE=16


def FAN_ON():
    '''Prender Ventilador'''
    print("Ventilador ON")
    return ()
def HUMIDIFIER_ON():
    """Prender humidificador"""
    print("HUMIDIFICADOR ON")
    return ()
def OZONE_ON():
    """Prender generador de ozono"""
    print("OZONE ON")
    return ()
def FAN_OFF():
    '''Apagar Ventilador'''
    print("Ventilador OFF")
    return ()
def HUMIDIFIER_OFF():
    """Apagar humidificador"""
    print("HUMIDIFICADOR OFF")
    return ()
def OZONE_OFF():
    """Apagar generador de ozono"""
    print("OZONE OFF")
    return ()
def GET_LECTURE():
    """Obtiene lecturas de los sensores"""
    print("Getting data...")
    Ozone_Measure=121 #TEST VALUE
    Temp_Measure=25 #TEST VALUE
    Hum_Measure=60 #TEST VALUE
    return (Ozone_Measure,Temp_Measure,Hum_Measure)
def GATE_OPEN():
    ''' Abre la compuerta del filtro de ozono'''
    print("Opening gate...")
    return()
def GATE_CLOSE():
    '''Cierra la compuerta del filtro de ozono'''
    print("Closing gate...")
    return()