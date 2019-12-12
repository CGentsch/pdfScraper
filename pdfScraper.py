import sys
import re
import glob
import PyPDF2
import textract
import ntpath

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class pdfScraper(object):

	def __init__(self):
		self._splash()
		self.folder = "//daten.ht.tu-berlin.de/home/Protokolle/"

	def _path_leaf(self, path):
		head, tail = ntpath.split(path)
		return tail or ntpath.basename(head)

	def _extract_keywords(self, file):
		text = ""
		byte = textract.process(file, encoding='utf8')
		text += byte.decode("utf-8")
		tokens = word_tokenize(text)
		punctuations = ['(',')',';',':','[',']',',']
		stop_words = stopwords.words('german')
		keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
		keyword_set = set(keywords)
		return list(keywords)

	def scrape(self, keyword):
		files = glob.glob(self.folder + "*.pdf")
		pdf_list = []
		for pdf in files:
			keyword_list = self._extract_keywords(pdf)
			if keyword in keyword_list:
				pdf_list.append(self._path_leaf(pdf))
		return self._print(pdf_list)

	def _splash(self):
		print("\n\n")
		print("Welcome to pdfScraper\n".center(80))
		print("Copyright © 2019 Christian Gentsch".center(80))
		print("This work is free, You can redestribute it and/or modify it under the".center(80))
		print("terms of the Do What The Fuck You Want To Public License, Version 2,".center(80))
		print("as published by Sam Hocevar. See http://www.wtfpl.net/ for more details".center(80))
		print("\n\n")

	def _print(self, pdf_list):
		print("\nYour keyword was found in the following documents")
		print("-------------------------------------------------")
		for pdf in pdf_list:
			print(pdf)
		print("\n")

if __name__ == "__main__":

	scraper = pdfScraper()

	while True:

		keyword = input("Insert Keyword.\n", )

		print(scraper.scrape(keyword))
