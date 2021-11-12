#!/usr/bin/python3
# -*- coding: utf-8 -*
#B. Vandeportaele 2021
# à lancer avec la commande python3 wokwi2gtkwave.py   dans le dossier de téléchargement des fichiers .vcd

import os
import sys
import math


 
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
    defaultfilecontent = """
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
pathToObserve='./'
# https://stackoverflow.com/questions/4548684/how-to-get-the-seconds-since-epoch-from-the-time-date-output-of-gmtime
#timeLastPKill= time.localtime()
#print("timeLastPKill: "+ str(timeLastPKill) )
#global timeLastPKill
#timeLastPKill = int(time.time())
#print("timeLastPKill: "+ str(timeLastPKill) )

global rcFile
global directoryforgtkwave
directoryforgtkwave="vcdforgtkwave"
rcFile="gtkwaverc"
################################################################################  
class MonHandler(FileSystemEventHandler):
    timeLastPKill=0
    def __init__(self):
        self.timeLastPKill = int(time.time())
        #print("timeLastPKill: "+ str(self.timeLastPKill) )        
    # cette méthode sera appelée à chaque fois qu'un fichier est modifié
    def on_modified(self, event):
        global rcFile
        global directoryforgtkwave
        nouvelleSimu=False        #pour réinitialiser le fichier bash         
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
               filename_in=event.src_path.replace("./","") 
               commandline="mkdir -p " + directoryforgtkwave
               print("execution de: "+commandline)
               os.system(commandline)
               createRcFile(directoryforgtkwave+"/"+rcFile)
               commandline="mv \""+ filename_in +"\" " + directoryforgtkwave +"/"           
               print("execution de: "+commandline)
               os.system(commandline)
               #filename_in=directoryforgtkwave+"/"+filename_in
               #filename_out=event.src_path.replace(".vcd","-out.vcd")
               filename_out=filename_in.replace(".vcd",".VCD") #extension VCD pour éviter que la création d'un vcd dans le meme dossier rapelle on_modified....
               traiteVCD(directoryforgtkwave+"/"+filename_in,directoryforgtkwave+"/"+filename_out)
               filename_gtkw=filename_in.replace(".vcd",".gtkw")
               createGtkwFile(directoryforgtkwave+"/"+filename_gtkw)              

               commandline="rm \"" +directoryforgtkwave+"/"+filename_in+"\""
               print("execution de: "+commandline)
               os.system(commandline)
               
               commandline="gtkwave --slider-zoom   "+"\"" +directoryforgtkwave+"/"+filename_out+"\"" +" "+"\"" +directoryforgtkwave+"/"+filename_gtkw+"\" \""+directoryforgtkwave+"/"+rcFile+"\" & " #sleep 1 "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger               
               #commandline="pkill gtkwave & gtkwave "+"\"" +filename_out+"\"" +" "+"\"" +filename_gtkw+"\"" + " & "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger             
               print("execution de: "+commandline)
               os.system(commandline)

               shellscriptname="showtraces.sh"
               fileExists=os.path.isfile(directoryforgtkwave+"/"+shellscriptname)
               if nouvelleSimu==True:
                   fout = open(directoryforgtkwave+"/"+shellscriptname, "w") #write                                   
                   #if not fileExists:
                   fout.write("#!/bin/bash\n")
               else:
                   fout = open(directoryforgtkwave+"/"+shellscriptname, "a") #append               
               commandline="gtkwave --slider-zoom   "+"\"" +filename_out+"\"" +" "+"\"" +filename_gtkw+"\" \""+rcFile+"\" & \n" #sleep 1 "  #attention les noms de fichiers peuvent contenir des espaces, donc il faut les protéger
               
               fout.write(commandline)                          
               fout.close()                
               commandline="chmod a+x "+directoryforgtkwave+"/"+shellscriptname
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

