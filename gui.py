# -*- coding: utf-8 -*-

# Gui

# imports

import settings as settings
import log as log
import network as network
import monitor

from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog
import time

# Main Window Class


class mainWindow(Frame):

	def __init__(self, mWindow=None):
		Frame.__init__(self, mWindow)
		self.mWindow = mWindow
		self.init_window()

	def init_window(self):

		self.mWindow.title("Lan Map v0.2")

		# main layout frames of main window
		self.toolbarFrame = Frame(self.mWindow, height=30, bd=1)
		self.nodelistFrame = Frame(self.mWindow, bd=1, relief=SUNKEN)
		self.nodeMapFrame = Frame(self.mWindow, bd=1, relief=SUNKEN)
		self.statusbarFrame = Frame(self.mWindow, height=20, bd=1)

		self.toolbarFrame.pack(side=TOP, fill=X, ipadx=15, ipady=5)
		self.statusbarFrame.pack(side=BOTTOM, fill=X, ipadx=15, ipady=2)
		self.nodelistFrame.pack(side=LEFT, fill=Y)
		self.nodeMapFrame.pack(side=RIGHT, fill=BOTH, expand=True, ipadx=15)

		# Toolbar objects of main window

		self.monitorButton = Button(self.toolbarFrame, text="Start \nMonitoring",
			command=lambda: self.startMonitor())
		self.monitorButton.pack(side=LEFT, fill=Y, pady=2, ipadx=8)

		self.scanButton = Button(self.toolbarFrame, text="Scan for \nNetwork Nodes")
		self.scanButton.pack(side=LEFT, fill=Y, pady=2, ipadx=8)
		self.scanButton.bind("<Button-1>", self.scannerWindow)

		self.editButton = Button(self.toolbarFrame, text="Edit \nNetwork Nodes")
		self.editButton.pack(side=LEFT, fill=Y, pady=2, ipadx=8)
		self.editButton.bind("<Button-1>", self.editNodesWindow)

		self.loadImageButton = Button(self.toolbarFrame, text="Load \nMap Image",
			command=lambda: self.loadBgImage())
		self.loadImageButton.pack(side=LEFT, fill=Y, pady=2, ipadx=8)

		self.clearImageButton = Button(self.toolbarFrame, text="Clear \nMap Image",
			command=lambda: self.clearBgImage())
		self.clearImageButton.pack(side=LEFT, fill=Y, pady=2, ipadx=8)

		#self.saveNetworkButton = Button(self.toolbarFrame, text="Save \nNetwork Layout")
		#self.saveNetworkButton.pack(side=LEFT, fill=Y, pady=2, ipadx=8)

		#self.loadNetworkButton = Button(self.toolbarFrame, text="Load \nNetwork Layout")
		#self.loadNetworkButton.pack(side=LEFT, fill=Y, pady=2, ipadx=8)

		self.logButton = Button(self.toolbarFrame, text="Open Log")
		self.logButton.pack(side=RIGHT, fill=Y, pady=2, ipadx=2)
		self.logButton.bind("<Button-1>", self.logWindow)

		self.settingsButton = Button(self.toolbarFrame, text="Settings")
		self.settingsButton.pack(side=RIGHT, fill=Y, pady=2, ipadx=2)

		# Nodelist objects in MainWindow

		self.nodelist = Canvas(self.nodelistFrame,background="#555555", width=280)
		self.nodelistScrollbar = Scrollbar(self.nodelistFrame, orient="vertical",
			command=self.nodelist.yview)
		self.nodelistScrollbar.pack(side=RIGHT, fill=Y)
		self.nodelist.configure(yscrollcommand=self.nodelistScrollbar.set)
		self.nodelist.pack(side=LEFT, fill=BOTH, expand=True)

		self.updateNodelist()

		# networkmap of mainwindow (right)

		self.nodeMap = Canvas(self.nodeMapFrame,background="#888888", scrollregion=(0,0,1800,1500))
		self.nodeMapScrollbarx = Scrollbar(self.nodeMapFrame, orient=HORIZONTAL)
		self.nodeMapScrollbary = Scrollbar(self.nodeMapFrame, orient=VERTICAL)
		self.nodeMapScrollbary.pack(side=RIGHT, fill=Y)
		self.nodeMapScrollbary.config(command=self.nodeMap.yview)
		self.nodeMapScrollbarx.pack(side=BOTTOM, fill=X)
		self.nodeMapScrollbarx.config(command=self.nodeMap.xview)
		self.nodeMap.config(xscrollcommand=self.nodeMapScrollbarx.set,
			                   yscrollcommand=self.nodeMapScrollbary.set)
		self.nodeMap.pack(side=TOP, fill=BOTH, expand=True)
		self.nodeMapWidth = self.nodeMap.winfo_reqwidth()
		self.nodeMapHeight = self.nodeMap.winfo_reqheight()

		# event bindings nodeMap
		self.nodeMap.bind("<Configure>", self.resizeMap) # get resize events
		self.nodeMap.bind("<B1-Motion>", self.moveNode) #move node
		self.nodeMap.bind("<ButtonRelease-1>", self.updateMapAfterMove) #update map after move

		self.updateMap()

		# Statusbar Objects of MainWindow

		self.statusMsg = Label(self.statusbarFrame, text="Idle")
		self.statusMsg.pack(side=LEFT, padx=3)

		self.statusOnlineNodes = Label(self.statusbarFrame, text="|  Nodes online: 0.")
		self.statusOnlineNodes.pack(side=RIGHT, padx=3)

		ownip = network.getMyIp()
		self.statusIp = Label(self.statusbarFrame, text="Current Ipv4: " + ownip)
		self.statusIp.pack(side=RIGHT, padx=3)

	# Nodelist functions

	def updateNodelist(self):
		"""updates the list with nodes"""

		# clear the canvas first, memory hog prevention
		self.nodelist.delete("all")

		# display the nodelist headers
		self.nodelist.create_rectangle(2,1, 280, 24,
				fill="#BBBBBB")
		self.nodelist.create_text(10,13, text="IPv4 address", anchor=W, fill="#000000")
		self.nodelist.create_text(125,13, text="Name", anchor=W, fill="#000000")

		# value for lightgreying every other nodeline
		lightgrey = 0

		# display each node in the nodelist
		for node in settings.nodes:
			self.position = node[11]
			self.posTop = self.position*24+25
			self.posBottom = self.posTop+24

			self.posText = int(self.posTop)+12
			self.nodeIp4 = str(node[6][0])
			self.nodeName = str(node[0])

			# set status colors
			self.nodeStatus = "white"
			nodeText = "black"
			if settings.monitorRunning:
				if node[5]=="Online":
					self.nodeStatus = "#" + settings.mapperNodeStatusColorOnline + ""
				if node[5]=="Offline":
					self.nodeStatus = "#" + settings.mapperNodeStatusColorOffline + ""
					nodeText = "white"
				if node[5]=="Awaiting":
					self.nodeStatus = "#" + settings.mapperNodeStatusColorAwaiting + ""
			else:
				if lightgrey==0:
					self.nodeStatus = "#ffffff"
					lightgrey = 1
				else:
					self.nodeStatus = "#dddddd"
					lightgrey = 0

			self.nodelist.create_rectangle(2,self.posTop, 280, self.posBottom,
				fill=self.nodeStatus)
			if network.validIp4(self.nodeIp4) and node[4]:
				self.nodelist.create_text(10,self.posText, text=self.nodeIp4, fill=nodeText,
					anchor=W, tags=(self.nodeName,"ipv4"))
			else:
				self.nodelist.create_text(10, self.posText, text="", fill=nodeText,
					anchor=W, tags=(self.nodeName,"ipv4"))
			self.nodelist.create_text(125,self.posText, text=self.nodeName,
				fill=nodeText, anchor=W, tags=(self.nodeName,"name"))

	def moveNodeInList(self, event):
		"""click and move nodes on the map """
		canvas = event.widget
		x = canvas.canvasx(event.x)
		y = canvas.canvasy(event.y)
		itemCoord = canvas.coords(CURRENT)
		try:
			offsetX = x - (itemCoord[0])
			offsetY = y - (itemCoord[1])
			for tag in canvas.gettags(CURRENT):
				for node in settings.nodes:
					if tag==node[0]:
						canvas.move(CURRENT, offsetX, offsetY)
		except:
			pass



 # networkmap functions

	def setMapImage(self):
		"""set and resize the background image/map/buildingplans"""

		imageLocation = settings.mapperImage
		imageScaling = settings.mapperImageScaling

		# check if any background image is set
		if(imageLocation==""):
			return
		else:
			# delete current image, memoryhog prevention
			self.nodeMap.delete("bg")

			# load image for width/height
			self.nodeMapImage = PhotoImage(file=imageLocation)
			self.nodeMap.image = self.nodeMapImage

			# rescale image to fit canvas and center it
			if imageScaling:
				canvasw = self.nodeMapWidth
				canvash = self.nodeMapHeight
				imagew = self.nodeMap.image.width()
				imageh = self.nodeMap.image.height()
				imageaspect = float(imageh)/float(imagew) # width * factor gives the height

				imgw = imagew
				imgh = imageh
				pw = 0
				ph = 0

				# get the size of the image and scale to fit window if window bigger then image

				if canvasw < imagew and canvash < imageh:
					imgw = imagew
					imgh = imageh

				if canvasw > imagew and canvash > imageh:
					imgw = canvasw
					imgh = int(canvasw * imageaspect)
					ph = (canvash - imgh)/2
					pw = 0
					if imgh > canvash:
						imgh = canvash
						imgw = int(canvash / imageaspect)
						pw = (canvasw - imgw)/2
						ph = 0

				if canvasw > imagew and canvash < imageh:
					imgw = canvasw
					imgh = int(canvasw * imageaspect)
					ph = (canvash - imgh)/2
					pw = 0
					if imgh > canvash:
						imgw = imagew
						imgh = imageh
						pw = (canvasw - imgw)/2
						ph = 0

				if canvasw < imagew and canvash > imageh:
					imgw = canvasw
					imgh = int(canvasw * imageaspect)
					ph = (canvash - imgh)/2
					pw = 0
					if imgh < canvash:
						imgw = imagew
						imgh = imageh
						pw = 0
						ph = (canvash - imgh)/2

				size = (int(imgw),int(imgh))

				# zoom and place image on map
				self.nodeMapImage = Image.open(imageLocation)
				self.nodeMapImageResized = self.nodeMapImage.resize(size,Image.ANTIALIAS)
				img = ImageTk.PhotoImage(self.nodeMapImageResized)
				self.nodeMap.image = img
				self.nodeMap.create_image(pw, ph, image=img, anchor=NW, tags="bg")
			else:
				self.nodeMapImage = Image.open(imageLocation)
				img = ImageTk.PhotoImage(self.nodeMapImage)
				self.nodeMap.image = img
				self.nodeMap.create_image(0,0, image=img, anchor=NW, tags="bg")


	def updateMap(self):
		"""update the Network Map"""
		# clear the map (prevent nasty memoryhogging)
		self.nodeMap.delete(ALL)

		#reload background image
		self.setMapImage()

		# load/draw the nodes on the map

		self.nodecount = 0 # for the ones without coordinates

		for node in settings.nodes:

			# set position of node on map
			if node[12]=="0" or node[12]=="":
				posX = 30
				posY = 30*self.nodecount+30
				self.nodecount = self.nodecount + 1

			elif not node[12]=="0" or node[12]=="":
				hw = node[12].split("x")
				if hw[0] and hw[1]:
					posX = hw[0]
					posY = hw[1]

			# set size of the nodes circles
			nodew = settings.mapperNodeSize
			nodeh = settings.mapperNodeSize
			borderw = 2
			posX2 = int(posX) + nodew
			posY2 = int(posY) + nodeh

			# save the nodes coordinates
			node[12] = "" + str(posX) + "x" + str(posY) + ""

			# set status color
			if settings.monitorRunning:
				if node[5]=="Online":
					status = "#" + settings.mapperNodeStatusColorOnline + ""
					textstatus = "black"
				if node[5]=="Offline":
					status = "#" + settings.mapperNodeStatusColorOffline + ""
					textstatus = "white"
				if node[5]=="Awaiting":
					status = "#" + settings.mapperNodeStatusColorAwaiting + ""
					textstatus = "black"
			else:
				status = "white"
				textstatus = "black"
			if node[4]==False:
				status = "#" + settings.mapperNodeStatusColorNoStatus + ""

			# draw the circle on the canvas
			self.nodeMap.create_oval(posX,posY,posX2,posY2, fill=status,
				outline="#222222", width=borderw,tags=("top", node[0],"node"))

			# put a namebox and text next to node
			if settings.mapperShowLabels:
				nameX = int(posX) + nodew + 3
				nameY = int(posY) + 1
				nodenametext = self.nodeMap.create_text(nameX,nameY, text=node[0],
					anchor=NW, fill=textstatus, tags=("top", "nodetext", "node"))
				nameLocation = self.nodeMap.bbox(nodenametext)
				self.nodeMap.create_rectangle(nameLocation[0]-nodew/2, nameLocation[1]-1,
					nameLocation[2]+2, 	nameLocation[3], width=1, fill=status, tags=("middle","node"))

			# draw a line to it(s) parent(s)
			if settings.mapperDrawLines:
				linetype = 0
				if node[13]:
					linetype = (9,7)
				for ip in node[10]:
					if not ip==node[6] or ip==node[7] or ip==node[8] or ip=="":
						x1 = int(posX) + nodew/2
						y1 = int(posY) + nodeh/2
						xy = [posX,posY]

						for parents in settings.nodes:
							for parent in parents[6]:
								if parent==ip:
									if not parents[12]=="":
										xy = parents[12].split("x")
										x2 = int(xy[0])+nodew/2
										y2 = int(xy[1])+nodeh/2
									if linetype==0:
										#self.nodeMap.create_line(x1,y1,x2,y2, fill="white",
											#width=6, capstyle=ROUND, smooth=True, tags=("subline"))
										self.nodeMap.create_line(x1,y1,x2,y2, fill="black",
											width=3, tags=("line"))
									elif linetype:

										self.nodeMap.create_line(x1,y1,x2,y2, fill="white",
											width=3, tags=("subline"))
										self.nodeMap.create_line(x1,y1,x2,y2, fill="black",
											width=3, tags=("line"),smooth=True, dash=linetype)
					else:
						pass # don't draw line

			# put nodes on top of lines
			self.nodeMap.tag_lower("bg")
			self.nodeMap.tag_raise("line")
			self.nodeMap.tag_raise("middle")
			self.nodeMap.tag_raise("top")

	def resizeMap(self, event):
		"""if a window/canvas resize event happens, scale the shit out of everything"""

		# get the scaling factor
		#wscale = float(event.width)/float(self.nodeMapWidth)
		#hscale = float(event.height)/float(self.nodeMapHeight)

		# give the canvas it's new height and width
		self.nodeMapWidth = event.width
		self.nodeMapHeight = event.height
		self.nodeMap.config(width=self.nodeMapWidth, height=self.nodeMapHeight)

		# scale the image/map/buildingplans
		self.setMapImage()

		# rescale the rest - Needs some work maybe
		#self.nodeMap.scale(ALL, 0, 0, wscale, hscale)

		# reset layering
		self.nodeMap.tag_lower("bg")
		self.nodeMap.tag_raise("line")
		self.nodeMap.tag_raise("middle")
		self.nodeMap.tag_raise("top")

	def moveNode(self, event):
		"""on mouseclick move nodecircle"""
		canvas = event.widget
		x = canvas.canvasx(event.x)
		y = canvas.canvasy(event.y)
		itemCoord = canvas.coords(CURRENT)
		try:
			offsetX = x - (itemCoord[0] + settings.mapperNodeSize/2)
			offsetY = y - (itemCoord[1] + settings.mapperNodeSize/2)
			for tag in canvas.gettags(CURRENT):
				for node in settings.nodes:
					if tag==node[0]:
						canvas.move(CURRENT, offsetX, offsetY)
						# save coordinates to settings
						node[12] = str(int(x-offsetX)-settings.mapperNodeSize/2) + "x" + str(int(y-offsetY)-settings.mapperNodeSize/2)
		except:
			pass

	def updateMapAfterMove(self, event):
		self.updateMap()

	def startMonitor(self):
		self.monitorButton.config(text="Stop\nMonitor", command=lambda: self.stopMonitor())
		monitor.start()
		self.monitorUpdateMap()

	def stopMonitor(self):
		self.monitorButton.config(text="Start\nMonitor", command=lambda: self.startMonitor())
		monitor.stop()
		self.updateMap()
		self.updateNodelist()

	def monitorUpdateMap(self):
		if settings.monitorRunning:
			self.updateNodelist()
			self.updateMap()
			root.after(settings.monitorUpdateInterval, self.monitorUpdateMap)


	# Scanner Window - work in progres

	def scannerWindow(self, event):
		self.scannerGui = Toplevel()
		self.scannerGui.title("Lan Map - Scanner")
		self.scannerGui.geometry("700x500")

		self.scannerGuiOptionsFrame = Frame(self.scannerGui, relief=RAISED)
		self.scannerGuiOptionsFrame.pack(side=LEFT, fill=Y, padx=5, pady=5)
		self.scannerGuiResultsFrame = Frame(self.scannerGui, relief=SUNKEN)
		self.scannerGuiResultsFrame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

		self.scannerGuiStartScanButton = Button(self.scannerGuiOptionsFrame, text="Start Scan")
		self.scannerGuiStartScanButton.pack(side=TOP, fill=X, expand=True)

		self.scannerGuiFillFrame = Frame(self.scannerGuiOptionsFrame)
		self.scannerGuiFillFrame.pack(side=BOTTOM, fill=Y, expand=True)

		self.scannerGuiResultsListbox = Listbox(self.scannerGuiResultsFrame)
		self.scannerGuiResultsListbox.pack(side=TOP, fill=BOTH)


	# EditNodes Window - work in progres

	def editNodesWindow(self, event, openNode=0):
		self.editNodesGui = Toplevel()
		self.editNodesGui.title("Lan Map - Edit Nodes in Network")
		self.editNodesGui.geometry("300x500")

		# dropdown selectbox
		self.editNodesIdName = Label(self.editNodesGui, text="Select Node:")
		self.editNodesIdName.pack(side=TOP, fill=X, anchor=N, padx=5, pady=5, expand=True)

		self.editNodesSelection = []
		count = 1
		for node in settings.nodes:
			name = node[0]
			ip = node[6][0]
			option = str(ip) + " - " + str(name) + ""
			self.editNodesSelection.append(option,)
			count = count + 1
		self.editNodesOptions = tuple(self.editNodesSelection)
		self.editNodesId = StringVar(self.editNodesGui)
		self.editNodesId.set(self.editNodesOptions[0])
		self.editNodesNodeSelector = apply(OptionMenu, (self.editNodesGui, self.editNodesId) + self.editNodesOptions)
		self.editNodesNodeSelector.pack(side=TOP, fill=X, anchor=N, padx=5, pady=5, expand=True)

		# selected node
		self.editNodesNodeFrame = Frame(self.editNodesGui, height=450, relief=SUNKEN)
		self.editNodesNodeFrame.pack(side=TOP, fill=X, anchor=N, padx=5, pady=5, expand=True)

	# Select an backgroud image for the map

	def loadBgImage(self):
		openf = filedialog.askopenfilename(defaultextension=".gif",
		filetypes=[('GIF files', '.gif'), ('all files', '.*')],
		title="Load Background map image")
		if openf:
			settings.mapperImage = openf
			self.updateMap()

	def clearBgImage(self):
		settings.mapperImage = ""
		self.updateMap()

	# Settings Window

	# Log Window

	def logWindow(self, event):
		self.loggui = Toplevel()
		self.loggui.title("Lan Map - Log")

		self.logtextFrame = Frame(self.loggui)
		self.logtextFrame.pack(side=TOP, fill=BOTH, expand=True)
		self.logCommandFrame = Frame(self.loggui, height=20)
		self.logCommandFrame.pack(side=BOTTOM, fill=X)

		self.logtext = Text(self.logtextFrame)
		self.logtext.pack(side=LEFT, fill=BOTH)
		self.logtextScrollbar = Scrollbar(self.logtextFrame, orient=VERTICAL)
		self.logtextScrollbar.pack(side=LEFT, fill=Y)
		self.logtextScrollbar.configure(command=self.logtext.yview,)
		self.logtext.configure(yscrollcommand=self.logtextScrollbar.set)

		self.logClearButton = Button(self.logCommandFrame, text="Clear Log")
		self.logClearButton.pack(side=LEFT, fill=X, expand=True)
		self.logSaveButton = Button(self.logCommandFrame, text="Save Log")
		self.logSaveButton.pack(side=LEFT, fill=X, expand=True)
		self.logCloseButton = Button(self.logCommandFrame, text="Close Log",
			command=self.loggui.destroy)
		self.logCloseButton.pack(side=LEFT, fill=X, expand=True)

		# fill the log with the log
		for item in settings.log:
			self.logtext.insert(END, item + "\n")
		self.logtext.config(state=DISABLED)

# Main Program

# save config and quit
def saveAndQuit():
	settings.save()
	root.destroy()

# main instance
root = Tk()

log.add("Lan Map Started")
settings.load()

# save config if window is closed
root.protocol("WM_DELETE_WINDOW", saveAndQuit)

root.geometry(settings.guiWindowSize)
#root.attributes('-zoomed', True) #start with maximized gui
app = mainWindow(root)

root.mainloop()


