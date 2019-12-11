import re
import glob
import PyPDF2
import textract

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

folder = '//daten.ht.tu-berlin.de/home/Protokolle'

def extract_keywords(pdf_file):

	text = ""

	byte = textract.process(pdf_file)

	text += byte.decode("utf-8")

	tokens = word_tokenize(text)

	punctuations = ['(',')',';',':','[',']',',']

	stop_words = stopwords.words('german')

	keywords = [word for word in tokens if not word in stop_words and not word in punctuations]

	keyword_set = set(keywords)

	return list(keywords)


if __name__ == "__main__":

	folder = input("Enter file folder:")

	word = input("Enter search word:")

	files = glob.glob(folder + "*.pdf")

	for pdf in files:

		keyword_list = extract_keywords(pdf)

		if word in keyword_list:

			print("Found in " + pdf)





