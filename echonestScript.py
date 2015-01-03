import urllib2,urllib,time,datetime
from bs4 import BeautifulSoup

#Echonest Api key and base URL
api_key = "Your Echonest api key"
baseUrl = "http://developer.echonest.com/api/v4/artist/"

#last.fm Api key and base URL
LastFMApiKey = "Your last.fm api key"
LastFMBaseUrl = "http://ws.audioscrobbler.com/2.0/?method="

# Helper Function 
def formatString(name):
	space,pos=0,0
	while pos!=-1:
		pos=name.find(' ',pos+1)
		space+=1
	space-=1
	return name.replace(' ','+',space)

#last.fm, to get name corrections
def getCorrection(Name):
	Name = formatString(Name)
	searchUrl = LastFMBaseUrl + "artist.getcorrection&artist=" + Name + "&api_key=" + LastFMApiKey
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	exists = soup.find("lfm",{"status": "ok"})
	if exists:
		if soup.find("name") is not None:
			return soup.find("name").string
		else:
			return Name
	else:
		return "DoesNotExist"

#Image Function to get images from Echonest
def getImages(name):
	name = formatString(name)
	searchUrl = searchUrl = baseUrl + "images?api_key=" + api_key + "&name=" + Name + "&format=xml&results=4&start=0"
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	images = soup.find_all("image")
	imageList = []

	for image in images:
		imageList.append(image.find("url").string)

	for image in imageList:
		image.replace("_","252")

	return imageList

# Get Biography Function, Returns a list of dictionaries containing biographies, from Echonest 
def getBiographies(Name):
	Name = formatString(Name)
	searchUrl = baseUrl + "biographies?api_key=" + api_key + "&name=" + Name + "&format=xml&results=10&start=0"
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	bioList = soup.find("biographies").find_all("biography")
	bioResult = []
	for bio in bioList:
		dic = {}
		dic['text'] = bio.find("text").string
		dic['site'] = bio.find("site").string
		dic['url'] = bio.find("url").string
		bioResult.append(dic)
	return bioResult


# Get News Function, Returns a list of dictionaries containing news, from Echonest
def getNews(Name):
	Name = formatString(Name)
	searchUrl = baseUrl + "news?api_key=" + api_key + "&name=" + Name + "&format=xml&results=20&start=0"
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	newsList = soup.find("news").find_all("news")
	newsResult = []
	for news in newsList:
		dic = {}
		dic['name'] = news.find("name").string
		dic['summary'] = news.find("summary").string
		dic['url'] = news.find("url").string
		newsResult.append(dic)
	return newsResult


# Get Reviews Function, from Echonest
def getReviews(Name):
	Name = formatString(Name)
	searchUrl = baseUrl + "reviews?api_key=" + api_key + "&name=" + Name + "&format=xml&results=10&start=0"
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	reviewList = soup.find("reviews").find_all("review")
	reviewResult = []
	for review in reviewList:
		dic = {}
		dic['name'] = review.find("name").string
		dic['summary'] = review.find("summary").string
		dic['summary'] = review.find("summary").string
		reviewResult.append(dic)
	return reviewResult


# Get Blogs Function, from Echonest
def getBlogs(Name):
	Name = formatString(Name)
	searchUrl = baseUrl + "blogs?api_key=" + api_key + "&name=" + Name + "&format=xml&results=20&start=0"
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	blogList = soup.find("blogs").find_all("blog")
	blogResult = []
	for blog in blogList:
		dic = {}
		dic['name'] = blog.find("name").string
		dic['summary'] = blog.find("summary").string
		dic['url'] = blog.find("url").string
		blogResult.append(dic)
	return blogResult

#Get Genres for an artist, Echonest
def getGenres(Name):
	Name = formatString(Name)
	searchUrl = baseUrl + "profile?api_key=" + api_key + "&name=" + Name + "&bucket=genre&format=xml"
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	genres = soup.find("genres").find_all("genre")
	genreResult = []
	for genre in genres:
		dic = {}
		dic['name'] = genre.find("name").string
		genreResult.append(dic)
	return genreResult[:7]

# Get Similar Artists Function, from Echonest
def getSimilarArtists(Name):
	Name = formatString(Name)
	searchUrl = baseUrl + "similar?api_key=" + api_key + "&name=" + Name + "&format=xml&results=10&start=0"
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	similarList = soup.find("artists").find_all("artist")
	similarResult = []
	for artist in similarList:
		dic = {}
		dic['name'] = artist.find("name").string
		similarResult.append(dic)
	return similarResult[:12]


# Get Top Songs Function, from Last.fm
def getTopSongs(Name):
	Name = getCorrection(Name)
	if Name == "DoesNotExist":
		return []
	Name = formatString(Name)
	searchUrl = LastFMBaseUrl + "artist.gettoptracks&artist=" + Name + "&api_key=" + LastFMApiKey
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	songList = soup.find("toptracks").find_all("track")
	songResult = []
	genreList = getGenres(Name)
	for song in songList:
		dic = {}
		dic['name'] = song.find("name").string
		dic['artist'] = song.find("artist").find("name").string
		songResult.append(dic)
	return songResult,genreList

def getInfo(Name):
	Name = getCorrection(Name)
	if Name == "DoesNotExist":
		return []
	Name = formatString(Name)
	searchUrl = LastFMBaseUrl + "artist.getinfo&artist=" + Name + "&api_key=" + LastFMApiKey
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	infoList = soup.find("artist")
	similar = infoList.find("similar").find_all("artist")
	bioResult = infoList.find("bio").find("summary").string
	infoResult = []
	similarList = []
	infoResult.append(bioResult)
	imageList = []
	sizes = ["small","medium","large","extralarge"]
	for sz in sizes:
		imageList.append(infoList.find("image",{"size":sz}).string)
	for sim in similar:
		dic = {}
		dic['name'] = sim.find('name').string
		dic['url'] = sim.find('url').string
		similarList.append(dic)
	infoResult.append(similarList)
	infoResult.append(infoList.find("name").string)
	infoResult.append(imageList)
	return infoResult

# Get Top Albums, from Last.fm
def getTopAlbums(Name):
	Name = getCorrection(Name)
	if Name == "DoesNotExist":
		return []
	Name = formatString(Name)
	searchUrl = LastFMBaseUrl + "artist.gettopalbums&artist=" + Name + "&api_key=" + LastFMApiKey
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	albumList = soup.find("topalbums").find_all("album")[:10]
	albumResult = []
	similarList = getSimilarArtists(Name)
	for album in albumList:
		dic = {}
		dic['name'] = album.find("name").string
		dic['artist'] = album.find("artist").find("name").string
		dic['url'] = album.find("url").string
		albumResult.append(dic)
	return (albumResult,similarList)

#echonest
def getArtistsByGenre(Name):
	Name = formatString(Name)
	searchUrl = "http://developer.echonest.com/api/v4/genre/artists?api_key=" + api_key  + "&format=xml&results=10&bucket=hotttnesss"+"&name=" + Name
	request = urllib2.Request(searchUrl)
	try:
		response = urllib2.urlopen(request).read()
		soup = BeautifulSoup(response,"xml")
		Artists = soup.find("artists").find_all("artist")
		artistResult = []
		for artist in Artists:
			dic = {}
			dic['name'] = artist.find("name").string
			artistResult.append(dic)
		return artistResult
	except urllib2.HTTPError:
		return []

#Last.fm
def getAlbumInfo(artist,album):
	artist = getCorrection(artist)
	if artist == "DoesNotExist":
		return []
	album = formatString(album)
	searchUrl = LastFMBaseUrl + "album.getinfo"+"&api_key=" + LastFMApiKey+"&artist="+artist+"&album="+album
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	albumInfo = soup.find("album")
	albumRes = []
	albumRes.append(albumInfo.find("name").string)
	albumRes.append(albumInfo.find("artist").string)
	albumRes.append(albumInfo.find("image",{"size":"extralarge"}).string)
	albumRes.append(albumInfo.find("summary").string)
	albumRes.append(albumInfo.find("url").string)
	trackList = []
	tracks = albumInfo.find("tracks").find_all("track")
	for tr in tracks:
		dic = {}
		dic['name'] = tr.find("name").string
		dic['url'] = tr.find("url").string
		trackList.append(dic)
	return (albumRes,trackList)

#last.fm
def getTrackInfo(artist,track):
	artist = getCorrection(artist)
	if artist == "DoesNotExist":
		return []
	track = formatString(track)
	searchUrl = LastFMBaseUrl + "track.getinfo"+"&api_key=" + LastFMApiKey+"&artist="+artist+"&track="+track
	request = urllib2.Request(searchUrl)
	response = urllib2.urlopen(request).read()
	soup = BeautifulSoup(response,"xml")
	TInfo = []
	TInfo.append(soup.find("track").find("name").string)
	TInfo.append(soup.find("track").find("artist").find("name").string)
	TInfo.append(soup.find("track").find("album").find("image",{"size":"extralarge"}).string)
	TInfo.append(soup.find("track").find("wiki").find("summary").string)
	TInfo.append(soup.find("track").find("url").string)
	return TInfo