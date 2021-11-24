# wokwi2gtkwave
A Python script that automates the visualization of vcd files generated with Wokwi 

## Description
This project aims to facilitate the simulation of Arduino programs using the excellent Wokwi tools ( https://wokwi.com/ ). Wokwi embeds a 8 channel logic analyzer that can capture signals and  allows the users to download a Value Change Dump file for visualization and analysis using the tool gtkwave. Wokwi2gtkwave automatizes the many tasks required to show the VCD file each time it is downloaded by keeping track of file changes in the download directory:


It automatically call gtkwave to display the downloaded files.

It generates a gtkwave configuration file that sets the autozoom feature ON so the display allows an overview of the signals to allow the user to zoom in the region of interrest.

It generates a gtkwave file that sets the different signal names and organization to avoid the annoying task of grabbing signals to the signal windows in order to view them.

It manages the use of multiple logic analyzer components for which one VCD file is created for each logic analyzer (the name of the file being set using the attributes of the logic analyzer in the diagram.json file).

It creates a directory containing the multiple VCD files of a simulation and manages the creation of a script (shell for Linux and bat file for Windows) in the created directory to allows the automatic opening of the different VCD files afterward.

It automatically closes the old instances of gtkwave (supported only on Linux).

At its origin, wokwi2gtkwave was made to repair the VCD files created by Wokwi for French Locale systems, as they contained erroneous date information that normally forbidden gtkwave to open them. Uri Shaked updated Wokwi so this is not required anymore.

## Requirements
Wokwi2gtkwave requires this 2 software to be installed:
  - gtkwave
  - python3 >=3.6.3 has been tested 
  
Wokwi2gtkwave will install automatically Python modules that it requires if they are not installed previously:
  - watchdog to detect file downloads
  - glob2 (for Windows only) to fetch the gtkwave executable
 

# Installation and usage for Windows systems

## Installation for Windows systems

Download and install Python 3.8.6: https://bvdp.inetdoc.net/files/cesi/gtkwave/python-3.8.6-amd64.exe

Create a C:\Users\“yourlogin”\wokwi directory and download  and unzip the following file in this directory: 
https://bvdp.inetdoc.net/files/cesi/gtkwave/gtkwave-3.3.100-bin-win32.zip

Copy the wokwi2gtkwave.py file in the  C:\Users\“yourlogin”\wokwi 

## Usage for Windows systems
Open a cmd windows and type:
```
  cd C:\Users\%username%\wokwi
  python wokwi2gtkwave.py
```

If the python executable is not in your PATH environement variable, the directory_where_python_is_installed can be determined by recursively searching for the python.exe file in C:\
```
  cd C:\
  dir python3.exe /s/p
```

you should add the path before invoking python:
```
  cd C:\Users\%username%\wokwi
  C:\directory_where_python_is_installed\python wokwi2gtkwave.py
```

You may create a .bat file with these commands to be able to start wokwi2gtkwave easily.

Once started, wokwi2gtkwave will observe the vcd files downloaded in C:\Users\“yourlogin”\Téléchargements or C:\Users\“yourlogin”\Downloads and process them automatically to C:\Users\“yourlogin”\wokwi\vcdforgtkwave , If the user wants to keep the files for a simulation, he just has to move or copy this folder. The default directories can be changed by editing wokwi2gtkwave.py:

```
elif platform == "win32":
    if debug: print("Windows supported")
    userName=os.getenv('username') #"travailleur"
    directoryToScan= 'C:\\Users\\'+userName+'\\Downloads'
    directoryToStore="C:\\Users\\"+userName+"\\wokwi\\vcdforgtkwave"
    pathForGtkwaveBin="C:\\Users\\"+userName+"\\wokwi\\gtkwave-3.3.100-bin-win32\\gtkwave\\bin"
```    

# Installation and usage for Linux systems

## Installation for Linux systems
Install dependencies:
```
   sudo apt install python3 gtkwave
```


Check that gtkwave is in your PATH, the following command should return the location of gtkwave:
```
  whereis gtkwave 
```


Create a folder to receive the program and generated files:
```
  mkdir ~/wokwi
  cp wokwi2gtkwave.py  ~/wokwi
  chmod a+x ~/wokwi/wokwi2gtkwave.py
```

## Usage for Linux systems
Open a terminal and type:
```
  cd ~/wokwi
  wokwi2gtkwave.py
```

wokwi2gtkwave will then observe the vcd files downloaded in ~/Téléchargements or ~/Downloads and process them automatically to ~/wokwi/vcdforgtkwave , If the user wants to keep the files for a simulation, he just has to move or copy this folder. The default directories can be change by editing wokwi2gtkwave.py, for instance by setting:
```
if platform == "linux" or platform == "linux2":
  directoryToScan= '/home/bvandepo/Téléchargements/'
  directoryToStore=’/home/bvandepo/whereIWant’
```


# Installation and usage for MAC systems

I've not yet tested, if you want me to add the support for this system, ask me by adding a message in the Issue section on Github.

# Configuration of the browser to download automatically the VCD files in the download folder

## Chromium
You just have to set the download folder  in Parameters->advanced parameters->location  and to desactivate the option "always ask where to save the file"

## Firefox
Firefox is a bit more careful and won't let you donwload the VCD file automatically because there is not MIME type information attached to the VCD file that tells Firefox that the download is secure. So we need to modify the settings:
  - type the following URL in Firefox: about:config
  - click on "Accept..."
  - copy/paste the following preference name: browser.helperApps.neverAsk.saveToDisk
  - click on the blue pen (Modify), then copy/paste in the text area: application/octet-stream
  - click on the blue V to validate and then close the onglet

## Midori
Wokwi does not work with this browser...
