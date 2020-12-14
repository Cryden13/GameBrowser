from window import *


class GameLib:
	def __init__(self):
		self.masterList, gList = {}, os_path.join(TOPDIR, 'Game List.json')
		if os_path.exists(gList):
			with open(gList, 'r') as f:
				self.masterList = json.load(f)
			self.alphabetize()
			self.checkMissing()

	def checkMissing(self):
		if (missingGames := [g for g in self.masterList if g not in os_listdir()]):
			for game in missingGames:
				if (ans:=mbox.askyesnocancel("Missing reference", "'{}'\ncould not be found.\nPress 'yes' to delete the reference, 'no' to browse for the file, or 'cancel' to do nothing".format(game))):
					self.masterList.pop(game)
				elif ans == False and (exePath := os_path.relpath(filedialog.askopenfilename(title="Select the Executable for '{}'".format(game), initialdir=mainDir))):
					data = self.masterList.pop(game)
					data['Info']['Program Path'] = exePath
					self.masterList.update({exePath.split('\\')[0]: data})
					root.deiconify()
				else:
					continue
				self.save()

	def checkNewTags(self):
		if (missingInfo := [game for game,data in self.masterList.items() if data['Info']])
		for game,data in self.masterList.items():
			if (missingInfo := [g for g in data['']])

	def save(self):
		self.alphabetize()
		with open(os_path.join(TOPDIR, 'Game List.json'), 'w') as f:
			json.dump(self.masterList, f, indent=4)

	def alphabetize(self):
		titles = {data['Info']['Title']:name for name,data in self.masterList.items()}
		(alpha:=list(titles)).sort()
		self.masterList = {name: self.masterList[name] for name in [titles[title] for title in alpha]}

	def checkGames(self):
		if (newGames := [g for g in os_listdir() if (os_path.isdir(g) or os_path.splitext(g)[1] in FILETYPES) and g not in self.masterList and g != os_path.basename(TOPDIR)]):
			addNew = EditGames(root, self, newGames, True)
			try:
				root.wait_window(addNew)
			except Exception:
				pass
		else:
			mbox.showinfo("Notice","No new games were found!")
		return

os_chdir(GAMEDIR)
root = GUI()
gamelib = GameLib()
root.start_main(gamelib)
root.mainloop()
