#!/usr/bin/python

##################################################################
# Script to connect to a 3270 server and take a screenshot	 #
#                                                                #
# Requirements: Python, s3270 and optionally x3270               #
# Created by: Soldier of Fortran (@mainframed767)                #
# Usage: Given a hostname[:port] or file of hosts[:ports] 	 #
# connects and takes a screenshot of the first screen            #
#                                                                #
# Copyright GPL 2012                                             #
##################################################################

from py3270 import EmulatorBase
import time #needed for sleep
import sys 
import argparse #needed for argument parsing
import platform #needed for OS check

from blessings import Terminal
t = Terminal()

def Grab_Screen(hostname):
	command = 'printtext(html,' + hostname + '.html)'
	em.exec_command(command)

def Connect_to_ZOS(hostname):
	#connects to the target machine and sleeps for 'sleep' seconds
	trying = False
	try:
		em.connect(hostname)
		trying = True
	except:
		trying = False	
	return trying

print t.bold + '''

      8""8""8 8""""   8""""8                             
      8  8  8 8       8      eeee eeeee  eeee eeee eeeee 
      8e 8  8 8eeee   8eeeee 8  8 8   8  8    8    8   8 
      88 8  8 88          88 8e   8eee8e 8eee 8eee 8e  8 
      88 8  8 88      e   88 88   88   8 88   88   88  8 
      88 8  8 88      8eee88 88e8 88   8 88ee 88ee 88  8 						                                           

						By: Soldier of Fortran
						   (@mainframed767)

''' + t.normal


#start argument parser
parser = argparse.ArgumentParser(description='MF Screen - A script to capture the first screen of a mainframe',epilog='Get it!')
parser.add_argument('-m','--mainframe', help='target IP address or Hostname and port: TARGET[:PORT] default port is 23',dest='target')
parser.add_argument('-f','--file', help='a file containing a listing of hosts[:ports] to connect to.',dest='hosts')
parser.add_argument('-s','--sleep',help='Seconds to sleep between actions (increase on slower systems). The default is 1 second.',default=1,type=int,dest='sleep')
parser.add_argument('-t','--tor',help='Use TOR proxy to connect. Syntax is TYPE:HOSTNAME:PORT for any TOR proxy. Most likely socks5d:localhost:9050',dest='tor')
args = parser.parse_args()
results = parser.parse_args() # put the arg results in the variable results

if platform.system() == 'Darwin': #'Darwin'
	class Emulator(EmulatorBase):
		x3270_executable = 'MAC_Binaries/x3270'
		s3270_executable = 'MAC_Binaries/s3270'
		if results.tor is not None: 
			s3270_args = ['-proxy', results.tor,]
			x3270_args = ['-proxy', results.tor,'-script']
elif platform.system() == 'Linux':
	class Emulator(EmulatorBase):
		x3270_executable = '/usr/bin/x3270'
		s3270_executable = '/usr/bin/s3270' 
		if results.tor is not None: 
			s3270_args = ['-proxy', results.tor,]
			x3270_args = ['-proxy', results.tor,'-script']
elif platform.system() == 'Windows':
	class Emulator(EmulatorBase):
		s3270_executable = 'Windows_Binaries/ws3270.exe'
		if results.tor is not None: s3270_args = ['-proxy', results.tor]
else:
	print t.red + t.bold + '      [!] Your Platform:', platform.system(), 'is not supported at this time. Windows support should be available soon' + t.normal
	sys.exit()


if not results.target and not results.hosts:
	print t.red + t.bold + '      [!] You gotta specify a host or a file. Try -h for help.' + t.normal
	sys.exit()

if not results.hosts:
	print t.green_bold + '      [' + t.white + ' X ' + t.green +'] Target:',
	print t.white(results.target) + t.normal
	print t.green_bold + '      [   ] Multiple targets file:' + t.normal
if not results.target:
	print t.green_bold + '      [   ] Target:'
	print t.green_bold + '      [' + t.white_bold + ' X ' + t.green +'] Multiple targets file:', 
	print t.white(results.hosts) + t.normal
	
if results.sleep > 1:
	print t.green_bold + '      [' + t.white + ' X ' + t.green +'] Sleep set to:',
	print t.white(str(results.sleep)) + t.normal
else:
	print  t.green_bold + '      [   ] Sleep set to:',
	print t.white(str(results.sleep)) + t.normal

if results.tor is not None:
	print t.green_bold + '      [' + t.white + ' X ' + t.green +'] Tor Proxy:',
	print t.white(results.tor) + t.normal
else:
	print t.green_bold + '      [   ] Tor Proxy:' + t.normal


print ''

if not results.hosts: #enter single server mode	
	em = Emulator(visible=True)
	print t.blue_bold + '      +     Connecting to:',
	print t.white(results.target)	
	Connect_to_ZOS(results.target)
	print t.green_bold('      +     Connected')
	print t.blue_bold + '      +     Sleeping for',
	print t.white(str(results.sleep)) + t.normal
	snooze = results.sleep -1
	while snooze >0:
		time.sleep(1)
		print '                        ',
		print t.white_bold(str(snooze)) + t.normal
		snooze -=1
	print t.blue_bold + '      +     Grabbing screen to', 
	print t.white(results.target + '.html')
	Grab_Screen(results.target)	
	em.terminate()
else:
	hostsfile=open(results.hosts) #open the usernames file
	for hostnames in hostsfile:
		em = Emulator(visible=True)
		print t.blue_bold + '      +     Connecting to:',
		print t.white(hostnames.strip())	
		Connect_to_ZOS(hostnames.strip())
		print t.green_bold('      +     Connected')
		print t.blue_bold + '      +     Sleeping for',
	        print t.white(str(results.sleep)) + t.normal
	        snooze = results.sleep -1
	        while snooze >0:
        	        time.sleep(1)
                	print '                        ',
		        print t.white_bold(str(snooze)) + t.normal
                	snooze -=1
		print t.blue_bold + '      +     Grabbing screen to', 
		print t.white(hostnames.strip() + '.html')
		Grab_Screen(hostnames.strip())
		em.terminate()
# And we're done. Close the connection
