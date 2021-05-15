**********
Overview
**********


| The application named "CAN Reader" was created in Python 3.x using Qt framework.
| The PyQt5 module was used as an API between Qt and Python.

| A block representation of the system function is shown below.
| Arrows leading from one block to another indicate direct interaction of these blocks.
| While the arrows leading from the block to the edge of the area marked with a dashed line indicates call of the given subroutine.
|
| It is a multi-threaded program that contains 2 permanent threads "Main" and "GUI".
| The "Communication" and "Data processing" threads are created situationally on the basis of an action derived by the user and subsequently by receiving data from the formula.

.. image:: ../img/DiagramCanReaderOverview_EN.png
    :alt:   Functionality Overview

|
| Application is separated into 4 parts:

    #. Main program ensures communication between the individual subroutines, and is also responsible for :ref:`logging <Data logger code>` of incoming data.

    #. :ref:`GUI <GUI code>` subroutine is in charge of the user interface. That is, displaying the basic GUI, dealing with user requirements and update display based on provided data.

    #. :ref:`Communication <Communication code>` subroutine ensures communication with the formula based on the user-specified criteria.

    #. :ref:`Data processing <Data processing code>` provides filtering, processing and sorting of incoming data.

GUI Overview
================

.. image:: ../img/Overview_anotation.png
    :alt:   CAN Reader Overview

|
| The application consists following 11 parts:

1. :ref:`Dashboard <Dashboard>`.

2. :ref:`Graph tab <Graph tab>`.

3. :ref:`Error tab <Error tab>`.

4. :ref:`CAN messages settings <CAN Settings>`.

5. Choice of communication type.

6. :ref:`Communication settings <Communication>`.

7. Establishing / interrupting communication.

8. Display the current connection status.

9. Display of the last received CAN message.

10. Possibilities of working with files.

11. Display of documentation or "about application" window.