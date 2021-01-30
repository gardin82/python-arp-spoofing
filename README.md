Python Arp Spoofing

OVERVIEW:

These scripts are pentesting tools.
Only use these programs with permission.

You can run these on different os'.


CREATORS:
these scripts are not made by me. i have just modyfied them a bit.

"script1" is originally from "https://github.com/shrestha-tripathi/offensive-python/blob/master/arp_spoof.py".
"script2" is originally from "https://www.thepythoncode.com/article/building-arp-spoofer-using-scapy"

HOW TO USE:

Script1

flags: -t --target -m --mode -?
-t is required.

The mode flag has two options.
1. spoofer
With the spoofer flag enabled you don't restore the arp tables when closing the program (with ctrl-c).
2. restore
With the restore flag enabled you only restore the arp tables.

And with no flag enabled then you spoof the arp tables then when you close the program you restore.

-t or --target is where you specify target ip.

Examples:


python script1.py -t 192.168.1.59
python script1.py -m spoofer -t 192.168.0.23
python script1.py -m restore -t 192.168.1.44

Script2

arguments:

first argument is target ip
second argument is gateway/router ip

both are required.

Examples:

linux:
sudo python3 script2.py 192.168.1.45 192.168.1.1
sudo python3 script2.py 192.168.0.54 192.168.0.1

windows:
python script2.py 192.168.1.45 192.168.1.1
python script2.py 192.168.0.54 192.168.0.1

COMPATABILITY:

script1 only works with windows.
script2 works with linux and should work on windows.

RECOMMENDATION:
if you are using windows then use script1.
if you are using linux then use script2.

