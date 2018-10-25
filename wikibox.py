#!/usr/bin/python3
# encoding: utf-8
#
# ----------- LICENSING ----------------
#
# Copyright 2018 - Esteful
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including without limitation the rights to use,
#  copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#  and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# ----------- Project Details ----------
#
# This program is the software part of the WikiBox project.
# The hardware consists of a Raspberry Pi, a ZJ-58 thermal printer, a LED and a Button and a Switch.
#
# Installation guide for the ZJ-58 printer in Raspbian:
# http://scruss.com/blog/2015/07/12/thermal-printer-driver-for-cups-linux-and-raspberry-pi-zj-58/
# After installing it the default font width should be adjusted to the desired font size, and according to that
#
# A LED is connected to the pin 13, and shows the current state of the program (don't forget to add a resistor)
# A Button is connected to the pin 5: 1 short pulsation prints a Wikipedia page, 
#                                     2 short pulsations prints the number of articles in the current Wikipedia category
#                                     1 long pulsation prints the list of the current Wikipedia category
# A switch is connected to the pin 21 for enabling RPi shutdown

import os
import wikipediaapi
import urllib.request, json
import time
from RPi import GPIO
from random import randint #artikuluak aleatorioki zerrendatzeko
import sys
import socket

# Program Settings :)
kategoria = "Inventoras" #hemen aldatu nahi den kategoria
kategoria_wiki = "Categoría:"+kategoria #kategoria dagokion hizkuntzara aldatu
wiki_lang = "es" #hizkuntza hautatu

# Program Constants
REMOTE_SERVER = "www.wikipedia.org"
Button_Pin    = 5
Switch_Pin    = 21
LED_Pin       = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(Button_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Switch_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_Pin, GPIO.OUT)

# Print intro
#os.system('echo "Sistema abiarazten\nGo Totoro, Go!!!\n-\n" | fold -s -w 27 | lp')
os.system('lp -o position=top /home/pi/totoro.jpg')
os.system('echo "Kaixo!!! botoi urdina behin sakatuta wikipediako artikulu bat aterako dizut, \
	       Argi gorria piztuta fijo badago lanean ari naizen seinale, ez nazazu molestatu!!! \
	       Prest nagoenean keinuka arituko da" | fold -s -w 27 | lp')

off_switch = 0

while True:
    time.sleep(0.1) #CPU denbora guztia ez kontsumitzeko
    try:
        start_time1 = time.time()
        loop_counter = 0
        while (GPIO.input(Button_Pin) == 1):
            if ((time.time() - start_time1) > 0.1):
                start_time1 = time.time()
                loop_counter = loop_counter + 1
                if (loop_counter == 5):
                    loop_counter = 0
            if (loop_counter == 4):
                GPIO.output(LED_Pin, True)
            else:
                GPIO.output(LED_Pin, False)
            time.sleep(0.02) #CPU guztia ez kontsumitzeko

            if (GPIO.input(Switch_Pin) == 1):
                off_switch = 1

        if (GPIO.input(Switch_Pin) == 0 and off_switch == 1):
            print ("Powering Off")
            os.system('poweroff')

        button_status = 0

        if (GPIO.input(Button_Pin) == 0):
            GPIO.output(LED_Pin, True)

            button_status=1 # Button 1 pulsation

            time.sleep(0.1) #Debounce button

            #detect second pulsation
            start_time = time.time()

            button_released = 0
            while ((time.time() - start_time) < 1.5):
                if (GPIO.input(Button_Pin) == 1):        #Botoia askatu da
                    time.sleep(0.1) #Debounce button
                    button_released = 1
                if (button_released == 1 and GPIO.input(Button_Pin) == 0): # Bigarren botoi pulsazioa
                    button_status = 2

            if (button_released == 0 and button_status == 1): # Botoia iniz ez da askatu
                    button_status =3

        if (button_status == 1):
            # Wikipedia inizializatu
            wiki_wiki = wikipediaapi.Wikipedia(language=wiki_lang,
                                               extract_format=wikipediaapi.ExtractFormat.WIKI)

            #kategoria orria deskargatu
            #kategoria_orria = wiki_wiki.page("Kategoria:"+kategoria)
            kategoria_orria = wiki_wiki.page(kategoria_wiki)

            #kategoria orriko artikuluak zerrenda bihurtu
            emakume_zerrenda = list(kategoria_orria.categorymembers.keys())

            #Zerrendako lehen artikulua aukeratu, beti desberdin ordenatzen da zerrenda,
            # beraz beti desberdina izango da
            random_n= randint(0,len(emakume_zerrenda)-1)

            hautatutako_artikulua = wiki_wiki.page(emakume_zerrenda[random_n])

            # Paragrafo amaierako salto bakotza bitan bihurtu, paragrafoak banatzeko, eta hobeto irakur $
            # hautatutako_artikulua_polita = hautatutako_artikulua.summary.replace('\n', '\n\n')

            # Artikuluaren lehen parrafoa hartu
            if (len(hautatutako_artikulua.summary.split('\n')) > 1):
                hautatutako_artikulua_polita = hautatutako_artikulua.summary.split('\n')[0]
            else:
                hautatutako_artikulua_polita = hautatutako_artikulua.summary
            os.system('echo "'+kategoria + ": " + emakume_zerrenda[random_n]+'\n\n'+hautatutako_artikulu$

            GPIO.output(LED_Pin, False) #LEDa itzali
            time.sleep(5) #Hurrengo ziklora itxoin imprimagailua ez ataskatzeko

        if (button_status == 2):
            # Wikipedia inizializatu
            wiki_wiki = wikipediaapi.Wikipedia(language=wiki_lang,
                                               extract_format=wikipediaapi.ExtractFormat.WIKI)

            #kategoria orria deskargatu
            kategoria_orria = wiki_wiki.page(kategoria_wiki)

            #kategoria orriko artikuluak zerrenda bihurtu
            emakume_zerrenda = list(kategoria_orria.categorymembers.keys())

            izenburua = kategoria + str(len(emakume_zerrenda)) + '\n-\n'

            os.system('echo "'+izenburua + '\n-\n-\n-\n-\n" | fold -s -w 27 | lp')

            GPIO.output(LED_Pin, False) #LEDa itzali
            time.sleep(5) #Hurrengo ziklora itxoin imprimagailua ez ataskatzeko
     
        if (button_status == 3):
            # Wikipedia inizializatu
            wiki_wiki = wikipediaapi.Wikipedia(language=wiki_lang,
                                               extract_format=wikipediaapi.ExtractFormat.WIKI)

            #kategoria orria deskargatu
            kategoria_orria = wiki_wiki.page(kategoria_wiki)

            #kategoria orriko artikuluak zerrenda bihurtu
            emakume_zerrenda = list(kategoria_orria.categorymembers.keys())

            izenburua = kategoria+": " + str(len(emakume_zerrenda)) + '\n-\n'

            emakumeak = '\n'.join(emakume_zerrenda)

            os.system('echo "'+'\n'+izenburua + emakumeak + '\n-\n-\n-\n-\n" | fold -s -w 27 | lp')

            GPIO.output(LED_Pin, False) #LEDa itzali
            time.sleep(8) #Hurrengo ziklora itxoin imprimagailua ez ataskatzeko

    except KeyboardInterrupt:
        GPIO.output(LED_Pin, False) #LEDa itzali
        print (" ")
        print ("Ctrl+C captured..... Exiting")
        sys.exit(0)

    except:
        pass
