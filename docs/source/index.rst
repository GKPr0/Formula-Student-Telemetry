.. CanReader documentation master file, created by
   sphinx-quickstart on Thu Jan  2 21:10:59 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Configuration of Project Environment
*************************************

Documentation for the CanReader app.
This app receives data from the remote device, process these data and visualize them.
The app was created for Formula student team Fs Tul Racing.

Overview on How to Run this APP
================================
1. Install a Python IDE
2. Install packages required
3. Run app

Setup procedure
================
1. Download Pycharm IDE
      - Install Pycharm (www.jetbrains.com/pycharm/download/)

      .. note:: Any other Python IDE would have worked as well, but the only configuration for Pycharm is described in the followed step.

2. Configure project environment
      - Open the CanReader Directory (File -> Open)
      - Configure the Base Project Interpreter (File -> Settings -> Project Interpreter)
         * Based Project Interpreter: Python 3.7.0
      - Manually install packages to project interpreter (File -> Settings -> Project Interpreter -> plus button on the upper left side of the package table) and apply changes

         OR

      - Type the command below on the activated virtual environment.::

            pip install -r requirements.txt

2. Run CanReader.py::

    python CanReader.py

Endpoints of the Teacher API
============================
1. View the current state of the vehicle
2. View the continuous state of the vehicle
3. Configurable CAN bus messages
4. Connectivity status monitoring
5. Adjustable saving of files

Documentation for the Code
**************************
.. toctree::
   :maxdepth: 2
   :caption: Contents:


Communication
==============


Socket Server
--------------
.. automodule:: Communication.SocketServer
   :members:


Config
=======

Config
--------------
.. automodule:: Config.Config
   :members:

DataConfig
--------------
.. automodule:: Config.DataConfig
   :members:

DataProcessing
===============

RawData
---------
.. automodule:: DataProcessing.RawData
   :members:

DataDecoder
------------
.. automodule:: DataProcessing.DataDecoder
   :members:

DataPoint
----------
.. automodule:: DataProcessing.DataPoint
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
