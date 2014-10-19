import cgi
import urllib
import webapp2

from google.appengine.ext import ndb

HTML_HEADER = """
<html>
	<head>
	</head>
	<body>
"""

HTML_FOOTER = """
		<form action="/write" method="post">
			<div>User Name: <input value="%s" name="chat_name"></div>
			<div><textarea name="content" rows="3" cols="60"></textarea></div>
			<div><input type="submit" value="Add Message"></div>
		</form>
	</body>
</html>
"""

DEFAULT_CHAT_NAME = "Test_Chat"

def chatlog_key(chatlog_name=DEFAULT_CHAT_NAME):
	return ndb.Key('ChatLog', chatlog_name)

class ChatLog(ndb.Model):
	author = ndb.StringProperty(indexed=False)
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write(HTML_HEADER)

		user = self.request.get('name', "")

		#Insert DB Query here.
		historyQuery = ChatLog.query(ancestor = chatlog_key(DEFAULT_CHAT_NAME)).order(+ChatLog.date)
		history = historyQuery.fetch(10)

		for item in history:
			self.response.write('<b>%s</b>: ' % cgi.escape(item.author))
			self.response.write('%s<br>' % cgi.escape(item.content))

		self.response.write(HTML_FOOTER % user)

class ChatHandler(webapp2.RequestHandler):
	def post(self):
		user = self.request.get('chat_name')
		message = self.request.get('content')
		chat = ChatLog(parent=chatlog_key(DEFAULT_CHAT_NAME))
		chat.author = user
		chat.content = message
		chat.put()
		query_params = {'name': user}
		self.redirect('/?' + urllib.urlencode(query_params))

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/write', ChatHandler),
], debug=True)