#Brad Halloween Script
#ran in Python 2
#written for Raspberry Pi and Piface
#- Pi volumne settingd:  $ amixer sset PCM,0 XX%
#- Pi force analog audio: $ amixer cset numid=3 1
#Sequence:
#- trigger sensor on steps 
#- Flash light in house for warning (output 7)
#- start rocking chair and creaking sound turn on light
#- wait for them to get up steps
#- breaking lightbulb sound and turn light off
#- scream
#- lights to draw attention to vortex.
#- Evil Laugh
#- restart after XX second sleep so they do not set it off as they walk back down
from time import sleep
import pifacedigitalio

import os
import pygame

BUTTON_PRESS_TIME = 0.5


DEVICE_1_ON = 6 #controller 2

DEVICE_1_OFF = 3 #controller 2

DEVICE_2_ON = 7 #controller 3

DEVICE_2_OFF = 2 #controller 3

DEVICE_3_ON = 5 #controller 1

DEVICE_3_OFF = 4 #controller 1


def main():
    pifacedigitalio.init()    
    pfd = pifacedigitalio.PiFaceDigital()
    pfd.output_port.all_off()

    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()

    snd_creaking = pygame.mixer.Sound('/home/pi/halloween/sounds/slowrockcreak.wav')
    snd_light = pygame.mixer.Sound('/home/pi/halloween/sounds/breakinbulb1.wav')
    snd_scream = pygame.mixer.Sound('/home/pi/halloween/sounds/womanscream12.wav')
    snd_laugh = pygame.mixer.Sound('/home/pi/halloween/sounds/evillaughhall.wav')

    print "Start to SCARE!"
    
    while(1):
        if pfd.input_pins[0].value == 1:

            print "Sensor trip! BOO!"

            print "Warning LED inside"
            for x in range(0, 10):
                pfd.leds[0].turn_on()
                sleep(0.10)
                pfd.leds[0].turn_off()
                sleep(0.10)

            print "Rocking chair, sound, and light on"
            snd_creaking.play()#currently 22 seconds
            mains_switch(pfd, DEVICE_2_ON)#light
            sleep(0.2)
            mains_switch(pfd, DEVICE_1_ON)#chair
           
            sleep(5)
        
            print "Chair light off"
            snd_light.play()
            mains_switch(pfd, DEVICE_2_OFF)#light
            sleep(1.3)

            snd_scream.play()
            sleep(3)

            print "Flash LED Vortex light"
            for x in range(0, 20):
                pfd.leds[1].turn_on()
                sleep(0.10)
                pfd.leds[1].turn_off()
                sleep(0.10)

            sleep(8)
            
            print "SCARY laugh!"
            snd_laugh.play()# idea, tie to sound organ? hmmmm
            sleep(6.5)

            print "Chair stop"
            mains_switch(pfd, DEVICE_1_OFF)#chair
            sleep(10)
            print "Waiting on next victim!"
                
                
def mains_switch(pfd, port):

   pfd.output_pins[port].turn_on()

   sleep(BUTTON_PRESS_TIME)

   pfd.output_pins[port].turn_off()

   
if __name__ == "__main__":

    main()            
