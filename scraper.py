from lxml import html
import requests

def bfs(start, depth):
    visited, artists_tags, queue = set(), set(),list(start)
    last = len(queue)-1
    counter = 0
    page_base = 'http://www.last.fm'
    level = 0
    while queue and level != depth:
        artist = queue.pop(0)
        if artist not in visited:

            visited.add(artist)
            pgb = page_base + artist[1]
            page1 = requests.get(pgb)
            tree1 = html.fromstring(page1.content)
            artists_tags |= set(tree1.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section[1]/ul/*/a/text()'))
            similar_artists = zip(tree1.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section[5]/ol/*/div/div/p[1]/a/text()'), 
            						tree1.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section[5]/ol/*/div/div/p[1]/a/@href'))
            queue.extend(similar_artists)

        if counter == last :
        	last = counter + len(queue)
        	level += 1
        counter += 1
    return visited,artists_tags

if __name__ == '__main__':

	page = requests.get('http://www.last.fm/es/user/NevadaStreets')
	tree = html.fromstring(page.content)

	artists = zip(tree.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section[2]/div/ol/*/div/div/p[1]/a/text()'), 
					tree.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section[2]/div/ol/*/div/div/p[1]/a/@href'))

	total = bfs(artists,3)



	print('Artists: ', total[0])
	print('Tags:', total[1])
