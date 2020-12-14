from constants import *


class EditGames(Toplevel):
	def __init__(self, root, gameClass, games, showSkip=False):
		Toplevel.__init__(self, root, padx=PAD*2, pady=PAD)
		self.root, self.gameClass, self.showSkip = root, gameClass, showSkip
		self.title("Edit Games")
		self.transient(root)
		self.protocol("WM_DELETE_WINDOW", lambda: self.closeWindow(True))
		self.geometry(root.geometry())
		self.geometry('{:.0f}x{:.0f}'.format(WIDTH*0.7, HEIGHT*0.7))
		self.grab_set()

		self.curProcess = IntVar()
		for g in games:
			self.curProcess.set(1)
			self.game = g
			self.gameFolPath = os_path.join(GAMEDIR, self.game)
			self.createGUI()
			if self.game in self.gameClass.masterList:
				self.insertInfo()
			self.wait_variable(self.curProcess)
			if self.curProcess.get() == 0:
				break
		self.closeWindow(True)

	def closeWindow(self, close=False):
		if close:
			self.curProcess.set(0)
			self.root.focus_force()
			self.destroy()
		else:
			self.cnvs.destroy()
			self.curProcess.set(2)

	def createGUI(self):
		self.cnvs = Canvas(self)
		self.cnvs.place(relx=0, rely=0, relwidth=1, relheight=1)
		[self.cnvs.rowconfigure(n, weight=1) for n in [1,2,3]]
		self.cnvs.columnconfigure(0, weight=1)
		# create header
		(pathFrm := LFrame(self.cnvs, font=FONT_MD, text="Folder Name", padx=PAD)).grid(row=0, column=0, sticky=EW)
		self.pathLbl = Label(pathFrm, font=FONT_LG, text=self.game)
		self.pathLbl.grid(row=0, column=0, sticky=NSEW)
		# create body
		self.createInfoFrm()
		self.createCatFrm()
		self.createTagFrm()
		# create footer
		(btnFrm := LFrame(self.cnvs, pady=PAD)).grid(row=4, column=0, columnspan=2, sticky=NSEW, pady=PAD)
		[btnFrm.columnconfigure(n, weight=1) for n in [0,1,2]]
		Button(btnFrm, text="Cancel", command=lambda: self.closeWindow(True)).grid(row=0, column=(curCol:=0), padx=25)
		if self.showSkip:
			Button(btnFrm, text="Skip", command=self.closeWindow).grid(row=0, column=(curCol:=curCol+1), padx=25)
		Button(btnFrm, text="Save", command=self.submit).grid(row=0, column=curCol+1, padx=25)

	def createInfoFrm(self):

		def searchForExe(searchMe):
			if os_path.splitext(searchMe)[1] in FILETYPES:
				return os_path.relpath(searchMe)
			elif os_path.isfile(searchMe):
				return ''
			elif (p:=[os_path.relpath(os_path.join(searchMe, f)) for e in FILETYPES for f in os_listdir(searchMe) if os_path.splitext(f)[1] == e]):
				return p[0]
			return ''
		def browseFolders():
			if (p:=filedialog.askopenfilename(initialdir=os_path.join(GAMEDIR, self.game))) and (path := os_path.relpath(p)):
				ins = '||{}'.format(path) if self.infoEnts['Program Path'].get() else path
				self.infoEnts['Program Path'].insert(END, ins)
			self.deiconify()

		(infoFrm := LFrame(self.cnvs, font=FONT_MD, text="Info", padx=PAD)).grid(row=1, column=0, sticky=NSEW)
		infoFrm.columnconfigure(2, weight=1)
		[Label(infoFrm, text=i).grid(row=r, column=0) for r,i in enumerate(INFO_ENT)]
		Button(infoFrm, text='f95zone lookup', command=self.getInfoF95).grid(row=INFO_ENT.index('URL'), column=2)
		Button(infoFrm, text='Open URL', command=lambda: os_startfile(self.infoEnts['URL'].get())).grid(row=INFO_ENT.index('URL'), column=3)
		# add entries
		self.infoEnts = {i: Entry(infoFrm, width=85) for i in INFO_ENT}
		[e.grid(row=r, column=1) for r,(i,e) in enumerate(self.infoEnts.items())]
		if self.game not in self.gameClass.masterList:
			# insert data
			g = re_sub(r'([a-z])([A-Z])', r'\1 \2', self.game.replace("_", " "))
			self.infoEnts['Title'].insert(0, g)
			# try to find exe
			if (exePath:=searchForExe(self.gameFolPath)):
				self.infoEnts['Program Path'].insert(0, exePath)
			elif mbox.askyesno("Multi-Work Series?", "Couldn't find an executable file. Does '{}' have a nested file structure or is it a multi-work series?".format(self.game), parent=self):
				if (exePaths := {searchForExe(os_path.join(self.gameFolPath, subFol)) for subFol in os_listdir(self.gameFolPath)} - {''}):
					self.infoEnts['Program Path'].insert(0, '||'.join(exePaths))
				else:
					mbox.showinfo("Failure", "Still couldn't find executables. Please add them manually, separated by semicolons", parent=self)
			self.deiconify()
		Button(infoFrm, text="Browse", command=browseFolders).grid(row=len(INFO_ENT), column=1, sticky=E)
		# add textbox
		Label(infoFrm, text="Description").grid(row=len(INFO_ENT)+1, column=0, sticky=W)
		self.infoDesc = Text(infoFrm, font=FONT_MD, height=5, width=75, wrap=WORD, padx=3, pady=3)
		self.infoDesc.grid(row=len(INFO_ENT)+1, column=1, columnspan=2, sticky=W)

	def createCatFrm(self):
		(catFrm := LFrame(self.cnvs, font=FONT_MD, text="Categories", padx=PAD)).grid(row=2, column=0, sticky=NSEW)
		curRow,curCol,self.catToggles,self.catLists = 0,0,{i: IntVar() for i in CAT_TOG},{}
		# add checkbuttons
		for c,v in self.catToggles.items():
			Checkbutton(catFrm, text=c, variable=v).grid(row=curRow, column=curCol, padx=PAD/2)
			curRow,curCol = [curRow+1,0] if curCol == 5 else [curRow,curCol+1]
		# add comboboxes
		for c,v in CAT_LST.items():
			(lf := LFrame(catFrm, font=FONT_SM, text=c)).grid(row=curRow, column=curCol, padx=PAD/2)
			(cb := Combobox(lf, values=v, width=13)).grid(sticky=W)
			# cb.current(0)
			self.catLists.update({c: cb})
			curRow,curCol = [curRow+1,0] if curCol == 5 else [curRow,curCol+1]
		[catFrm.columnconfigure(n, minsize=GRIDMIN) for n in range(6)]

	def createTagFrm(self):
		(tagFrm := LFrame(self.cnvs, font=FONT_MD, text="Tags", padx=PAD)).grid(row=3, column=0, sticky=NSEW)
		curRow,curCol,self.tagToggles,self.tagLists = 0,0,{i: IntVar() for i in TAG_TOG},{}
		# add checkbuttons
		for c,v in self.tagToggles.items():
			Checkbutton(tagFrm, text=c, variable=v).grid(row=curRow, column=curCol, sticky=W, padx=PAD/2)
			curRow,curCol = [curRow+1,0] if curCol == 5 else [curRow,curCol+1]
		# add comboboxes
		for c,v in TAG_LST.items():
			(lf := LFrame(tagFrm, font=FONT_SM, text=c)).grid(row=curRow, column=curCol, padx=PAD/2)
			(cb := Combobox(lf, values=v, width=13)).grid(sticky=W)
			# cb.current(0)
			self.tagLists.update({c: cb})
			curRow,curCol = [curRow+1,0] if curCol == 5 else [curRow,curCol+1]
		[tagFrm.columnconfigure(n, minsize=GRIDMIN) for n in range(6)]

	def getInfoF95(self):
		if not (url:=self.infoEnts['URL'].get()):
			if (url:=OLD_DATA.get(self.infoEnts['Title'].get())):
				self.infoEnts['URL'].insert(0, url)
			else:
				mbox.showerror("Error","No URL specified")
				return
		elif 'f95zone' not in url:
			mbox.showerror("Error","Only f95zone urls supported")
			return
		
		# set data paths
		title = '//div[@uix_component="MainContent"]//h1[@class="p-title-value"]//child::text()'
		tags = '//li[@class="groupedTags"]/a//child::text()'
		desc = '//article[@class="message-body js-selectToQuote"]/div[@class="bbWrapper"]/div'
		ver = '//article[@class="message-body js-selectToQuote"]//b[text()="Version"]/following-sibling::text()[1]'
		# get and format data
		page = html.fromstring(req_url().get(url).content)
		frmt = lambda data: ''.join(data).encode('ascii', 'ignore').decode().strip()

		# get catagory info
		if (rawHeader := frmt(page.xpath(title)).lower()) and (rawCatInfo := re_findall(r'(?<=\[).+?(?=\])', rawHeader)):
			self.catToggles['Completed'].set(1 if 'completed' in rawCatInfo else 0)
			[self.catLists['Format'].set(c) for c in CAT_LST['Format'] if c.lower() in rawCatInfo]

		# get tag info
		if (rawTags := (t:=set(page.xpath(tags))) - set(TAG_EQU) - set(CAT_EQU) | {v for k,v in {**TAG_EQU, **CAT_EQU}.items() if k in t}):
			# set toggle tags
			togTags = [t for t in TAG_TOG if t.lower() in rawTags]
			[self.tagToggles[t].set(1) for t in togTags]
			# set art category
			catTags = [t for t in CAT_LST['Art'] if t.lower in rawTags]
			[self.catLists['Art'].set(c) for c in catTags]
			# check for eroge
			if 'japanese game' in rawTags:
				self.catToggles['Eroge'].set(1)
			# get protagonist info
			rawProtag = {t.split(' ')[0] for t in rawTags if 'protagonist' in t}
			if (l:=len(rawProtag)) <= 1:
				protag = [p for p in TAG_LST['Protagonist'] if p.lower() in rawProtag][0] if l > 0 else 'Unknown'
			elif {'male','female'} == rawProtag or {'male','female','multiple'} == rawProtag:
				protag = 'Male/Female'
			else:
				protag = 'Multiple' if 'multiple' in rawProtag or len(rawProtag) > 1 else 'Unknown'
			self.tagLists['Protagonist'].set(protag)
		# set description & version
		desc = re_sub(r'\s*(\r+|\n+)\s*', r'\n', frmt(page.xpath(desc)[0].text_content()))
		self.infoDesc.insert(1.0, re_sub(r'(?s)Overview:|Spoiler:.+$', r'', desc).strip())
		self.infoEnts['Version'].insert(END, page.xpath(ver)[0][2:])
		# close info window
		os_system('nircmd stdbeep')

	def insertInfo(self):
		data = self.gameClass.masterList[self.game]
		# insert info
		[cb.insert(0, data['Info'][lbl]) for lbl,cb in self.infoEnts.items()]
		self.infoDesc.insert(1.0, data['Info']['Description'])
		# insert categories
		[cb.set(data['Categories'][lbl]) for lbl,cb in {**self.catToggles, **self.catLists}.items()]
		# insert tags
		[cb.set(data['Tags'][lbl]) for lbl,cb in {**self.tagToggles, **self.tagLists}.items()]

	def submit(self):
		self.gameClass.masterList.update({self.game: {
			'Info': {**{k:v.get().strip() for k,v in self.infoEnts.items()},
					**{'Description': self.infoDesc.get(1.0,'end-1c').strip()}},
			'Categories': {**{k:v.get() for k,v in self.catToggles.items()},
						  **{k:v.get().strip() for k,v in self.catLists.items()}},
			'Tags': {**{k:v.get() for k,v in self.tagToggles.items()},
					**{k:v.get().strip() for k,v in self.tagLists.items()}}}})
		self.gameClass.save()
		self.root.changed = True
		self.closeWindow()
