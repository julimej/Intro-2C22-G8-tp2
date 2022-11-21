import sys
import os
import time

from pox.core import core

import pox.openflow.libopenflow_01 as of
import pox.openflow.discovery
import pox.openflow.spanning_tree
import pox.forwarding.l2_learning

import pox.lib.packet as pkt
from pox.lib.revent import EventMixin
from pox.lib.util import dpid_to_str
from pox.lib.addresses import IPAddr, EthAddr

logger = core.getLogger()

PROTOCOL_NAME_TO_PROTOCOL = {"UDP": pkt.ipv4.UDP_PROTOCOL, "TCP": pkt.ipv4.TCP_PROTOCOL, "ICMP": pkt.ipv4.ICMP_PROTOCOL}

class Controller(EventMixin):
	def __init__(self, firewall_switch):
		self.listenTo(core.openflow)
		self.firewall_switch = firewall_switch
		self.parse_rules()
		logger.debug(self.rules)

	def parse_rules(self):
		rules = []
		with open(os.path.join(sys.path[0],"config"),"r") as config_file:
			for line in config_file:
				rule = line.rstrip("\n").split(",")
				if (len(rule) > 0) : # evito lineas vacias
				    rules.append(rule)
		self.rules = rules

	def echo(self):
		logger.info("echo")

	def _handle_ConnectionUp(self, event):

		logger.debug("Looking for " + str(self.firewall_switch))
		logger.debug("Switch " + str(event.dpid))
		if int(event.dpid) == int(self.firewall_switch):
			for rule in self.rules:
				logger.debug("rule " + str(rule))
				self.create_match(event,rule)

	def drop_packet_with_match(self, match, event):
		msg = of.ofp_flow_mod()
		msg.match = match
		msg.actions.append(of.ofp_action_tp_port.set_dst(of.OFPP_NONE))
		event.connection.send(msg)

	def create_match(self, event, rule):
		match = of.ofp_match(
			dl_type=pkt.ethernet.IP_TYPE,
		)

		if rule[0] != "any":
			match.nw_src = IPAddr(rule[0])

		if rule[1] != "any":
			match.tp_src = int(rule[1])

		if rule[2] != "any":
			match.nw_dst = IPAddr(rule[2])

		if rule[3] != "any":
			match.tp_dst = int(rule[3])

		if rule[4] != "any":
			match.nw_proto = PROTOCOL_NAME_TO_PROTOCOL[rule[4]] 
		
		logger.debug(match)

		self.drop_packet_with_match(match,event)

		
		

def launch(firewall_switch = 0):
	logger.debug("firewall_switch setted to " + firewall_switch)

	core.registerNew(Controller,firewall_switch)
	pox.forwarding.l2_learning.launch()
