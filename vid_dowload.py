#!/usr/bin/env python

from __future__ import print_function
import requests
from bs4 import BeautifulSoup as bs
import sys
import logging
from os.path import splitext,join
import uuid

# pip install beautifulsoup4
# pip install requests

logger = logging.getLogger(__name__)
# handler = logging.StreamHandler()
handler = logging.FileHandler('/tmp/vid_download.log')
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

proxies = {
	"https":"socks5://localhost:8157",
	"http":"socks5://localhost:8157"
}

def getUrlWithoutParams(url):
	return url.split('?')[0]

def getFileExtension(path):
	return splitext(path)[1]

def makeFileName(baseDir="/tmp", extension=".mp4"):
	return join(baseDir, "{}{}".format(str(uuid.uuid4())[:8], extension))

def downloadFile(urlFrom,pathTo):
	logger.info("Downloading {} to {}".format(urlFrom, pathTo))
	
	try:
		r = requests.get(urlFrom, stream=True, proxies=proxies)
		with open(pathTo, 'wb') as f:
			for chunk in r.iter_content(chunk_size=1024 * 1024):
				if chunk:
					f.write(chunk)
		logger.info("File {} downloaded to {}".format(urlFrom, pathTo))
	
	except Exception as e:
		logger.error(e.message)
	

def main(baseurl="https://distillvideo.com/"):
	if len(sys.argv) < 2:
		logger.error("invalid number of input")
		logger.debug(sys.argv)
		sys.exit(-1)
	
	url = sys.argv[1]
	logger.info("URL: {}".format(url))
	logger.debug("Getting download link")

	link=None

	try:
		page = requests.get("https://distillvideo.com/", params={"url":url}, proxies=proxies)
		soup = bs(page.text, 'html.parser')
		link = soup.find_all(class_='vd-down btn btn-default btn-download')[0]['href']
		logger.debug("Download Link: {}".format(link))
		
		new_link = getUrlWithoutParams(link)
		file_extension = getFileExtension(new_link)
		filepath = makeFileName(extension=file_extension)
		
		logger.debug("Unfluffed: {}".format(new_link))
		logger.debug("File extension: {}".format(file_extension))
		logger.debug("Download path: {}".format(filepath))

		downloadFile(link, filepath)

	except Exception as e:
		logger.error(e.message)
		sys.exit(-1)



if __name__=='__main__':
   main()