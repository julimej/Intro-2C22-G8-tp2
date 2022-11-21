from mininet . topo import Topo

def int2dpid( dpid ):
   try:
      dpid = hex( dpid )[ 2: ]
      dpid = '0' * ( 16 - len( dpid ) ) + dpid
      return dpid
   except IndexError:
      raise Exception( 'Unable to derive default datapath ID - '
                       'please either specify a dpid or use a '
		       'canonical switch name such as s23.' )

class MyTopo ( Topo ) :
	def __init__ ( self, number_switches ) :
	# Initialize topology
		Topo.__init__ ( self )
		number_switches += 1
		# Create switch
		s_first = self.addSwitch('switch_1', dpid=int2dpid(1))
		s_last = self.addSwitch('switch_' + str(number_switches + 1), dpid=int2dpid(number_switches + 1))
		# Create hosts
		h1 = self.addHost('host_1')
		h2 = self.addHost('host_2')
		h3 = self.addHost('host_3')
		h4 = self.addHost('host_4')

		# Add links between switches and hosts self.addLink( s1 , s2 )
		switches = [s_first]
		switches += [self.addSwitch('switch_' + str(switch), dpid=int2dpid(switch)) for switch in range(2,number_switches+1)]
		switches.append(s_last)

		for iter_num in range(len(switches)-1):
			print(iter_num)
			print(switches[iter_num])
			print(switches[iter_num+1])
			self.addLink(switches[iter_num],switches[iter_num+1])



		self.addLink( s_first, h1 )
		self.addLink( s_first, h2 )
		self.addLink( s_last, h3 )
		self.addLink( s_last, h4 )

topos = {'customTopo': MyTopo }