#!/usr/bin/python3
# -*- coding: utf-8 -*
#B. Vandeportaele 2021
# à lancer avec la commande python3 wokwi2gtkwave.py   dans le dossier de téléchargement des fichiers .vcd

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

#----------------------------------------------------
def traiteVCD(filename_in,filename_out):
    fin = open(filename_in, "r")
    fout = open(filename_out, "w")
    for line in fin.readlines():
      lineout = line.replace("(heure d’été d’Europe centrale)", "")
      lineout = lineout.replace("(heure normale d’Europe centrale)", "") #avec le changement d'heure....
      fout.write(lineout)          
    fin.close()
    fout.close()
#----------------------------------------------------
#filename_in="wokwi-logic2.vcd"
#filename_out="wokwi-logic2-out.vcd"
#traiteVCD(filename_in,filename_out)


#autozoom viré car plante de temps en temps à l'iut
'''
    defaultfilecontent = """do_initial_zoom_fit 1
"""
'''

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
global pathToObserve
global basename_filename_rc
global directoryforgtkwave


if platform == "linux" or platform == "linux2":
    print("linux")
elif platform == "darwin":
    print("OS X")
elif platform == "win32":
    print("Windows")    

    
pathToObserve='/home/bvandepo/Téléchargements/'
# https://stackoverflow.com/questions/4548684/how-to-get-the-seconds-since-epoch-from-the-time-date-output-of-gmtime
#timeLastPKill= time.localtime()
#print("timeLastPKill: "+ str(timeLastPKill) )
#global timeLastPKill
#timeLastPKill = int(time.time())
#print("timeLastPKill: "+ str(timeLastPKill) )

#directoryforgtkwave="vcdforgtkwave"
directoryforgtkwave="/home/bvandepo/Bureau/pythonb/wokwi2gtkwave/vcdforgtkwave"
basename_filename_rc="gtkwaverc"

################################################################################  
class MonHandler(FileSystemEventHandler):
    timeLastPKill=0
    def __init__(self):
        self.timeLastPKill = int(time.time())
        #print("timeLastPKill: "+ str(self.timeLastPKill) )        
    # cette méthode sera appelée à chaque fois qu'un fichier est modifié
    def on_modified(self, event):
        global pathToObserve
        global basename_filename_rc
        global directoryforgtkwave
        nouvelleSimu=False        #pour réinitialiser le fichier bash

        #pour gérer / ou \ automatiquement:
        ##(os.path.join(src, filename), os.path.join(dst, filename))

        
        if os.path.isfile(event.src_path):
            if event.src_path.endswith(('.vcd')):
               print("Un fichier vcd vient d'être téléchargé:" + str( event.src_path))
                #determine si il faut tuer gtkwave
               currentTime = int(time.time())
               if currentTime-self.timeLastPKill>10: #tue les instances anciennes de gtkwave mais pas les récentes qui peuvent etre due à des analyseurs logiques en parallèle
                   self.timeLastPKill=currentTime
                   commandline="pkill gtkwave &"       
                   print("execution de: "+commandline)
                   os.system(commandline)
                   nouvelleSimu=True               
               time.sleep(1)
               #else:
               #    time.sleep(2)
               filename_in=event.src_path.replace("./","")  #nom du fichier avec chemin complet
               basename_filename_in=os.path.basename(filename_in)
               
               print("filename_in: "+filename_in)
               #commandline="mkdir -p " + directoryforgtkwave;  print("execution de: "+commandline); os.system(commandline)
               try:
                   os.mkdir(directoryforgtkwave)
               except OSError:
                   print ("Creation of the directory %s failed" % directoryforgtkwave)
               else:
                   print ("Successfully created the directory %s " % directoryforgtkwave)

               filename_rc=os.path.join(directoryforgtkwave, basename_filename_rc)
               createRcFile(filename_rc)
               #commandline="mv \""+ filename_in +"\" " + directoryforgtkwave +"/";  print("execution de: "+commandline); os.system(commandline)
               #déplace le fichier en écrasant la cible si elle existe déjà (il faut indiquer dossier+nom en destination)
               shutil.move(filename_in, os.path.join(directoryforgtkwave, basename_filename_in))
               
               
               #filename_in=directoryforgtkwave+"/"+filename_in
               #filename_out=event.src_path.replace(".vcd","-out.vcd")
               basename_filename_out=basename_filename_in.replace(".vcd",".VCD") #extension VCD pour éviter que la création d'un vcd dans le meme dossier rapelle on_modified....
               filename_out=os.path.join(directoryforgtkwave, basename_filename_out)
               print("basename_filename_out: "+basename_filename_out)
               print("filename_out: "+filename_out)
               traiteVCD(os.path.join(directoryforgtkwave, basename_filename_in),filename_out)
                              
               basename_filename_gtkw=basename_filename_in.replace(".vcd",".gtkw")
               filename_gtkw=os.path.join(directoryforgtkwave, basename_filename_gtkw)
               print("filename_gtkw:"+filename_gtkw)
               createGtkwFile(filename_gtkw)

               #commandline="rm \"" +directoryforgtkwave+"/"+filename_in+"\""; print("execution de: "+commandline);  os.system(commandline)
               try:
                   os.remove(os.path.join(directoryforgtkwave, basename_filename_in))
               except OSError:
                   print ("Deletion of the file %s failed" % os.path.join(directoryforgtkwave, basename_filename_in))
                   

               commandline="gtkwave --slider-zoom   "+"\"" +filename_out+"\" \"" +filename_gtkw+"\" \"" +filename_rc+"\" & " #sleep 1 "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger               
               #commandline="pkill gtkwave & gtkwave "+"\"" +filename_out+"\"" +" "+"\"" +filename_gtkw+"\"" + " & "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger             
               print("execution de: "+commandline)
               os.system(commandline)

               if platform == "linux" or platform == "linux2":
                   basename_filename_script="showtraces.sh"
                   filename_script=os.path.join(directoryforgtkwave,basename_filename_script)
                   fileExists=os.path.isfile(filename_script)
                   if nouvelleSimu==True:
                       fout = open(filename_script, "w") #write                                   
                       #if not fileExists:
                       fout.write("#!/bin/bash\n")
                   else:
                       fout = open(filename_script, "a") #append               
                   #commandline="gtkwave --slider-zoom   "+"\"" +filename_out+"\"" +" "+"\"" +filename_gtkw+"\" \""+rcFile+"\" & \n" #sleep 1 "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger
                   commandline="gtkwave --slider-zoom   "+"\"" +basename_filename_out+"\" \"" +basename_filename_gtkw+"\" \"" +filename_rc+"\" & "  #sleep 1 "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger                             
                   fout.write(commandline)                          
                   fout.close()                
                   commandline="chmod a+x "+filename_script
                   print("execution de: "+commandline)
                   os.system(commandline)

               
               #print("execution de: "+commandline +" terminée")               
               time.sleep(0.1) #il faut laisser un peu de temps entre les 2 appels de gtkwave sinon il ouvre 2 fois le meme fichier
################################################################################
def main():
  print("automatise gtkwave pour Wokwi.\n B. Vandeportaele IUT GEII 2021\nFonctionne avec plusieurs analyseurs logiques, avec 1 fichier VCD par analyseur")  
  #if len(sys.argv)==2:
  #  inf=sys.argv[1]
  #  ouf=sys.argv[2]
  observer = Observer()
  # Surveiller récursivement tous les événements du dossier pathToObserve
  # et appeler les méthodes de MonHandler quand quelque chose se produit
  observer.schedule(MonHandler(), path=pathToObserve, recursive=True)
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

