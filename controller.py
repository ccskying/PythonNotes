# Assignment 2 Skeleton

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet
from pox.lib.packet import ipv4

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_firewall (self, packet, packet_in):
    # The code in here will be executed for every packet.
    '''
    packet is a ehernet class object
    '''

    #Create objects of flow table and match feaure
    #Set the value of 'dl_type' in match feature
    flow_mod = of.ofp_flow_mod()
    block = of.ofp_match()
    Type = packet.type
    block.dl_type = Type

    # Check the tpye is IPv4, IPv6, ARP, or others
    if Type == ethernet.IP_TYPE : # If IPv4
      # Set the value of 'protocol' in match feature
      protocol = packet.payload.protocol
      block.nw_proto = protocol
      flow_mod.priority = 1 # Defuat use the lowest priority
      
      # If protocol is TCP, set the action as process as normal
      # and set the priority as medium
      if protocol == ipv4.TCP_PROTOCOL:
        print('accept')
        action = of.ofp_action_output(port = of.OFPP_NORMAL)
        flow_mod.actions.append(action)
        flow_mod.priority = 32768 

    # If type is ARP, set the action as process as normal
    # and set the priority as medium
    elif (Type == ethernet.ARP_TYPE or Type == ethernet.RARP_TYPE ) :
      print('accept')
      action = of.ofp_action_output(port = of.OFPP_NORMAL)
      flow_mod.actions.append(action)
      flow_mod.priority = 32768

    # Otherwise, just don't set the action. (defualt action is 'drop')
    else :
      print('drop')
      flow_mod.priority = 1
    flow_mod.match = block
    self.connection.send(flow_mod)



  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    print('event ',type(event))
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
