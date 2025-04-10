# mc_msg2dstar
Simple code to send messages from meshcom network to DSTAR devices

A meshcom lora gateway node can send "received packets" to an ip or in a broadcast manner via udp. This code acquires packets that respect certain rules (messages) and sends them to a dstar gateway. This gateway will send them out in RF on the connected repeater bridge and they can be displayed on the dstar radio devices. The system was tested with the two gateways (lora and ircddbgateway) present on the same lan network and the code running on Pi-star (the same of the repeater).<br>

On the dstar repeater bridge side, the Pi-star distribution is used but any solution is fine as long as it contains the texttransmitd software by Jonathan G4KLX (this is the path **/usr/local/bin/texttransmitd** if it differs then change it in the code). Pi-star has a firewall, you need to add a rule in iptables, better in the /root/ipv4.fw file so that it is always present even at reboot and updates. For the management of commands in Pi-star refer to the support groups or forums.<br>

The rule for iptables is:
<br><br>
**iptables -I INPUT -p udp --dport 1799 -j ACCEPT**
<br><br>
On the meshcom gateway node the commands to execute are:<br><br>
**--extudp on** (enables sending of received data via network/lan, udp protocol)<br>
**--extudpip 192.168.0.4** (insert the ip where texttransmitd is present)<br><br>

The udp port used is forcedly 1799. If the systems are not present on the same lan, it is also necessary to manage the relative nat and opening ports on the firewall that manages the connectivity.<br>

In the code, configurations section, insert the name of the repeater to which the message will be sent (make sure that the length is always 8 characters, callsign plus space/s plus module, as dstar syntax requires) and the recipient callsign of the message. This is the filter that checks the messages and will send to the repeater only those addressed to this callsign (it could be the meshcom node callsign for convenience). The message text is sized to 20 characters for correct display on the devices.<br>

We can try to send through the meshcom APP (connected to a node) or via web interface a message addressed to the callsign (node ​​present on the meshcom server) specified in the configuration. The message will be (with its times due to the type of mesh network in use) taken in charge and transmitted to the repeater that will go out on the radio with callsign/INFO.<br>

To set the code in background:<br>
**nohup python3 mc_msg2dstar.py &**
