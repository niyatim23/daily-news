from flask import Flask, jsonify, request
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
from collections import Counter
import string

#http://127.0.0.1:5000/custom_request/virus/2020-02-21/2020-03-06/medical-news-today
#http://127.0.0.1:5000/get_sources/health
#http://127.0.0.1:5000/top_headlines

app = Flask(__name__)


@app.route('/')
def render_page():
	return app.send_static_file("index.html")


@app.route('/top_headlines/')
def top_headlines():
	newsapi = NewsApiClient(api_key = "9a9be6bb99934ba68825728cba40674b")
	top_headlines = newsapi.get_top_headlines(page_size = 30)
	articles = top_headlines["articles"]
	

	count = 0
	filtered_headlines = []
	for article in articles:
		if count < 5:
			if  "author" in article and article["author"] != None and len(article["author"]) != 0 and \
				"description" in article and article["description"] != None and len(article["description"]) != 0 and \
				"title" in article and article["title"] != None and len(article["title"]) != 0 and \
				"url" in article and article["url"] != None and len(article["url"]) != 0 and \
				"urlToImage" in article and article["urlToImage"] != None and len(article["urlToImage"]) != 0 and \
				"publishedAt" in article and article["publishedAt"] != None and len(article["publishedAt"]) != 0 and \
				"source" in article and article["source"] != None and len(article["source"]) != 0 and \
				"id" in article["source"] and article["source"]["id"] != None and len(article["source"]["id"]) != 0 and \
				"name" in article["source"] and article["source"]["name"] != None and len(article["source"]["name"]) != 0: 
				filtered_headlines.append(article)
				count += 1
		else:
			break


	top_words_dict = Counter("".split())
	count = 0
	stop_words = ["a","a's","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","b","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","d","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","e","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","f","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","g","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","h","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","inc","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","j","just","k","keep","keeps","kept","know","knows","known","l","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","m","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","n","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","o","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","p","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","q","que","quite","qv","r","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","s","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","u","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","uucp","v","value","various","very","via","viz","vs","w","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","wonder","would","would","wouldn't","x","y","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","z","zero"]
	for article in articles:
		if count < 30:
			if "title" in article and article["title"] != None and len(article["title"]) != 0:
				clean_title = []
				for word in article["title"].split():
					word = word.replace(",", "").replace(";", "").replace(":", "").replace("!", "").replace("%", "").replace("#", "").replace("(", "").replace(")", "").replace('"', "").replace("[", "").replace("]", "").replace(".", "").replace("/", "")
					if (not(word.isdecimal())) and (len(word) > 1) and (word.lower() not in stop_words):
						if word.lower() not in clean_title or word not in clean_title: 
							clean_title.append(word)
				top_words_dict = top_words_dict + Counter(clean_title)
				count += 1
		else:
			break
	sorted_top_words = sorted([{'word':k, 'size': v * 5} for k,v in top_words_dict.items()], key = lambda x: x['size'], reverse = True)[:30]

	cnn_top_headlines = newsapi.get_top_headlines(page_size = 30, sources = "cnn", language = "en")
	articles = cnn_top_headlines["articles"]
	filtered_cnn_headlines = []
	count = 0
	for article in articles:
		if count < 4:
			if  "author" in article and article["author"] != None and len(article["author"]) != 0 and \
				"description" in article and article["description"] != None and len(article["description"]) != 0 and \
				"title" in article and article["title"] != None and len(article["title"]) != 0 and \
				"url" in article and article["url"] != None and len(article["url"]) != 0 and \
				"urlToImage" in article and article["urlToImage"] != None and len(article["urlToImage"]) != 0 and \
				"publishedAt" in article and article["publishedAt"] != None and len(article["publishedAt"]) != 0 and \
				"source" in article and article["source"] != None and len(article["source"]) != 0 and \
				"id" in article["source"] and article["source"]["id"] != None and len(article["source"]["id"]) != 0 and \
				"name" in article["source"] and article["source"]["name"] != None and len(article["source"]["name"]) != 0: 
				filtered_cnn_headlines.append(article)
				count += 1
		else:
			break


	fox_top_headlines = newsapi.get_top_headlines(page_size = 30, sources = "fox-news", language = "en")
	articles = fox_top_headlines["articles"]
	filtered_fox_headlines = []
	count = 0
	for article in articles:
		if count < 4:
			if  "author" in article and article["author"] != None and len(article["author"]) != 0 and \
				"description" in article and article["description"] != None and len(article["description"]) != 0 and \
				"title" in article and article["title"] != None and len(article["title"]) != 0 and \
				"url" in article and article["url"] != None and len(article["url"]) != 0 and \
				"urlToImage" in article and article["urlToImage"] != None and len(article["urlToImage"]) != 0 and \
				"publishedAt" in article and article["publishedAt"] != None and len(article["publishedAt"]) != 0 and \
				"source" in article and article["source"] != None and len(article["source"]) != 0 and \
				"id" in article["source"] and article["source"]["id"] != None and len(article["source"]["id"]) != 0 and \
				"name" in article["source"] and article["source"]["name"] != None and len(article["source"]["name"]) != 0: 
				filtered_fox_headlines.append(article)
				count += 1
		else:
			break

	response = {}
	response["slideshow-articles"] = filtered_headlines
	response["sorted-top-words"] = sorted_top_words
	response["cnn-articles"] = filtered_cnn_headlines
	response["fox-articles"] = filtered_fox_headlines

	return jsonify(response)



@app.route('/get_sources/<category>')
def get_sources(category):
	newsapi = NewsApiClient(api_key = "9a9be6bb99934ba68825728cba40674b")
	if category == "all":
		sources = newsapi.get_sources(language = "en", country = "us")
	else:
		sources = newsapi.get_sources(category = category, language = "en", country = "us")
	if(len(sources["sources"]) < 10):
		return jsonify(sources["sources"])
	else:
		return jsonify(sources["sources"][:10])


@app.route('/custom_request/<keyword>/<from_date>/<to_date>/<source>')
def custom_request(keyword, from_date, to_date, source):
	newsapi = NewsApiClient(api_key = "9a9be6bb99934ba68825728cba40674b")
	try:
		if(source == "all"):
			custom_headlines = newsapi.get_everything(q = keyword, from_param = from_date, to = to_date, language = "en", page_size = 30, sort_by = "publishedAt")
		else:
			custom_headlines = newsapi.get_everything(q = keyword, from_param = from_date, to = to_date, sources = source, language = "en", page_size = 30, sort_by = "publishedAt")
		articles = custom_headlines["articles"]
		filtered_custom_headlines = []
		count = 0
		for article in articles:
			if count < 15:
				if "author" in article and article["author"] != None and len(article["author"]) != 0 and \
					"description" in article and article["description"] != None and len(article["description"]) != 0 and \
					"title" in article and article["title"] != None and len(article["title"]) != 0 and \
					"url" in article and article["url"] != None and len(article["url"]) != 0 and \
					"urlToImage" in article and article["urlToImage"] != None and len(article["urlToImage"]) != 0 and \
					"publishedAt" in article and article["publishedAt"] != None and len(article["publishedAt"]) != 0 and \
					"source" in article and article["source"] != None and len(article["source"]) != 0 and \
					"name" in article["source"] and article["source"]["name"] != None and len(article["source"]["name"]) != 0: 
					filtered_custom_headlines.append(article)
					count += 1
			else:
				break	
	except NewsAPIException as exception:
		filtered_custom_headlines = exception.__dict__
	return jsonify(filtered_custom_headlines)


