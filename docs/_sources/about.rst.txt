*************************************
About
*************************************

| CAN Reader is app developed specifically for for Formula student team `FS Tul Racing <https://www.fstulracing.cz/>`_.
| The application was developed as part of a `bachelor's thesis <https://dspace.tul.cz/>`_.

| Created system collects data from the CAN bus and sends them via Wi-Fi to the user for further processing and visualization.

| A graphical representation of the system is shown below.
| The user can choose from two methods of data transfer:

1. Formula -> User
    - In this variant, the formula communicates directly to the user's PC via Wifi.
    - The advantage of this is the higher transmission speed and simplicity of connection.
    - The disadvantage of this is the relatively limited range.
2. Formula -> ESP32 -> User
    - In this variant, the formula communicates with an intermediate member (ESP32-based device), which transmits the received data to the application via a serial line.
    - The advantage of this is a sharp increase in range (theoretically over 1 km).
    - The disadvantage of this method is the limited transmission speed (250 kb/s) and the need for additional equipment.

.. image:: img/Telemetrie.png
    :width: 500
    :alt:   Telemetry concept



Author
============
| Contact me on `Linkedin <https://www.linkedin.com/in/ond%C5%99ej-vacek-99a3a4204/>`_.
| Checkout my other project on `GitHub <https://github.com/GKPr0>`_.