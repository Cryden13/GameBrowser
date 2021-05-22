from PIL.ImageTk import PhotoImage
from os import startfile

from tkinter import (
    LabelFrame as LFrame,
    Canvas,
    Text,
    Event,
    Toplevel
)
from PIL import (
    Image,
    ImageDraw,
    ImageFont
)
from changecolor import (
    darken,
    lighten
)

try:
    from ..constants import *
except ImportError:
    from subprocess import run
    from pathlib import Path
    pth = Path(__file__).parents[2]
    run(['py', '-m', pth.name, 'console'], cwd=pth.parent)
    raise SystemExit


class LineItem:
    lineitem: Canvas
    bg: str
    fol: Path
    info: dict[str, U[str, Path, dict[str, Path]]]
    title: str
    children: list[U[Canvas, LFrame, Text]]
    col: int
    row: int
    height: int
    toolFrm: LFrame

    def __init__(self, lineItem: Canvas, bg: str, gFol: Path,
                 data: GAMEDATA_TYPE, startFunc: C, editFunc: C):
        self.lineitem = lineItem
        self.bg = bg
        self.fol = gFol
        self.info = data['Info'].copy()
        cats = data['Categories'].copy()
        tags = data['Tags'].copy()
        self.title = self.info['Title']
        self.children = list()
        self.col = 1
        self.row = 0
        self.height = 0

        self.fillTools(startFunc, editFunc)
        self.fillText(cats, tags)

    def fillTools(self, startFunc: C, editFunc: C) -> None:
        self.toolFrm = LFrame(master=self.lineitem,
                              font=FONT_SM,
                              text='Tools',
                              background=self.bg)
        self.toolFrm.grid(column=0,
                          row=0,
                          sticky='ns')
        self.toolFrm.columnconfigure(0, weight=1)

        # play btn
        def startGame(event: "Event"): startFunc(event=event,
                                                 gFolder=self.fol,
                                                 gTitle=self.title,
                                                 gPath=self.info['Program Path'])
        playBtn = self.canvasButton(color=COLOR_PLAY,
                                    txt='▶',
                                    cmd=startGame,
                                    fnt=FONT_TTL)
        # link btn
        def openLink(_): startfile(self.info['URL'])
        linkBtn = self.canvasButton(color=COLOR_LINK,
                                    txt='www',
                                    cmd=openLink)
        # edit btn
        def editGame(_): editFunc(gFol=self.fol)
        editBtn = self.canvasButton(color=COLOR_EDIT,
                                    txt='Edit',
                                    cmd=editGame)
        self.children += [self.toolFrm, playBtn, linkBtn, editBtn]

    def canvasButton(self, color: str, txt: str, cmd: C[[Event], None], fnt: str = FONT_SM) -> Canvas:
        cnvBtn = Canvas(master=self.toolFrm,
                        width=BTN_SIZE,
                        height=BTN_SIZE,
                        bg=self.bg)
        cnvBtn.grid(column=0,
                    row=self.row,
                    sticky='ns',
                    pady=2)
        cir = cnvBtn.create_oval(0, 0,
                                 (BTN_SIZE - 1),
                                 (BTN_SIZE - 1),
                                 fill=color)
        cnvBtn.create_text((BTN_SIZE // 2),
                           (BTN_SIZE // 2 - 2),
                           text=txt,
                           font=fnt)
        hlcolor: str = darken(color=self.toolFrm.winfo_rgb(color),
                              inputtype='RGB16')
        cnvBtn.bind('<ButtonRelease-1>', cmd)

        def onEnter(_): cnvBtn.itemconfig(cir, fill=hlcolor)
        cnvBtn.bind('<Enter>', onEnter)

        def onLeave(_): cnvBtn.itemconfig(cir, fill=color)
        cnvBtn.bind('<Leave>', onLeave)
        self.row += 1
        return cnvBtn

    def fillText(self, cats: dict[str, U[str, int]], tags: dict[str, U[str, int]]) -> None:
        # version
        complete = cats.pop('Completed')
        abandoned = cats.pop('Abandoned')
        clr = 'white' if complete else 'darkred' if abandoned else 'SystemButtonText'
        self.textbox(title="Version",
                     wd=TEXTBOX_WD['version'],
                     txt=self.info['Version'],
                     txtclr=clr)
        # title
        if cats.pop('Favorite'):
            clr = ''.join(f'{n >> 8:02x}' for n in
                          self.lineitem.winfo_rgb('gold'))
        else:
            clr = lighten(color=self.lineitem.winfo_rgb('SystemButtonText'),
                          percent=20,
                          inputtype='RGB16')[1:]
        self.titleImg(txtclr=f'#{clr}ff')
        # categories
        curCats = [f'{c}: {v}' for c, v in cats.items()]
        self.textbox(title="Categories",
                     wd=TEXTBOX_WD['categories'],
                     txt='\n'.join(curCats))
        # tags
        curTags = [t for t, v in tags.items() if v]
        self.textbox(title="Tags",
                     wd=TEXTBOX_WD['tags'],
                     txt=', '.join(curTags))
        # description
        self.textbox(title="Description",
                     wd=INFO_ENT['Description'],
                     txt=self.info['Description'])

    def textbox(self, title: str, wd: int, txt: str, txtclr: str = 'SystemButtonText') -> None:
        self.col += 1
        lf = LFrame(master=self.lineitem,
                    font=FONT_SM,
                    text=title,
                    background=self.bg)
        lf.grid(column=self.col,
                row=0,
                sticky='ns')
        t = Text(master=lf,
                 width=wd,
                 height=TEXTBOX_HT,
                 wrap='word',
                 padx=(PAD // 2),
                 pady=(PAD // 2),
                 bg=self.bg,
                 fg=txtclr,
                 undo=True,
                 maxundo=-1)
        t.grid()
        t.insert('end', txt)
        if not self.height:
            self.height = t.winfo_reqheight()
        t.config(state='disabled')
        self.children += [lf, t]

    def titleImg(self, txtclr: str) -> None:
        def zoom(_):
            tw = Toplevel(lf)
            tw.overrideredirect(1)
            xpos, ypos = lf.winfo_rootx(), lf.winfo_rooty()
            if xpos + img.width > SCREEN_WD:
                xpos = SCREEN_WD - img.width
            if ypos + img.height > SCREEN_HT:
                ypos = SCREEN_HT - img.height
            tw.geometry(f'{img.width}x{img.height}'
                        f'+{xpos}'
                        f'+{ypos}')
            tcnv = Canvas(master=tw,
                          bd=1,
                          relief='groove')
            tcnv.pack(fill='both', expand=True)
            imglg = PhotoImage(img)
            tcnv.create_image(0, 0, anchor='nw', image=imglg)
            tcnv.image = imglg

            tw.focus_set()
            for seq in 'Leave Escape ButtonRelease-1'.split():
                tw.bind(sequence=f'<{seq}>',
                        func=lambda _: tw.destroy())

        # create frm
        lf = LFrame(master=self.lineitem,
                    font=FONT_SM,
                    text='Title',
                    background=self.bg)
        lf.grid(column=1,
                row=0,
                sticky='ns')
        # create cnv
        wd = IMG_SIZE
        ht = self.height
        cnv = Canvas(master=lf,
                     bg=self.bg,
                     width=wd,
                     height=ht,
                     bd=1,
                     relief='groove')
        cnv.pack()
        # format title
        lines = list()
        line = list()
        for word in self.title.split():
            txt = ' '.join(line)
            new = f"{txt} {word}" if line else word
            if FONT_IMG.getsize(new)[0] > (IMG_SIZE - PAD):
                lines.append(txt)
                line.clear()
            line.append(word)
        if line:
            lines.append(' '.join(line))
        title = '\n'.join(lines)
        # get image
        imgpth = PATH_IMGS.joinpath(self.info.get('Image') or 'default.png')
        if imgpth.exists():
            img = Image.open(imgpth).convert('RGBA')
            img.thumbnail((1920, 1080))
        else:
            fntpth = Path(f'C:\\Windows\\Fonts\\{FONT_TTL[0]}.ttf')
            efnt = ImageFont.truetype(font=str(fntpth if fntpth.exists()
                                               else fntpth.with_stem('Gauge-Heavy')),
                                      size=72)
            img = Image.new('RGBA', (300, 300), (255, 0, 0, 255))
            err = ImageDraw.Draw(img)
            err.multiline_text(xy=(150, 150),
                               text='Image\nNot\nFound',
                               fill=(255, 255, 255, 255),
                               font=efnt,
                               anchor='mm',
                               align='center',
                               stroke_width=2,
                               stroke_fill=(0, 0, 0, 255))
        # create thumbnail
        tn_raw = img.copy()
        w, h = tn_raw.width, tn_raw.height
        size = (w, ht) if (w / h) > (wd / ht) else (wd, h)
        tn_raw.thumbnail(size)
        x, y = (tn_raw.width/2), (tn_raw.height/2)
        crop = (x-wd/2), (y-ht/2), (x+wd/2), (y+ht/2)
        thumb = tn_raw.crop(crop)
        # create thumb text
        tn_txt = Image.new('RGBA', thumb.size, f'{self.bg}{IMG_FADE}')
        d = ImageDraw.Draw(tn_txt)
        d.multiline_text(xy=(PAD / 2, 0),
                         text=title,
                         fill=txtclr,
                         font=FONT_IMG,
                         stroke_width=1,
                         stroke_fill=(0, 0, 0, 255))
        thumb.alpha_composite(tn_txt)

        imgsm = PhotoImage(thumb)
        cnv.create_image(0, 0, anchor='nw', image=imgsm)
        cnv.image = imgsm

        cnv.bind(sequence='<ButtonRelease-1>',
                 func=zoom)

        self.children += [lf, cnv]

    @classmethod
    def Fill(cls, lineItem: Canvas, bg: str, gFol: Path, data: GAMEDATA_TYPE,
             startFunc: C, editFunc: C) -> list[U[Canvas, LFrame, Text]]:
        line = cls(lineItem, bg, gFol, data, startFunc, editFunc)
        return line.children
