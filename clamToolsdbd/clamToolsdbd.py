#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------------
# Python Command-Line tools for clamav (clamToolsdbd)          |
# Created by q3aql (q3aql@openmailbox.org)                     |
# Licensed by GPL v.3                                          |
# Last update: 01-03-2016                                      |
#                                                              |
# Dependences: ClamAV & Rsync (Optional)                       |
# Compatible with Python 3.x                                   |
# --------------------------------------------------------------
version="1.0.1"

#Import python-modules
import subprocess
import os
import sys
import time
import random

#Check if your system use Python 3.x
if sys.version_info<(3,0):
	print ("")
	print ("You need python 3.x to run this program.")
	print ("")
	exit()

#Function to clear screen
def ClearScreen():
	if sys.platform == "cygwin":
		print (300 * "\n")
	elif os.name == "posix":
		os.system("clear")
	elif os.name == "nt":
		os.system("cls")
	else:
		print ("Error: Unable clear screen")
					
#Detect system & PATH of user folder
if os.name == "posix":
	HomeUser=os.environ["HOME"]
	os.chdir(HomeUser)
	print ("POSIX detected")
elif os.name == "nt":
	HomeUser=os.environ["USERPROFILE"]
	os.chdir(HomeUser)
	print ("Windows detected")

#Create clamTools folders
if not os.path.exists(".clamTools"):
	os.makedirs(".clamTools")
	os.chdir(".clamTools")
if os.path.exists(".clamTools"):
	os.chdir(".clamTools")
if not os.path.exists("db"):
	os.makedirs("db")
if not os.path.exists("logs"):
	os.makedirs("logs")
if not os.path.exists("qtn"):
	os.makedirs("qtn")
if not os.path.exists("pid"):
	os.makedirs("pid")

#Set variables of clamTools
if os.name == "posix":
	clamToolsdb=HomeUser+"/.clamTools/db/"
	clamToolslogs=HomeUser+"/.clamTools/logs/"
	clamToolsqtn=HomeUser+"/.clamTools/qtn/"
	clamToolspid=HomeUser+"/.clamTools/pid/"
	clamToolshome=HomeUser+"/.clamTools/"
	LockFile=HomeUser+"/.clamTools/clamToolsdbd.lock"
elif os.name == "nt":
	clamToolsdb=HomeUser+"\\.clamTools\\db\\"
	clamToolslogs=HomeUser+"\\.clamTools\\logs\\"
	clamToolsqtn=HomeUser+"\\.clamTools\\qtn\\"
	clamToolspid=HomeUser+"\\.clamTools\\pid\\"
	clamToolshome=HomeUser+"\\.clamTools\\"
	LockFile=HomeUser+"\\.clamTools\\clamToolsdbd.lock"

#Check if exists 'freshclam.conf'
if os.path.isfile("freshclam.conf"):
	print ("freshclam.conf exists")
else:
	print ("freshclam.conf created")
	clamToolscf=open('freshclam.conf','w')
	clamToolscf.close()
	clamToolscf=open('freshclam.conf','a')
	clamToolscf.write('DatabaseOwner clamav\n')
	clamToolscf.write('UpdateLogFile '+clamToolslogs+'freshclam.log\n')
	clamToolscf.write('LogVerbose false\n')
	clamToolscf.write('LogSyslog false\n')
	clamToolscf.write('LogFacility LOG_LOCAL6\n')
	clamToolscf.write('LogFileMaxSize 0\n')
	clamToolscf.write('LogTime true\n')
	clamToolscf.write('SafeBrowsing Yes\n')
	clamToolscf.write('Foreground false\n')
	clamToolscf.write('Debug false\n')
	clamToolscf.write('MaxAttempts 5\n')
	clamToolscf.write('DatabaseDirectory '+clamToolsdb+'\n')
	clamToolscf.write('DNSDatabaseInfo current.cvd.clamav.net\n')
	clamToolscf.write('AllowSupplementaryGroups false\n')
	clamToolscf.write('PidFile '+clamToolspid+'freshclam.pid\n')
	clamToolscf.write('ConnectTimeout 30\n')
	clamToolscf.write('ReceiveTimeout 30\n')
	clamToolscf.write('TestDatabases yes\n')
	clamToolscf.write('ScriptedUpdates yes\n')
	clamToolscf.write('CompressLocalDatabase no\n')
	clamToolscf.write('Bytecode true\n')
	clamToolscf.write('Checks 24\n')
	clamToolscf.write('DatabaseMirror clamav.oucs.ox.ac.uk\n')
	clamToolscf.write('DatabaseMirror clamav.irontec.com\n')
	clamToolscf.write('DatabaseMirror db.local.clamav.net\n')
	clamToolscf.write('DatabaseMirror database.clamav.net\n')
	clamToolscf.close()
	
#Check if clamav is correctly installed
from subprocess import PIPE, Popen
try:
	clamscanCheck = Popen(['clamscan', '-V'], stdout=PIPE, stderr=PIPE)
	clamscanCheck.stderr.close()
	freshclamCheck = Popen(['freshclam', '-V'], stdout=PIPE, stderr=PIPE)
	freshclamCheck.stderr.close()
except:
	ClearScreen()
	print ("")
	print ("* Error: 'clamav' is not installed!")
	print ("")
	print ("* Help:")
	print ("")
	print ("   - http://www.clamav.net/downloads#sourcecode")
	print ("   - http://www.clamav.net/downloads#otherversions")
	print ("")
	PauseExit=input("+ Press ENTER to exit ")
	exit()
	
#Check if rsync is installed (optional)	
from subprocess import PIPE, Popen
try:
	rsyncCheck = Popen(['rsync', '--version'], stdout=PIPE, stderr=PIPE)
	rsyncCheck.stderr.close()
	RsyncInstalled="yes"
	print ("Sanesecurity signatures enabled (rsync)")
except:
	RsyncInstalled="no"
	print ("Sanesecurity signatures disabled (rsync)")

# Initial Mirror
URL="rsync.sanesecurity.net"
MIRROR="NET"
	
def DownloadSanesecuritySigns():
	os.chdir(clamToolsdb)
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/winnow.attachments.hdb . > sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/winnow.complex.patterns.ldb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/winnow_bad_cw.hdb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/winnow_extended_malware.hdb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/winnow_extended_malware_links.ndb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/winnow_malware.hdb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/winnow_malware_links.ndb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/winnow_phish_complete_url.ndb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/rogue.hdb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/scamnailer.ndb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/malwarehash.hsb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/spamimg.hdb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/badmacro.ndb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/hackingteam.hsb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/crdfam.clamav.hdb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/porcupine.ndb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/junk.ndb . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/sanesecurity.ftm . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/sigwhitelist.ign2 . >> sanesecurity.log")
	os.system("rsync -avhp rsync://"+URL+"/sanesecurity/blurl.ndb . >> sanesecurity.log")
	os.chdir(clamToolshome)

#Check if clamToolsdbd is running.
if os.path.isfile("clamToolsdbd.lock"):
	readLock=open('clamToolsdbd.lock', 'r', encoding="latin-1")
	LockN=readLock.read()
	readLock.close()
	ClearScreen()
	print ("Checking "+LockFile+"...")
	time.sleep(4)
	readLock2=open('clamToolsdbd.lock', 'r', encoding="latin-1")
	LockN2=readLock2.read()
	readLock2.close()
	if LockN != LockN2:
		ClearScreen()
		print ("")
		print ("* clamToolsdbd is already running.")
		print ("")
		PauseExit=input("+ Press ENTER to exit ")
		exit()
if not os.path.isfile("clamToolsdbd.lock"):
	createLock=open('clamToolsdbd.lock','w')
	createLock.write(str(random.randrange(135790)))
	createLock.close()

#Function to lock process.
def LockProcess():
	createLock=open('clamToolsdbd.lock','w')
	createLock.write(str(random.randrange(135790)))
	createLock.close()

#Function to sleep 'N' seconds.
def TimeSleep(N):
	Time=1
	while Time < N:
		createLock=open('clamToolsdbd.lock','w')
		createLock.write(str(random.randrange(135790)))
		createLock.close()
		time.sleep(1)
		Time=Time + 1
	
#Run clamToolsdbd daemon
ClearScreen()
LockProcess()
editlog=open(clamToolslogs+'clamToolsdbd.log','w')
CurrentTime = time.strftime("%H:%M")
print ("[clamToolsdbd] ["+CurrentTime+"] Initialized clamToolsdbd v"+version+" (Ctrl+C to stop).")
print ("[clamToolsdbd] ["+CurrentTime+"] Log in "+clamToolslogs+"clamToolsdbd.log.")
print ("[clamToolsdbd] ["+CurrentTime+"] Waiting 30 seconds...")
editlog.write("[clamToolsdbd] ["+CurrentTime+"] Initialized clamToolsdbd v"+version+"\n")
editlog.write("[clamToolsdbd] ["+CurrentTime+"] Waiting 30 seconds...\n")
editlog.close()
TimeSleep(30)

DataBaseDaemon = 1
while DataBaseDaemon <= 2:
	CurrentTime = time.strftime("%H:%M")
	editlog=open(clamToolslogs+'clamToolsdbd.log','a')
	if RsyncInstalled == "yes":
		try:
			print ("[clamToolsdbd] ["+CurrentTime+"] Sanesecurity signatures enabled (rsync) (downloading) ("+MIRROR+").")
			editlog.write("[clamToolsdbd] ["+CurrentTime+"] Sanesecurity signatures enabled (rsync) (downloading) ("+MIRROR+").\n")
			editlog.close()
			if MIRROR == "NET":
				URL="rsync.sanesecurity.co.uk"
				MIRROR="UK"
			elif MIRROR == "UK":
				URL="rsync.sanesecurity.net"
				MIRROR="NET"
			DownloadSanesecuritySigns()
			CurrentTime = time.strftime("%H:%M")
			editlog=open(clamToolslogs+'clamToolsdbd.log','a')
			print ("[clamToolsdbd] ["+CurrentTime+"] Sanesecurity signatures downloaded successfully.")
			editlog.write("[clamToolsdbd] ["+CurrentTime+"] Sanesecurity signatures downloaded successfully.\n")
			editlog.close()
		except:
			CurrentTime = time.strftime("%H:%M")
			editlog=open(clamToolslogs+'clamToolsdbd.log','a')
			print ("[clamToolsdbd] ["+CurrentTime+"] Error downloading Sanesecurity signatures ("+MIRROR+").")
			editlog.write("[clamToolsdbd] ["+CurrentTime+"] Error downloading Sanesecurity signatures ("+MIRROR+").\n")
			editlog.close()
	elif RsyncInstalled == "no":
		print ("[clamToolsdbd] ["+CurrentTime+"] Sanesecurity signatures disabled (rsync) (aborted).")
		editlog.write("[clamToolsdbd] ["+CurrentTime+"] Sanesecurity signatures disabled (rsync) (aborted).\n")
		editlog.close()
	editlog=open(clamToolslogs+'clamToolsdbd.log','a')
	print ("[clamToolsdbd] ["+CurrentTime+"] Updating ClamAV virus database signatures....")
	editlog.write("[clamToolsdbd] ["+CurrentTime+"] Updating ClamAV virus database signatures....\n")
	editlog.close()
	editlog=open(clamToolslogs+'clamToolsdbd.log','a')
	try:
		os.system("freshclam --quiet --config-file=freshclam.conf")
		CurrentTime = time.strftime("%H:%M")
		print ("[clamToolsdbd] ["+CurrentTime+"] ClamAV virus database signatures updated successfully.")
		editlog.write("[clamToolsdbd] ["+CurrentTime+"] ClamAV virus database signatures updated successfully.\n")
		editlog.close()
	except:
		CurrentTime = time.strftime("%H:%M")
		print ("[clamToolsdbd] ["+CurrentTime+"] Error updating ClamAV virus database signatures.")
		editlog.write("[clamToolsdbd] ["+CurrentTime+"] Error updating ClamAV virus database signatures.\n")
		editlog.close()
	editlog=open(clamToolslogs+'clamToolsdbd.log','a')
	print ("[clamToolsdbd] ["+CurrentTime+"] Next update in one hour...")
	editlog.write("[clamToolsdbd] ["+CurrentTime+"] Next update in one hour...\n")
	editlog.close()
	TimeSleep(3600)
