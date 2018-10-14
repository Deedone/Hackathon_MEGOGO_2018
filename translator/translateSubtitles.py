from py_translator import Translator

def main():
	print(translateSubtitles("Привет, меня зовут XoMute"))

def translateSubtitles(subtitles, dest, src):
	if subtitles == None:
		return ''
	translator = Translator()
	translated = translator.translate(text=subtitles, dest=dest, src=src).text
	return translated

if __name__=="__main__":
	main()
