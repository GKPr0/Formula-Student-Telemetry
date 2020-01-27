.. CanReader documentation master file, created by
   sphinx-quickstart on Thu Jan  2 21:10:59 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Configuration of Project Environment
*************************************

TErU is an application for visualization of tests result.
The documentation was created for Entry Engineering s.r.o .

Overview on How to Run this APP
================================
1. Install a Qt Creator IDE
2. Import TErU to Qt
3. Configure project environment
4. Build project
5. Run app

Setup procedure
================
1. Install a Qt Creator IDE
      - Download Qt Creator IDE from https://www.qt.io/download
      - Install Qt 5.12.2 MSCV2017 64 bit
      .. note:: Newer versions of QT would have worked as well.

3. Import TErU
      - Open QT Creator IDE
      - Import TEru project (File -> New File or Project -> Import Project -> Import Existing Project)
      - Select location of project and it´s name.
      - Select files matching: *.cpp, *.h, *.pro, *.pri, *.qbs, *.ui

      OR

      - #TODO add configuration for direct import from GIT repository

2. Configure project environment
      - Open Kits options ( Tools -> Options ->  Kits)
      - Create new Kit (Add button on right side)
      - Set C++ compiler
         * Used: Microsoft Visual C++ Compiler 16.2..
      - Set CMake tool
         * Used: CMake

5. Build TEruU
      - Build project ( Build -> Build project "ProjectName") OR Ctrl + B

4. Run TErU
      - Run project ( Green play button on lower left side) OR Ctrl + R




