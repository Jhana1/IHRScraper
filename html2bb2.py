import re, time
from bs4 import BeautifulSoup

def escapeString(html_doc):
	html_doc.replace("\"", "&quot;")
	html_doc.replace("&", "&amp;")
	html_doc.replace("<", "&lt;")
	html_doc.replace(">", "&gt;")
	return html_doc

def html2bb(html_doc):
	soup = BeautifulSoup(html_doc)
	content = []
	for post in soup.findAll('div', {'class':"postbody"}):
		content.append(escapeString(post2bb(post)))

	return content

def post2bb(soup):
	quoted = []
	for el in soup.findAll('span', style= 'font-weight: bold'):
		el.append('[/b]')
		el.insert(0,'[b]')
		el.replaceWithChildren()

	for el in soup.findAll('span', style= 'font-style: italic'):
		el.append('[/i]')
		el.insert(0,'[i]')
		el.replaceWithChildren()

	for el in soup.findAll('span', style= 'text-decoration: underline'):
		el.append('[/u]')
		el.insert(0,'[u]')
		el.replaceWithChildren()

	for el in soup.findAll('span',style="text-decoration: blink;"):
		el.append('[/blink]')
		el.insert(0,'[blink]')
		el.replaceWithChildren()

	for el in soup.findAll('span',style="text-decoration: line-through;"):
		el.append('[/s]')
		el.insert(0,'[s]')
		el.replaceWithChildren()

	for el in soup.findAll('span',style=re.compile('font-size: (\d+?)%; line-height: normal')):
	    size = re.findall('font-size: (\d+?)%; line-height: normal',el.attrs['style'])[0]
	    el.insert(0,'[size=' + str(size) + ']')
	    el.append('[/size]')
	    el.replaceWithChildren()

	for el in soup.findAll('span', style= re.compile("color: .{6,7}")):
		try:
			el.attrs['onmouseover']
			el.insert(0,'[4spoiler]')
			el.append('[/4spoiler]')
			el.replaceWithChildren()
		except KeyError:
			color = el.attrs['style'][7:14]
			el.insert(0,'[color=' + str(color) + ']')
			el.append('[/color]')
			#el.replaceWithChildren()

	for el in soup.findAll('div', {'class':"codecontent"}):
		el.append('[/code]')
		el.insert(0,'[code]')
		el.replaceWithChildren()
	
	for el in soup.findAll('div', {'class':"quotetitle"}):
		quoted.append(str(el.get_text())[:-7])
		el.clear()

	for el in soup.findAll('div', {'class':"quotecontent"}):
		el.append('[/quote]')
		el.insert(0,'[quote="' + quoted.pop(0) +'"]')
		el.replaceWithChildren()


	links = soup.findAll('a', {'class':"postlink"})
	img = soup.findAll('a', {'class':"postlink img_link"})
	
	s = set(img)
	temp3 = [x for x in links if x not in s]
	links = temp3


	for el in img:
		link = el.attrs['href']
		el.clear()
		el.append('[img]' + link + '[/img]')
		el.replaceWithChildren()


	for el in links:
		link = el.attrs['href']
		el.insert(0,'[url=' + link + ']')
		el.append('[/url]')
		el.replaceWithChildren()

	for el in soup.findAll('br'):
		el.append('\n')
		el.replaceWithChildren()

	for el in soup.findAll('div', align="center"):
		el.append('[/center]')
		el.insert(0,'[center]')
		el.replaceWithChildren()

	for el in soup.findAll('marquee'):
		el.append('[/marquee]')
		el.insert(0,'[marquee]')
		el.replaceWithChildren()

	for el in soup.findAll('object', data=re.compile('.+youtube.+')):
		ids = re.findall('http://www.youtube.com/v/(.+)',el['data'])[0]
		el.insert(0,'[youtube]' + ids + '[/youtube]')
		el.replaceWithChildren()

	for el in soup.findAll('embed'):
		ids = re.findall('id=(.+)',el['flashvars'])[0]
		el.insert(0,'[adultswim]' + ids + '[/adultswim]')
		el.replaceWithChildren()

	for el in soup.findAll('div', style='display: none;'):
		el.insert(0,'[spoiler]')
		el.append('[/spoiler]')
		el.replaceWithChildren()

	for el in soup.findAll('b'):
		el.clear()

	for el in soup.findAll('div', style=" height:300px; overflow:auto; padding:8px; scrollbar-face-color: #1E90FF; scrollbar-highlight-color: #D5D5D5; scrollbar-3dlight-color: ; scrollbar-darkshadow-color: #101010; scrollbar-shadow-color: ; scrollbar-arrow-color: #222222; scrollbar-track-color: #222222;"):
		el.append('[/scrollbox]')
		el.insert(0,'[scrollbox]')
		el.replaceWithChildren()

	
	soup = soup.get_text()
	out = re.sub('(:)\s*?\[spoiler\]',"[spoiler]",soup)
	return out

	#for el in soup.findAll('object', data=re.compile('.+youtube.+')):


