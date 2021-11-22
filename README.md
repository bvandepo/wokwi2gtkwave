# wokwi2gtkwave
A Python script that automates the visualization of vcd files generated with Wokwi 

##Description##
This project aims to facilitate the simulation of Arduino programs using the excellent Wokwi tools ( https://wokwi.com/ ). Wokwi embeds a 8 channel logic analyzer that can capture signals and  allows the users to download a Value Change Dump file for visualization and analysis using the tool gtkwave. Wokwi2gtkwave automatizes the many tasks required to show the VCD file each time it is downloaded by keeping track of file changes in the download directory:


It automatically call gtkwave to display the downloaded files.

It repairs the VCD files created by Wokwi for French Locale systems, as they contain erroneous date information that normally forbids gtkwave to open them.

It generates a gtkwave configuration file that sets the autozoom feature ON so the display allows an overview of the signals to allow the user to zoom in the region of interrest.

It generates a gtkwave file that sets the different signal name and organization to avoid the annoying task of grabbing signal to the signal windows in order to view them.

It manages the use of multiple logic analyzer components for which one VCD file is created for each logic analyzer (the name of the file being set using the attributes of the logic analyzer in the diagram.json file).

It creates a directory containing the multiple VCD files of a simulation and manages the creation of a script (shell for Linux and bat file for Windows) in the created directory to allows the automatic opening of the different VCD files afterward.

It automatically closes the old instances of gtkwave (supported only on Linux).


##Requirements##
Wokwi2gtkwave requires this 2 software to be installed:
  - gtkwave
  - python3 (and watchdog pip module, who is installed automatically if not installed previously)
 

#Installation and usage for Windows systems#

##Installation for Windows systems##

Download and install Python 3.8.6: https://bvdp.inetdoc.net/files/cesi/gtkwave/python-3.8.6-amd64.exe

Create a C:\Users\“yourlogin”\wokwi directory and download  and unzip the following file in this directory: 
https://bvdp.inetdoc.net/files/cesi/gtkwave/gtkwave-3.3.100-bin-win32.zip

Copy the wokwi2gtkwave.py file in the  C:\Users\“yourlogin”\wokwi 

##Usage for Windows systems##
Open a cmd windows and type:
```
  cd C:\Users\%username%\wokwi
  python wokwi2gtkwave.py
```

wokwi2gtkwave will then observe the vcd files downloaded in C:\Users\“yourlogin”\Downloads and process them automatically to C:\Users\“yourlogin”\wokwi\vcdforgtkwave , If the user wants to keep the files for a simulation, he just has to move or copy this folder. The default directories can be change by editing wokwi2gtkwave.py:

```
elif platform == "win32":
    if debug: print("Windows supported")
    userName=os.getenv('username') #"travailleur"
    directoryToScan= 'C:\\Users\\'+userName+'\\Downloads'
    directoryToStore="C:\\Users\\"+userName+"\\wokwi\\vcdforgtkwave"
    pathForGtkwaveBin="C:\\Users\\"+userName+"\\wokwi\\gtkwave-3.3.100-bin-win32\\gtkwave\\bin"
```    

#Installation and usage for Linux systems#

##Installation for Linux systems##
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
  cp  wokwi2gtkwave.py  ~/wokwi
```

##Usage for Linux systems##
Open a terminal and type:
```
  cd ~wokwi
  wokwi2gtkwave.py
```

wokwi2gtkwave will then observe the vcd files downloaded in ~/Téléchargements or ~/Downloads and process them automatically to ~/wokwi/vcdforgtkwave , If the user wants to keep the files for a simulation, he just has to move or copy this folder. The default directories can be change by editing wokwi2gtkwave.py, for instance by setting:
```
if platform == "linux" or platform == "linux2":
  directoryToScan= '/home/bvandepo/Téléchargements/'
  directoryToStore=’/home/bvandepo/whereIWant’
```


#Installation and usage for MAC systems#

I've not yet tested, if you want me to add the support for this system, ask me.