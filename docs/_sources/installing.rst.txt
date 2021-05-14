*************************************
Configuration of Project Environment
*************************************

Setup procedure
================
1. Download Pycharm IDE
      - Install `Pycharm <https://www.jetbrains.com/pycharm/download/>`_

      .. note::
        Any other Python IDE would have worked as well, but only the configuration for Pycharm is described in the followed step.

2. Configure project environment
      - Open the CanReader Directory (File -> Open)
      - Configure the Base Project Interpreter (File -> Settings -> Project Interpreter)
         * Based Project Interpreter: Python 3.8.0
      - Manually install packages to project interpreter (File -> Settings -> Project Interpreter -> plus button on the upper left side of the package table) and apply changes

         OR

      - Type the command below::

            pip install -r requirements.txt

3. Run CanReader.py

::

    python CanReader_main.py
