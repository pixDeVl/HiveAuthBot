import flask
from mwoauth import ConsumerToken, Handshaker
from src.config import Configuration as config

app = flask.Flask(__name__)


@app.route('/')
def index():
  return 'According to all known laws of Wiki, this shit should not work.'

@app.route('/begin')
def begin():
  # Construct a "consumer" from the key/secret provided by MediaWiki
  consumer_token = ConsumerToken(config.CONSUMER_KEY, config.CONSUMER_SECRET)

  # Construct handshaker with wiki URI and consumer
  handshaker = Handshaker("https://meta.mirabeta.org/w/index.php",
                          consumer_token,
                          callback='http://localhost/oauth-callback')

  # Step 1: Initialize -- ask MediaWiki for a temporary key/secret for user
  redirect_url, request_token = handshaker.initiate()
  return flask.redirect(redirect_url)
  # # Step 2: Authorize -- send user to MediaWiki to confirm authorization
  # print("Point your browser to: %s" % redirect)  #
  # response_qs = input("Response query string: ")
  #
  # # Step 3: Complete -- obtain authorized key/secret for "resource owner"
  # access_token = handshaker.complete(request_token, response_qs)

@app.route('/oauth-callback')
def callback():
  return(dict(flask.request.args))