#!/usr/bin/python

# Download manga from http://www.mangareader.net/
#	TODO:
#         Make the program exit gracefully when it's finished
#	      Figure out why it's stopping randomly while downloading stuff
#	      Implement page scrapers for other sites
#         Allow it to detect which url naming scheme is being used.
#
# Usage: manga_download.py <url of first page to download>

from urllib2 import Request, build_opener
import xml.etree.ElementTree as ET
from re import sub
import os
import re
import sys

siteurl = 'http://www.mangareader.net'
# Not used
title = ''
titleurl = ''
firstvol = '1'
firstpage = '1'

# Take a url from mangareader and download the image for that page. Then return the url for the next image, as well as the url for the image itself.
def getpage(url):
	# Download the requested url
	request = Request(url)
	opener = build_opener()
	response = opener.open(request)
	pagetext = response.read()
	pagetext = sub('&nbsp;', '', pagetext) # The xml parser doesn't like &nbsp;

	# Parse the page into xml for easy processing
	pagexml, ids = ET.XMLID(pagetext)
	
	# Start pulling information from the xml, starting with the link to the next page
	a = ids['imgholder'].find('{http://www.w3.org/1999/xhtml}a')
	nexturl = a.attrib.get('href') # something like '/the-big-o/1/23'
	# Then get the url for the image
	img = a.getchildren()[0]
	imgurl = img.attrib.get('src') # full url of the image, ready to download
	
	return imgurl, nexturl

# Pull the title, volume, and page number from the (relative) url.
# This particular function works for about half of the stuff on there. Apparently the
# other half uses a different url naming scheme.
def parseurl(url):
    # Parse urls of the form
    # /title/chapter/page
	url = url.partition('/')[2] # get rid of the leading slash
	title, sep, rest = url.partition('/')
	volume, sep, page = rest.partition('/')

	if page == '':
		page = '1'

	return title, int(volume), int(page)

# This should work for the other half
def parseurl2(url):
    # Parse urls of the form
    # /348-349893-01/title/chapter-01.html
    # where 01 represents the page number
    m = re.match("/[0-9]+-[0-9]+-([0-9]+)/([a-z\-]+)/chapter-([0-9]+).html", url);
    # title, volume, page
    return m.group(2), int(m.group(3)), int(m.group(1))

# Save an image in the correct directory with a happy filename.
def saveimg(url, title, volume, page):
	# Format the volume and page numbers to strings.
	volume = '%02d' % volume # use two digits for the volume number
	page = '%03d' % page # and three for the page number

	# Directory and image names
	directory = title + '/' + volume
	image_name = title + '-' + volume + '.' + page + '.jpg'

	print url + ' >> ' + directory + '/' + image_name

	request = Request(url)
	response = build_opener().open(request)
	image = response.read()

	# Make the directory if it doesn't already exist.
	if not os.path.exists(directory):
		os.makedirs(directory)

	# Actually save stuff.
	f = open(directory + '/' + image_name, 'w')
	f.write(image)
	f.close()

	return

# The main bit of the program
#nexturl = '/' + titleurl + '/' + firstvol + '/' + firstpage


# Just grab the url for the first page to download from the command line.
nexturl = sys.argv[1]

while True:
	title, vol, page = parseurl(nexturl)
	imgurl, nexturl = getpage(siteurl + nexturl)
	if not imgurl:
		break
	saveimg(imgurl, title, vol, page)

