#!/usr/bin/python3
# -*- coding: utf-8 -*
#B. Vandeportaele 2021
# à lancer avec la commande python3 wokwi2gtkwave.py   dans le dossier de téléchargement des fichiers .vcd

#TODO:
#générer à partir d'une variable chemin: C:\\Users\\travailleur\\Desktop\\gtkwave-3.3.100-bin-win32\\gtkwave\\bin\\gtkwave  pour exec+bat
#arg pour passer les emplacements si pas par défaut
#variables de chemin à régler au début du script

########################################
#https://stackoverflow.com/questions/1051254/check-if-python-package-is-installed
#install automatically watchdog if not already installed
import subprocess
import sys

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

if 'watchdog' in installed_packages:
  print('watchdog pip package already installed')
else: 
  print('watchdog pip package missing, lets install it')
  import pip
  pip.main(['install','watchdog'])
########################################

import os
import sys
import math


import shutil
from sys import platform
 
#inspiré de http://sametmax.com/reagir-a-un-changement-sur-un-fichier-avec-watchdog/
#sudo pip3 install watchdog
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
#doc dans : https://pythonhosted.org/watchdog/api.html#watchdog.observers.Observer
import time

debug=False

#----------------------------------------------------
def repairVcdFile(filename_in, filename_out):
    fin = open(filename_in, "r")
    fout = open(filename_out, "w")
    previous_time=0
    for line in fin.readlines():
      lineout = line.replace("(heure d’été d’Europe centrale)", "")
      lineout = lineout.replace("(heure normale d’Europe centrale)", "") #avec le changement d'heure....
      #ne marche pas sous windows... :( du coup je coupe à partir de (
      if lineout.startswith('$date'):
            pos=lineout.find('(')
            if pos!=-1: #found
                lineout=lineout[0:pos]+'$end\n'
      #number doit être croissant;
      if lineout.startswith('#'):
          current_time=int(lineout[1:])
          #print("current_time="+str(current_time))
          if current_time<previous_time:
              print("Error: Time backtracking detected in VCD file!")
          else:
              previous_time=current_time              
      fout.write(lineout)
      fout.write("\n") #pour s'assurer qu'il y a bien \n à la dernière ligne , c'est ça qui cause l'erreur  Time backtracking detected in VCD file!  qui fait planter gtkwave avec l'option #autozoom 
    fin.close()
    fout.close()
#----------------------------------------------------
#filename_in="wokwi-logic2.vcd"
#filename_out="wokwi-logic2-out.vcd"
#repairVcdFile(filename_in,filename_out)


################################################################################
#crée un fichier de réglage gtkwave par défaut pour l'application 
def createRcFile(filename_out):
    fout = open(filename_out, "w")    
    defaultfilecontent = """do_initial_zoom_fit 1
"""
    #print(defaultfilecontent)
    fout.write(defaultfilecontent)          
    fout.close()   
    
################################################################################
#crée un fichier de réglage gtkwave par défaut pour le fichier pour que les signaux à visualiser soit déjà selectionnés
def createGtkwFile(filename_out):
    fout = open(filename_out, "w")
    defaultfilecontent = """[timestart] 0
[size] 1000 600
[pos] -1 -1
*0.000000 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1
[sst_width] 225
[signals_width] 78
[sst_expanded] 1
[sst_vpaned_height] 152
@28
logic.D0
logic.D1
logic.D2
logic.D3
logic.D4
logic.D5
logic.D6
logic.D7
[pattern_trace] 1
[pattern_trace] 0"""
    #print(defaultfilecontent)
    fout.write(defaultfilecontent)          
    fout.close()

################################################################################
#createGtkwFile("test.gtkw")
################################################################################
#pathToObserve='./'
global directoryToScan
global directoryToStore


if platform == "linux" or platform == "linux2":
    if debug: print("linux supported")
    directoryToScan= '/home/bvandepo/Téléchargements/'
    directoryToStore= "/home/bvandepo/Bureau/pythonb/wokwi2gtkwave/vcdforgtkwave"
elif platform == "darwin":
    print("OS X not yet supported")
    exit()
elif platform == "win32":
    if debug: print("Windows supported")
    userName=os.getenv('username') #"travailleur"
    directoryToScan= 'C:\\Users\\'+userName+'\\Downloads'
    directoryToStore="C:\\Users\\"+userName+"\\wokwi\\vcdforgtkwave"
    pathForGtkwaveBin="C:\\Users\\"+userName+"\\wokwi\\gtkwave-3.3.100-bin-win32\\gtkwave\\bin"
    
    

# https://stackoverflow.com/questions/4548684/how-to-get-the-seconds-since-epoch-from-the-time-date-output-of-gmtime
#timeLastPKill= time.localtime()
#print("timeLastPKill: "+ str(timeLastPKill) )
#global timeLastPKill
#timeLastPKill = int(time.time())
#print("timeLastPKill: "+ str(timeLastPKill) )

#directoryforgtkwave="vcdforgtkwave"


################################################################################  
class MyEventHandler(FileSystemEventHandler):
    timeLastPKill=0
    def __init__(self):
        self.timeLastPKill = int(time.time())
    def on_modified(self, event):
        global directoryToScan
        global directoryToStore
        basename_rc = "gtkwaverc"
        isANewSimulation=False        #variable used to group a set of multiple simulation in the same script file

        #pour gérer / ou \ automatiquement:
        ##(os.path.join(src, filename), os.path.join(dst, filename))

        
        if os.path.isfile(event.src_path):
            if event.src_path.endswith(('.vcd')):
               print("A new vcd file has been downloaded:" + str( event.src_path))
                #determine si il faut tuer gtkwave
               currentTime = int(time.time())
               if currentTime-self.timeLastPKill>10: #tue les instances anciennes de gtkwave mais pas les récentes qui peuvent etre due à des analyseurs logiques en parallèle
                   self.timeLastPKill=currentTime
                   if platform == "linux" or platform == "linux2":
                       commandLine="pkill gtkwave &"
                       if debug: print("running: "+commandLine)
                       os.system(commandLine)
                   isANewSimulation=True
               time.sleep(1)
               filename_in=event.src_path.replace("./","")  #nom du fichier avec chemin complet
               basename_in=os.path.basename(filename_in)
               
               if debug: print("filename_in: "+filename_in)
               #commandLine="mkdir -p " + directoryforgtkwave;  print("execution de: "+commandLine); os.system(commandLine)
               try:
                   os.mkdir(directoryToStore)
               except OSError:
                   if debug: print ("Creation of the directory %s failed" % directoryToStore)
               else:
                   if debug: print ("Successfully created the directory %s " % directoryToStore)

               filename_rc=os.path.join(directoryToStore, basename_rc)
               createRcFile(filename_rc)
               #commandLine="mv \""+ filename_in +"\" " + directoryforgtkwave +"/";  print("execution de: "+commandLine); os.system(commandLine)
               #déplace le fichier en écrasant la cible si elle existe déjà (il faut indiquer dossier+nom en destination)
               #shutil.move(filename_in, os.path.join(directoryforgtkwave, basename_in))
               #filename_in=directoryforgtkwave+"/"+filename_in
               #filename_out=event.src_path.replace(".vcd","-out.vcd")
               #basename_out=basename_in.replace(".vcd",".VCD") #extension VCD pour éviter que la création d'un vcd dans le meme dossier rapelle on_modified....
               basename_out=basename_in
               filename_out=os.path.join(directoryToStore, basename_out)
               if debug: print("basename_out: "+basename_out)
               if debug: print("filename_out: "+filename_out)
               #repairVcdFile(os.path.join(directoryforgtkwave, basename_in),filename_out)
               repairVcdFile(filename_in, filename_out)
                              
               basename_gtkw=basename_in.replace(".vcd",".gtkw")
               filename_gtkw=os.path.join(directoryToStore, basename_gtkw)
               if debug: print("filename_gtkw:"+filename_gtkw)
               createGtkwFile(filename_gtkw)

               #mince sous windows, il n'y a pas de différentiation entre vcd et VCD...
               #commandLine="rm \"" +directoryforgtkwave+"/"+filename_in+"\""; print("execution de: "+commandLine);  os.system(commandLine)
               try:
                   #os.remove(os.path.join(directoryforgtkwave, basename_in))
                   os.remove(filename_in)
               except OSError:
                   print ("Deletion of the file %s failed" % os.remove(filename_in) ) #os.path.join(directoryforgtkwave, basename_in))
                   
               if platform == "linux" or platform == "linux2":
                   commandLine="gtkwave --slider-zoom   "+"\"" +filename_out+"\" \"" +filename_gtkw+"\" \"" +filename_rc+"\" & " #sleep 1 "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger
               elif platform == "win32":
                   #commandLine="START \"\" C:\\Users\\travailleur\\Desktop\\gtkwave-3.3.100-bin-win32\\gtkwave\\bin\\gtkwave --slider-zoom   "+"\"" +filename_out+"\" \"" +filename_gtkw+"\" \"" +filename_rc+"\"  " #sleep 1 "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger
                   commandLine="START \"\"  "+ pathForGtkwaveBin + "\\gtkwave --slider-zoom   "+"\"" +filename_out+"\" \"" +filename_gtkw+"\" \"" +filename_rc+"\"  " #sleep 1 "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger
                   
               #commandLine="pkill gtkwave & gtkwave "+"\"" +filename_out+"\"" +" "+"\"" +filename_gtkw+"\"" + " & "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger
               if debug: print("running: "+commandLine)
               os.system(commandLine)

               if platform == "linux" or platform == "linux2":
                   basename_script="showtraces.sh"
                   filename_script=os.path.join(directoryToStore, basename_script)
                   fileExists=os.path.isfile(filename_script)
                   if isANewSimulation==True:
                       fout = open(filename_script, "w") #write                                   
                       #if not fileExists:
                       fout.write("#!/bin/bash\n")
                   else:
                       fout = open(filename_script, "a") #append               
                   #commandLine="gtkwave --slider-zoom   "+"\"" +filename_out+"\"" +" "+"\"" +filename_gtkw+"\" \""+rcFile+"\" & \n" #sleep 1 "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger
                   commandLine="gtkwave --slider-zoom   "+"\"" +basename_out+"\" \"" +basename_gtkw+"\" \"" +filename_rc+"\" & "  #sleep 1 "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger
                   fout.write(commandLine)
                   fout.close()                
                   commandLine="chmod a+x "+filename_script
                   if debug: print("running: "+commandLine)
                   os.system(commandLine)
               elif platform == "win32":                
                   basename_script="showtraces.bat"
                   filename_script=os.path.join(directoryToStore, basename_script)
                   fileExists=os.path.isfile(filename_script)
                   if isANewSimulation==True:
                       fout = open(filename_script, "w") #write                                   
                   else:
                       fout = open(filename_script, "a") #append               
                   #commandLine="START \"\" gtkwave --slider-zoom   "+"\"" +basename_out+"\" \"" +basename_gtkw+"\" \"" +filename_rc+"\"  \n"  #sleep 1 "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger
                   commandLine="START \"\" "+ pathForGtkwaveBin + "\\gtkwave --slider-zoom   "+"\"" +basename_out+"\" \"" +basename_gtkw+"\" \"" +filename_rc+"\"  \n"  #sleep 1 "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger
                   fout.write(commandLine)
                   fout.close()                                  

               
               #print("execution de: "+commandLine +" terminée")
               time.sleep(0.1) #il faut laisser un peu de temps entre les 2 appels de gtkwave sinon il ouvre 2 fois le meme fichier
################################################################################
def main():
  print("Wokwi2gtkwave\n B. Vandeportaele IUT GEII 2021\nCan be used with multiple Logic Analizer, with one file for each analyzer")
  #if len(sys.argv)==2:
  #  inf=sys.argv[1]
  #  ouf=sys.argv[2]
  observer = Observer()
  # Surveiller récursivement tous les événements du dossier pathToObserve
  # et appeler les méthodes de MonHandler quand quelque chose se produit
  observer.schedule(MyEventHandler(), path=directoryToScan, recursive=True)
  observer.start()
  # L'observer travaille dans un thread séparé donc on fait une
  # boucle infinie pour maintenir le thread principal
  # actif dans cette démo 
  try:
    while True:
        time.sleep(1)
  except KeyboardInterrupt:
    # Ctrl + C arrête tout
    observer.stop()
  # on attend que tous les threads se terminent proprement
  observer.join()
  return
################################################################################
main()
