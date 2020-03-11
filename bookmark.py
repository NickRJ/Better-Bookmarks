#!/usr/bin/env python3

'''
	Adds bookmarks to the home page & downloads favicons to the favicons directory
'''

from bs4 import BeautifulSoup
import requests
import os.path
from urllib.parse import urlparse, urljoin

def download_favicon(url, icon_name):
	try:
		r = requests.get(url)
		soup = BeautifulSoup(r.content, features='html.parser')
		base_url = '{url.scheme}://{url.netloc}'.format(url=urlparse(url)) 

		favicon_url = soup.find('link', rel='shortcut icon')
		if favicon_url is None:
			favicon_url = soup.find('link', rel='icon')
		if favicon_url is None:
			favicon_url = urljoin(base_url, 'favicon.ico') 
		else:
			favicon_url = favicon_url['href']

		# if favicon url is relative, join it with base url 
		parsed_url = urlparse(favicon_url)	
		if parsed_url.scheme == '': 
			favicon_url = urljoin(base_url, favicon_url) 

		# attempt to download favicon
		img = requests.get(favicon_url)
		if img.status_code == 200 and len(img.content) != 0:
			with open('favicons/' + icon_name, 'wb') as f:
				f.write(img.content)
				print('Favicon added!\n')
		else:
			print('Unable to download favicon from {}\n'.format(favicon_url))
	except:
		print('Unable to connect to {}\n'.format(url)) 


def main():
	try:	
		with open('index.html') as f:
			soup = BeautifulSoup(f.read(), features='html.parser')
	except IOError:
		print('Error: Unable to open index.html')
		return

	h1_tags = soup.find_all('h1')

	if len(h1_tags) == 0:
		print('Error: No <h1> tags found in body of index.html')
		return

	# select category
	print('\nCategories:')
	for i, category in enumerate(h1_tags):
		print('{}: {}'.format(i, category.string))
	print()

	category = -1 
	while True:
		try:	
			category = int(input('Select category (enter index): '))
			if 0 <= category < len(h1_tags):
				break
		except ValueError:
			continue	
	
	url = ''
	while len(url) == 0 or len(url.replace('.', ' ').split()) == 1:
		url = input('Enter url: ') 
	title = ''	
	while len(title) == 0:
		title = input('Enter title: ')

	parsed_url = urlparse(url)

	# add http protocol if missing
	if parsed_url.scheme == '':
		url = 'http://' + url
		parsed_url = urlparse(url)

	# create new <a> tag
	tag = soup.new_tag('a', href=url)
	tag.string = title

	h1 = h1_tags[category]
	current_tag = h1.next_sibling 

	# append <a> tag to correct <h1> tag	
	# if category is empty, insert <a> tag right after heading 
	if current_tag.name != 'a':
		h1.insert_after(tag)
	else:
		# else search for last <a> tag under current heading
		while current_tag.next_sibling.name == 'a':
			current_tag = current_tag.next_sibling 
	
		current_tag.insert_after(tag)
	
	with open('index.html', 'w') as f:
		f.write(str(soup))
	
	print('\nNew bookmark added to {}\n'.format(h1.string))

	# download favicon if not in favicons directory
	icon_name = parsed_url.netloc + '.ico'	
	if not os.path.isfile('favicons/' + icon_name):
		print('Downloading favicon... ')
		download_favicon(url, icon_name)


if __name__ == '__main__':
	main()
