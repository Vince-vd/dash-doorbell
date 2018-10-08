from scapy.all import *
import wiringpi
import time
import datetime

#setup wiringpi for gpio control
wiringpi.wiringPiSetup()

# define pins per door, options are 
front = 3 # second relay
basement = 22 # third relay

wiringpi.pinMode(front, 1) #sets GPIO 3 to output (second relay, front door)
wiringpi.pinMode(basement, 1)

FRONT_DOOR_MAC = '00:fc:8b:32:d4:c7' # enter Dash Button's MAC Address here.
BASEMENT_DOOR_MAC = 'b4:7c:9c:92:3f:c9' # MAC address of back door dash doorbell


try:
    def ring_door(door):
        # set front door to high
        wiringpi.digitalWrite(door,1) 
        time.sleep(1) #wait 1 second
        # set front door to low again, bell should be ringing
        wiringpi.digitalWrite(door,0) 
           
    
    def detect_button(pkt):
        if pkt.haslayer(DHCP) and pkt[Ether].src == FRONT_DOOR_MAC:
            ring_door(front)
            return 'front door button was pressed at ' + str(datetime.datetime.now())
        if pkt.haslayer(DHCP) and pkt[Ether].src == BASEMENT_DOOR_MAC:
            ring_door(front)
            return 'back door button was pressed at ' + str(datetime.datetime.now())

    sniff(prn=detect_button, filter="(udp and (port 67 or 68))", store=0)


except KeyboardInterrupt:
    #cleanup GPIO settings before exiting, make sure relays are low
    wiringpi.digitalWrite(front,0) # set pin 3 to low on exit
    wiringpi.digitalWrite(basement, 0)
    print("Exiting...")
