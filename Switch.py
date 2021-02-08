# Spanning Tree project for GA Tech OMS-CS CS 6250 Computer Networks
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To 
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm - 
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015, updated for new VM by Jared Scott and James Lohse

from Message import *
from StpSwitch import *


class Switch(StpSwitch):

    def __init__(self, idNum, topolink, neighbors):
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)

        # TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.
        self.info = {'root': self.switchID,
                    'distance': 0,
                    'activelinks': dict.fromkeys(self.links, True),  # keep track of active links, default True
                    'switchThrough':self.switchID   # keep track of the neighbor to get to the root
        }

    def send_initial_messages(self):
        # TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
        #      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        for neighbor in self.links:
            # initially every switch thinks that it is the root
            # pathThrough is set as False because now origin does not need the destination to get to "root"
            # msg = Message(claimedRoot, distanceToRoot, originID, destinationID, pathThrough)
            message = Message(self.switchID,0,self.switchID,neighbor,False)
            # print('message is from '+ str(self.switchID)+ ' to neighbor '+ str(neighbor)+ ' saying the root is '+str(self.switchID))
            # print([message.root, message.destination])
            self.send_message(message)       
                
    def send_update_messages(self):
        # send neighbors updated information after updating itself
        for neighbor in self.links:
            # check if pass through the neighbor to get to the root
            pathThrough = False
            if neighbor == self.info['switchThrough']:
                pathThrough = True
            # msg = Message(claimedRoot, distanceToRoot, originID, destinationID, pathThrough)
            # print('message is from '+ str(self.switchID)+ ' to neighbor '+ str(neighbor)+ ' saying the root is '+str(self.info['root'])+' and distance is '+str(self.info['distance']))
            message = Message(self.info['root'],self.info['distance'],self.switchID,neighbor,pathThrough)
            self.send_message(message)

    def process_message(self, message):
        # TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message

        if message.root < self.info['root']: 
            # if they receive lower claimed root, the root should update
            self.info['root'] = message.root
            self.info['distance'] = 1+message.distance
            # print('root changed to', self.info['root'])
            # print('distance changed to', self.info['distance'])

            self.info['activelinks'][message.origin]= True
            self.info['switchThrough'] = message.origin

            # notify neighbors
            self.send_update_messages()

        elif message.root == self.info['root'] and 1+message.distance < self.info['distance']:
            # no need to update root, but need to update distance, activelinks, switchThrough
            self.info['distance'] = 1+message.distance
            self.info['activelinks'][message.origin]= True
            self.info['switchThrough'] = message.origin

            # notify neighbors
            self.send_update_messages()
            
        elif message.root == self.info['root'] and 1+message.distance > self.info['distance']:
            if message.pathThrough == True:
            # root is the same, distance is the same, just to link the neighbor to activelinks as the neighbor relies on this switch to root
                self.info['activelinks'][message.origin] = True
            else:
                # print("testing if ever been here")
                self.info['activelinks'][message.origin] = False

        elif message.root == self.info['root'] and 1+message.distance == self.info['distance']:
            if message.origin < self.info['switchThrough']:
            # root is the same, distance is the same, but origin has smaller value than switchThrough. need to update and notify neighbors
                # print("testing if ever been here")
                self.info['activelinks'][self.info['switchThrough']] = False
                self.info['activelinks'][message.origin] = True
                self.info['switchThrough'] = message.origin
            elif message.origin > self.info['switchThrough']:
                # print("testing if ever been here")
                self.info['activelinks'][message.origin] = False

            # notify neighbors
            self.send_update_messages()

    def generate_logstring(self):
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked 
        #      only after the simulaton is complete.  Output the links included in the 
        #      spanning tree by increasing destination switch ID on a single line. 
        #      Print links as '(source switch id) - (destination switch id)', separating links 
        #      with a comma - ','.  
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string 
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        log_str = []
        # print('now printing: \n')
        # print(self.switchID)
        # print(self.info['activelinks'])
        for activelink, if_true in sorted(self.info['activelinks'].items()):
            if if_true:
                log_str.append(str(self.switchID)+' - '+str(activelink)) 
        # print('str looks like:', log_str)      
        return ', '.join(log_str)