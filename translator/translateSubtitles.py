from py_translator import Translator

def main():
	print(translateSubtitles("Привет, меня зовут XoMute"))

def translateSubtitles(subtitles):

	translator = Translator()
	translated = translator.translate(text=subtitles, dest='en', src='ru').text
	return translated

if __name__=="__main__":
	main()