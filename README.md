# Medium.com writeup
[link](https://jl4730.medium.com/spanning-tree-protocol-for-network-switches-a6a7e89e7de6)

# Files
## Switch.py
Implement the functionality of the Spanning Tree Protocol to generate a Spanning Tree for each Switch

## Spanning-Tree-Protocol-for-Network-Switches
In this project, we will develop a simplified distributed version of the Spanning Tree Protocol that can be run on an arbitrary layer 2 topology.

## Topology.py 
Represents a network topology of layer 2 switches. This class reads in the specified topology and arranges it into a data structure that your switch code can access

## StpSwitch.py
A base class of the derived class you will code in Switch.py. The base class StpSwitch.py abstracts certain implementation details to simplify your tasks.

## Message.py 
This class represents a simple message format you will use to communicate between switches, similar to what was described in the course lectures. Specifically, you will create and send messages in Switch.py by declaring a message as:
```
msg = Message(claimedRoot, distanceToRoot, originID, destinationID, pathThrough
```
and assigning the correct data to each input. Message format may not be changed. See the comments in Message.py for more information on the data in these variables.

## run_spanning_tree.py
A simple "main" file that loads a topology file (see XXXTopo.py below), uses that data to create a Topology object containing Switches, and starts the simulation

## XXXTopo.py, etc 
These are topology files that you will pass as input to the run_spanning_tree.py file

## sample_output.txt
Example of a valid output file for Sample.py as described in the comments in Switch.py.

# Testing
To run your code on a specific topology (SimpleLoopTopo.py in this case) and output the results to a text file (out.txt in this case), execute the following command:
```
python run_spanning_tree.py SimpleLoopTopo out.txt
```
NOTE: “SimpleLoopTopo” is not a typo in the example command – don’t include the .py extension.
