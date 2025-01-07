import nmap

class Network(object):
	def __init__(self):
		ip = input("Enter ip address : ")
		self.ip = ip

	def networkscanner(self):
		network = self.ip + '/24'
	
		print("scanning Please wait....")

		nm = nmap.PortScanner()
		nm.scan(hosts = network, arguments='-sn')
		hosts_list = [(x,nm[x]['status']['state']) for x in nm.all_hosts()]
		if len(hosts_list) == 0:
			print("No Hosts are found...")
			pass
		for host, status in hosts_list:
			print("Host\t{}".format(host))

if __name__ == "__main__":
	D = Network()
	D.networkscanner()
