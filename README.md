# AtaqueReplayPLC_S7_1200

Este script en Python permite controlar un PLC Siemenes a través del protocolo S7.

## Proporciona funcionalidades para:
    - Encender el PLC.
    - Apagar el PLC.
    - Modificar las salidas digitales del PLC.
## Requisitos
    - Python 3.x
    - Conexión de red con el PLC Siemens
## Uso

Ejecuta el script con los siguientes parámetros:

    python3 replay.py [IP_DEL_PLC] [Acción]

### Acciones disponibles

    - encender: Enciende el PLC
    - apagar: Apaga el PLC
    - modificar [salida] [on|off]: Modifica el estado de una salida digital del PLC

### Ejemplos

Encender el PLC

    python3 replay.py 192.168.1.100 encender

Apagar el PLC

    python3 replay.py 192.168.100 apagar
    
Activar una salida digital (Ejemplo Q0.0)

    python3 replay.py 192.168.1.100 modificar Q0.0 on

Desactivar una salida digital (Ejemplo Q0.0)

    python3 replay.py 192.168.1.100 modificar Q0.0 off

## Contribuciones

Si deseas mejorar este proyecto, siéntete libre de hacer un fork y enviar un pull request con tus mejoras.

## Nota

Este proyecto tiene fines educativos y de auditoría en entornos controlados. No debe utilizarse con fines malintencionados ni en sistemas en producción sin autorización.

## Licencia

Este proyecto está bajo la licencia MIT.

    
