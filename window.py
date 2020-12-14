from editlist import *


class GUI(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.configure(padx=PAD*2)
		self.scrWd, self.scrHt = self.winfo_screenwidth(), self.winfo_screenheight()
		self.geometry('{}x{}+{:.0f}+{:.0f}'.format(WIDTH, HEIGHT, (self.scrWd-WIDTH)/2, (self.scrHt-HEIGHT)/2))
		self.title('Game List')

		(s := Style()).configure('.', font=FONT_MD)
		s.configure('TEntry', width=50)
		self.defBG = self.cget('bg')
		self.litBG = changecolor.lighten('RGB', self.winfo_rgb(self.defBG), 5, 'HEX', 16)

	def start_main(self, gameClass):
		self.gameClass = gameClass
		self.masterList = self.gameClass.masterList
		self.createSearch()
		self.createBrowse()

	def createSearch(self):
		self.searchFrm = LFrame(self, font=FONT_LG, text="Search", padx=PAD)
		self.searchFrm.place(anchor=N, relx=0.5, rely=0, relwidth=0.6, relheight=0.3)
		[self.searchFrm.rowconfigure(n, weight=2) for n in [0,1]]
		self.searchFrm.columnconfigure(0, weight=1)
		self.createCatFrm()
		self.createTagFrm()
		(btnFrm := Frame(self.searchFrm)).grid(row=2, column=0, pady=PAD)
		[btnFrm.columnconfigure(n, weight=1) for n in range(2)]
		Button(btnFrm, text="Clear", command=self.clearSearch).grid(row=0, column=0, padx=50)
		Button(btnFrm, text="Go!", command=self.searchBrowse).grid(row=0, column=1, padx=50)

	def createCatFrm(self):
		(catFrm := LFrame(self.searchFrm, font=FONT_MD, text="Categories", padx=PAD)).grid(row=0, column=0, sticky=EW)
		curRow,curCol,self.catToggles,self.catLists = 0,0,{i: IntVar() for i in CAT_TOG},{}
		for c,v in self.catToggles.items():
			Checkbutton(catFrm, text=c, variable=v).grid(row=curRow, column=curCol, sticky=W, padx=PAD/2)
			curRow,curCol = [curRow+1,0] if curCol == 5 else [curRow,curCol+1]
		for c,v in CAT_LST.items():
			v = ['Any', *v]
			(lf := LFrame(catFrm, font=FONT_SM, text=c)).grid(row=curRow, column=curCol, padx=PAD/2)
			(cb := Combobox(lf, values=v, width=13)).grid(sticky=W)
			cb.current(0)
			self.catLists.update({c: cb})
			curRow,curCol = [curRow+1,0] if curCol == 5 else [curRow,curCol+1]
		[catFrm.columnconfigure(n, minsize=GRIDMIN) for n in range(6)]

	def createTagFrm(self):
		(tagFrm := LFrame(self.searchFrm, font=FONT_MD, text="Tags", padx=PAD)).grid(row=1, column=0, sticky=EW)
		curRow,curCol,self.tagToggles,self.tagLists = 0,0,{i: IntVar() for i in TAG_TOG},{}
		for c,v in self.tagToggles.items():
			Checkbutton(tagFrm, text=c, variable=v).grid(row=curRow, column=curCol, sticky=W, padx=PAD/2)
			curRow,curCol = [curRow+1,0] if curCol == 5 else [curRow,curCol+1]
		for c,v in TAG_LST.items():
			v = ['Any', *v]
			(lf := LFrame(tagFrm, font=FONT_SM, text=c)).grid(row=curRow, column=curCol, padx=PAD/2)
			(cb := Combobox(lf, values=v, width=13)).grid(sticky=W)
			cb.current(0)
			self.tagLists.update({c: cb})
			curRow,curCol = [curRow+1,0] if curCol == 5 else [curRow,curCol+1]
		[tagFrm.columnconfigure(n, minsize=GRIDMIN) for n in range(6)]

	def createBrowse(self):

		def scanGames():
			if mbox.askyesno("Check for updates?","Would you like to check for\nnew or altered game folders?"):
				self.changed = False
				self.gameClass.checkGames()
				if self.changed:
					self.searchBrowse()

		Button(self, text="Scan Folder", command=scanGames).place(anchor=SW, relx=0, x=PAD, rely=0.3)

		self.browseFrm = ScrolledFrame(self, scrollbars='E', dohide=False, padding=[PAD, PAD, PAD, PAD], relief=SUNKEN)
		self.browseFrm.place(anchor=N, relx=0.5, rely=0.3, y=PAD, relwidth=1, relheight=0.7, height=-PAD*2)

		self.gameList = {**self.masterList}
		self.redrawList()

	def redrawList(self):
		[w.destroy() for w in self.browseFrm.winfo_children()]
		for i, (name, data) in enumerate(self.gameList.items()):
			if (i % 2) == 0:
				BG = self.defBG
			else:
				BG = self.litBG
			info = data['Info']
			cats = data['Categories']
			tags = data['Tags']

			lineItem = Canvas(self.browseFrm, background=BG)
			lineItem.grid(row=i, column=0, padx=PAD/2, pady=PAD/2)
			(f := LFrame(lineItem, font=FONT_SM, text='Tools', background=BG)).grid(row=0, column=(curCol:=0), sticky=NS)
			f.columnconfigure(0, weight=1)
			# play btn
			self.canvasButton(f, bg=BG, color='#87ffb9', fnt=FONT_LG, txt='▶', cmd=(lambda e,n=name,p=info['Program Path']: self.startGame(e,n,p)), row=0, col=0)
			# link btn
			self.canvasButton(f, bg=BG, color='#9cd4ff', txt='www', cmd=(lambda e,u=info['URL']: self.checkForUpdate(u)), row=1, col=0)
			# edit btn
			self.canvasButton(f, bg=BG, color='#e3b668', txt='Edit', cmd=(lambda e,n=name: self.editGame(n)), row=2, col=0)
			# title
			self.textbox(lineItem, ttl="Title", h=5, w=20, bg=BG, txt=info['Title'], row=0, col=(curCol:=curCol+1))
			# version
			self.textbox(lineItem, ttl="Version", h=5, w=8, bg=BG, txt=info['Version'], row=0, col=(curCol:=curCol+1))
			# categories
			curCats = [t for t,v in cats.items() if v and t not in CAT_LST] + ['{}: {}'.format(n, cats['{}'.format(n)]) for n in CAT_LST]
			self.textbox(lineItem, ttl="Categories", h=5, w=15, bg=BG, txt='\n'.join(curCats), row=0, col=(curCol:=curCol+1))
			# tags
			curTags = [t for t,v in tags.items() if v and t not in TAG_LST] + ['{} {}'.format(tags['{}'.format(n)], n) for n in TAG_LST]
			self.textbox(lineItem, ttl="Tags", h=5, w=20, bg=BG, txt=', '.join(curTags), row=0, col=(curCol:=curCol+1))
			# description
			self.textbox(lineItem, ttl="Description", h=5, w=75, bg=BG, txt=info['Description'], row=0, col=(curCol:=curCol+1))

		self.browseFrm.redraw()

	def checkForUpdate(self, curUrl):
		if 'f95zone' in curUrl and curUrl == req_url().head(curUrl, allow_redirects=True).url and not mbox.askyesno("No update", "There has been no update according to the url. Open anyway?"):
			return
		os_startfile(curUrl)

	def canvasButton(self, p, bg, color, txt, cmd, row, col, fnt=FONT_SM):
		(cnvBtn := Canvas(p, width=BTNSIZE, height=BTNSIZE, background=bg)).grid(row=row, column=col, sticky=NS, pady=2)
		cir = cnvBtn.create_oval(0, 0, BTNSIZE-1, BTNSIZE-1, fill=color)
		cnvBtn.create_text(BTNSIZE/2, BTNSIZE/2, text=txt, font=fnt)
		hlcolor = changecolor.darken('HEX', color)
		cnvBtn.bind('<ButtonRelease-1>', cmd)
		cnvBtn.bind('<Enter>', lambda e,b=cnvBtn,c=cir,clr=hlcolor: b.itemconfig(c, fill=clr))
		cnvBtn.bind('<Leave>', lambda e,b=cnvBtn,c=cir: b.itemconfig(c, fill=color))

	def textbox(self, p, ttl, h, w, bg, txt, row, col):
		(lf := LFrame(p, font=FONT_SM, text=ttl, background=bg)).grid(row=row, column=col, sticky=NS)
		(t := Text(lf, font=FONT_MD, height=h, width=w, wrap=WORD, padx=3, pady=3, background=bg)).grid()
		t.insert(END, txt)
		t.config(state=DISABLED)

	def startGame(self, event, gameName, gamePath):
		try:
			if '||' in gamePath:
				tw = Toplevel(self, padx=PAD, pady=PAD)
				tw.overrideredirect(1)
				tw.geometry('+{}+{}'.format(event.x_root, event.y_root))
				tw.focus_set()
				tw.bind('<FocusOut>', lambda e: tw.destroy())
				[Button(tw, text=g, command=lambda game=os_path.join(gameName,g): [tw.destroy(), os_startfile(game)]).pack() for g in gamePath.split('||')]
			else:
				if os_path.isdir(gameName):
					os_startfile(os_path.join(gameName, gamePath))
				else:
					os_startfile(gamePath)
		except Exception:
			if mbox.askyesno("Error", "Couldn't start '{}'.\nWould you like to change the executable path?"):
				self.editGame(gameName)

	def editGame(self, game):
		self.changed = False
		editWin = EditGames(self, self.gameClass, [game])
		try:
			self.wait_window(editWin)
		except Exception:
			pass
		if self.changed:
			self.searchBrowse()

	def searchBrowse(self):
		self.gameClass.alphabetize()
		sCats = {k:0 for k in CAT_LST}
		sCats.update({k:v.get() for k,v in {**self.catToggles, **self.catLists}.items() if v.get() != 'Any'})
		sTags = {k:0 for k in TAG_LST}
		sTags.update({k:v.get() for k,v in {**self.tagToggles, **self.tagLists}.items() if v.get() != 'Any'})
		listRemove = []
		for cat,val in sCats.items():
			if val:
				for game,data in self.masterList.items():
					if data['Categories'][cat] != val:
						listRemove.append(game)
		for tag,val in sTags.items():
			if val:
				for game,data in self.masterList.items():
					if data['Tags'][tag] != val:
						listRemove.append(game)
		self.gameList = {game:data for game,data in self.gameClass.masterList.items() if game not in listRemove}
		self.redrawList()

	def clearSearch(self):
		[v.set(0) for k,v in {**self.catToggles, **self.tagToggles}.items()]
		[v.current(0) for k,v in {**self.catLists, **self.tagLists}.items()]
		self.gameList = self.masterList
		self.redrawList()
