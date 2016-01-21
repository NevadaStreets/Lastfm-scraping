from lxml import html
import requests

def bfs(start, depth):
    visited, artists_tags, queue = set(), set(), list(start)
    last = len(queue)-1
    counter = 0
    page_base = 'http://www.last.fm'
    level = 0
    while queue and level != depth:
        artist = queue.pop(0)

        if artist not in visited:
            visited.add(artist)
            artist_page = page_base + artist[1]
            page_opened = requests.get(artist_page)
            art_tree = html.fromstring(page_opened.content)


            albums_page = artist_page + "/+albums"
            albums_opened = requests.get(albums_page)
            albs_tree = html.fromstring(albums_opened.content)
            albums_pages = list(albs_tree.xpath('//*[@id="artist-albums-section"]/ol/*/a/@href'))

            tags = set()
            for album in albums_pages:
            	album_page = page_base + album
            	album_opened = requests.get(album_page)
            	alb_tree = html.fromstring(album_opened.content)
            	tags |= set(alb_tree.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section[1]/ul/*/a/text()'))

            tags |= set(art_tree.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section[1]/ul/*/a/text()'))
            artists_tags |= tags

            artist_data = open("./Data/"+artist[0]+".txt", "w")
            artist_data.write(artist[0]+"\n")
            for tag in tags:
            	artist_data.write(tag+"\n")
            artist_data.close()

            similar_page = artist_page + "/+similar"
            similar_opened = requests.get(similar_page)
            sim_tree = html.fromstring(similar_opened.content)
            similar_artists = zip(sim_tree.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section/ol/*/div[1]/div/div/p[1]/a/text()'), 
            						sim_tree.xpath('//*[@id="mantle_skin"]/div[4]/div/div[1]/section/ol/*/div[1]/div/div/p[1]/a/@href'))
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



	print('Artists: ', len(total[0]))
	print('Tags:', len(total[1]))
