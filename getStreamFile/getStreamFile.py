from browsermobproxy import Server
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
#from threading import Thread
import time

#proxyContainer = {'proxy':None, 'server':None}


#def loadProxy(holder):

    #server = Server(r"c:\Users\Alex\Documents\GitHub\Hackathon_MEGOGO_2018\getStreamFile\browsermob-proxy\bin\browsermob-proxy")
    #server.start()
    #proxy = server.create_proxy()

    #holder['proxy'] = proxy
    #holder['server'] = server
    #print("PROXXXY LOADED")


#proxyThread = Thread(target=loadProxy,args=(proxyContainer,))
#proxyThread.start()

def main():
    print(getStreamFile("http://baskino.me/films/boeviki/105-nachalo.html"))

def getStreamFile(linkToFilm):
    #print("WAITING FOR PROXY")
    #proxyThread.join()
    #print("DONE WAITING")
    #proxy = proxyContainer["proxy"]
    #server = proxyContainer["server"]

    server = Server(r"c:\Users\Alex\Documents\GitHub\Hackathon_MEGOGO_2018\getStreamFile\browsermob-proxy\bin\browsermob-proxy")
    server.start()
    proxy = server.create_proxy()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    chrome_options.add_argument("headless")
    browser = webdriver.Chrome(chrome_options=chrome_options)

    proxy.new_har("defaultName")
    browser.get(linkToFilm)

    element = 0
    try:
        # that's for serials
        element = browser.find_element_by_xpath('//*[@id="episode-code"]/iframe')

    except NoSuchElementException:

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
                        if "m3u8" in elem['request']['url']:
                        	browser.quit()
	                        server.stop()
	                        return elem['request']['url']

        if i > 20:
            print("Error in getting requests. Restart the app.") # TODO: restart browser() in case requests won't load

if __name__ == "__main__":
    main()

