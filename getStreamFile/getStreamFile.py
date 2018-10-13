from browsermobproxy import Server
from selenium import webdriver
import time

def main():
	print(getStreamFile("http://baskino.me/films/boeviki/105-nachalo.html"))

def getStreamFile(linkToFilm):
	server = Server(r"./browsermob-proxy/bin/browsermob-proxy")
	server.start()
	proxy = server.create_proxy()

	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
	chrome_options.add_argument("headless")
	browser = webdriver.Chrome(chrome_options=chrome_options)

	proxy.new_har("defaultName")
	browser.get(linkToFilm)

	# that's for serials
	#element = browser.find_element_by_xpath('//*[@id="episode-code"]/iframe')

	# and that's for movies
	element = browser.find_element_by_xpath('//*[@id="basplayer_hd"]/iframe')

	element.click()
	element.click() # double-click to ensure that video will load

	i = 0

	while True:
		print("wait...")
		time.sleep(0.1)
		i = i + 0.1
		for elem in proxy.har['log']['entries']:
			if "request" in elem.keys():
				if "queryString" in elem['request'].keys():
					if len(elem['request']['queryString']) > 0 and elem['request']['queryString'][0]['name'] == "tok":
						browser.quit()
						server.stop()
						if "m3u8" in elem['request']['url']:
							return elem['request']['url']

		if i > 10:
			print("Error in getting requests. Restart the app.") # TODO: restart browser() in case requests won't load

if __name__ == "__main__":
	main()

