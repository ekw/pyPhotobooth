pyPhotobooth
=============

I wrote this photobooth software (and built the photobooth itself) for my sister's wedding banquet over the course of a month back in 2012.  During the wedding banquet, the software ran under WinXP and printed to a Canon PIXMA MG5320, but I have since ran it successfully on WinVista and Win7.  The software should also run under Linux, but printing currently only works with Windows. Printing should work for Linux as well if the code in photobooth.print.winPrint module is ported.  The only printer I have used with pyPhotobooth is the Canon PIXMA MG5320.

Prerequisites
-------------
(These are the versions I developed with, under Windows.  Earlier/later versions may also work):
* Python 2.7.3
* OpenCV-2.3.1-win-superpack.exe
* cmake-2.8.7-win32-x86.exe
* pygame-1.9.1.win32-py2.7.msi
* PIL-1.1.7.win32-py2.7.exe
* scipy-0.10.1-win32-superpack-python2.7.exe
* numpy-1.6.1-win32-superpack-python2.7.exe
* pywin32-217.win32-py2.7.exe
* CherryPy-3.2.2.win32.exe

Simplified instructions for compiling/installing OpenCV for Windows
-------------------------------------------------------------------
Complete instructions here: http://opencv.willowgarage.com/wiki/InstallGuide

1. Extract OpenCV-2.3.1-win-superpack.exe to C:\OpenCV
2. Ensure cmake-2.8.7-win32-x86.exe is installed
3. From DOS prompt:
    a. cd C:\OpenCV  # the directory containing INSTALL, CMakeLists.txt etc.
    b. mkdir release
    c. cd release
    d. cmake -D:CMAKE_BUILD_TYPE=RELEASE -D:BUILD_PYTHON_SUPPORT=ON C:\OpenCV
4. Open/build C:\opencv\release\OpenCV.sln with Microsoft Visual Studio (I used VS2010 Professional.  OpenCV docs say Express Editions of VS2008 and VS2010 also work).
5. After successful build, copy cv.py and cv2.pyd in C:\opencv\build\python\2.7\ to C:\Python27\Lib\site-packages

Running pyPhotobooth
--------------------
At command prompt, go to directory where photobooth.bat is located.
Run photobooth.bat with the location of a settings.ini file.

Example: photobooth.bat event1conf\settings.ini
