import flask
from mwoauth import ConsumerToken, Handshaker, RequestToken
from src.config import Configuration as config
from src.db.sessionmaker import Session
from src.db.database import TokenBind, Verification
from sqlalchemy.exc import IntegrityError
app = flask.Flask(__name__)
consumer_token = ConsumerToken(config.CONSUMER_KEY, config.CONSUMER_SECRET)

@app.route('/')
def index():
    return 'According to all known laws of Wiki, this shit should not work.'


@app.route('/begin')
def begin():
    # Construct a "consumer" from the key/secret provided by MediaWiki
    consumer_token = ConsumerToken(config.CONSUMER_KEY, config.CONSUMER_SECRET)

    # Construct handshaker with wiki URI and consumer
    handshaker = Handshaker("https://meta.mirabeta.org/w/index.php",
                            consumer_token)

    # Step 1: Initialize -- ask MediaWiki for a temporary key/secret for user
    redirect_url, request_token = handshaker.initiate()
    return flask.redirect(redirect_url)
    # # Step 2: Authorize -- send user to MediaWiki to confirm authorization
    # print("Point your browser to: %s" % redirect)  #
    # response_qs = input("Response query string: ")
    #
    # # Step 3: Complete -- obtain authorized key/secret for "resource owner"
    # access_token = handshaker.complete(request_token, response_qs)


@app.route('/oauth-callback/<int:user_id>')
def callback(user_id):
    session = Session()
    bind = (session.query(TokenBind).filter(TokenBind.discord_id == user_id).order_by(TokenBind.timestamp.desc())).first()
    handshaker = Handshaker("https://meta.mirabeta.org/w/index.php",
                            consumer_token)
    access_token = handshaker.complete(RequestToken(bind.token, bind.secret), flask.request.query_string)
    identity = handshaker.identify(access_token)
    session.delete(bind)
    session.add(Verification(discord_id=user_id, wiki_username=identity['username'], wiki_id=identity['sub']))
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return 'You are already verified!' #TODO: Possibly replace the old row with the new auth
    return identity #TODO: Make this a redirect to a confirmation page
