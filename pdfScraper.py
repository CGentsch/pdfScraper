import re
import glob
import PyPDF2
import textract

from getpass import getpass
import requests
from bs4 import BeautifulSoup

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


class FileFetcher(object):
    def __init__(self):
        #share url fuer plenumsprotokolle
        self.base_url = "https://tubcloud.tu-berlin.de/s/60MBrwSi1LjYpFP/"

    def _password_prompt(self):
        passw = getpass(prompt="Passwort für die Datenbank eingeben: ")
        return passw

    def _login(self, session):
        # establish cookie jar by logging in without doing anything
        passw = self._password_prompt()
        login_url = self.base_url + "authenticate/showShare"
        first_response = session.get(login_url)
        first_soup = BeautifulSoup(first_response.text, "html.parser")
        request_token = first_soup.head.get("data-requesttoken")
        sharing_token = first_soup.find("input", id="sharingToken").get("value")

        post_data = {"password": passw}
        post_data.update({"sharingToken": sharing_token})
        post_data.update({"requesttoken": request_token})
        
        response = session.post(login_url, data=post_data)
        soup = BeautifulSoup(response.text, "html.parser")
        if not soup.find("div", {"class":"warning"}):
            cookies = response.cookies
        else:
            raise ConnectionError("Verbindung konnte nicht hergestellt werden. Falsches Passwort?")
        return cookies

    def download_file(self, fname):
        #TODO Raise Exception if fname doesn't exist in shared folder
        with requests.Session() as session:
            cookies = self._login(session)
            download_url = self.base_url + "download?path=%2F&files=" + fname

            byte_file = session.get(download_url, cookies = cookies, allow_redirects = True) 
            with open(fname, "wb") as dlfile:
                dlfile.write(byte_file.content)

if __name__ == "__main__":

	folder = input("Enter file folder:")

	word = input("Enter search word:")

	files = glob.glob(folder + "*.pdf")

	for pdf in files:

		keyword_list = extract_keywords(pdf)

		if word in keyword_list:

			print("Found in " + pdf)





