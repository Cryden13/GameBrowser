# constants
from os import path as os_path, listdir as os_listdir, curdir as os_curdir, system as os_system, startfile as os_startfile, chdir as os_chdir
# editlist
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox as mbox, LabelFrame as LFrame
from time import sleep
from re import sub as re_sub, search as re_search, findall as re_findall
from requests import Session as req_url
from lxml import html
# window
import changecolor
from scrolledframe import ScrolledFrame
# main
import json


TOPDIR = os_path.dirname(__file__)
GAMEDIR = os_path.dirname(TOPDIR)
WIDTH = 1265
HEIGHT = 1000
BTNSIZE = 30
GRIDMIN = 85
PAD = 6
FILETYPES = ['.exe', '.jar', '.swf', '.html', '.url']

FONT_SM = 'Calibri 8'
FONT_MD = 'Calibri 12'
FONT_LG = 'Calibri 16'

INFO_ENT = ['Title', 'Version', 'URL', 'Program Path']

CAT_TOG = ['Completed', 'Eroge', 'Favorite']
CAT_LST = {'Status': ['New', 'Playing', 'Beaten'],
		   'Format': ['Flash', 'HTML', 'Java', 'Others', 'Ren\'Py', 'RPGM', 'Unity', 'Wolf'],
		   'Art': ['3D', 'Drawn', 'Pixel', 'Real Porn', 'Text']}

TAG_TOG = ['Animated', 'Bestiality', 'Corruption', 'Femdom', 'Footjob', 'Furry', 'Futa/Trans',
		   'Gay', 'Gross', 'Incest', 'Loli', 'Monster Girl', 'Transformation', 'Vore']
TAG_LST = {'Protagonist': ['Unknown', 'Male', 'Female', 'Futa/Trans', 'Male/Female', 'Multiple']}

TAG_EQU = {'scat': 'gross', 'urination': 'gross', 'female domination': 'femdom', 'sissyfication': 'transformation'}
CAT_EQU = {'text based': 'text', 'real porn': 'real porn', '3dcg': '3d'}

with open(os_path.join(TOPDIR, 'data.json'), 'r') as f:
	OLD_DATA = json.load(f)
