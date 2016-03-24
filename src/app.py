from flask import Flask, g, render_template, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

import re
import short_config
import string
import random
import requests

engine = create_engine(short_config.DATABASE, echo=short_config.DEBUG)
Base = automap_base()
Base.prepare(engine, reflect=True)
Session = sessionmaker(bind=engine)
Shortlinks = Base.classes.shortlinks

app = Flask(__name__)

def connectDBSession():
    session = Session()
    return session

@app.before_request
def before_request():
    g.db = connectDBSession()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/<path:id>+')
def linkInfo(id):
    results = g.db.query(Shortlinks).filter_by(link_id=id).first()
    if results is None:
        return 'No link for %s' % id

    return render_template('info.html', absPath = short_config.ABS_PATH, shortID=results.link_id, orgURL=results.link_url, hits=results.link_hits)

@app.route('/<path:url>', methods=['GET', 'POST'])
def initLinkCreation(url):
    URL_INDICATORS = ['.', '/', '?', '&', '#']

    if request.method == 'POST' or len(url) >= 12 or any(indicator in url for indicator in URL_INDICATORS):
        resp = setupLinkCreation(url)
        if resp[0]:
            return redirect('%s%s+' % (short_config.ABS_PATH, resp[1]), code=301)
        else:
            return render_template('index.html', error=resp[1])
    else:
        resp = getShortenedLink(url)

    return resp

def setupLinkCreation(url):
    protocol = getProtocolBool(url)
    
    if protocol == 'unknown':
        url = 'http://%s' % (url)
    elif not protocol:
        return [False, 'Invalid protocol.']

    if isAlreadyShortLink(url):
        return [False, 'This link is already a short link from this service.']

    if getStatusCodeBool(url):
        safeBrowsingStatus = getGglSafeBrowsingStatus(url)

        if safeBrowsingStatus == 'ok':
            dupeCheck = isDupe(url)

            if not dupeCheck:
                return [True, performLinkCreation(url)]
            else:
                return [False, '%s has already been shortened with id %s' % (url, dupeCheck)]
        else:
            return [False, 'Google Safe Browsing reports the following: %s' % safeBrowsingStatus[1]]
    else:
        return [False, 'There was an issue accessing the page. Please verify that it is accessible.']

def performLinkCreation(url):
    newLink = Shortlinks(link_id=getRandomID(), link_url=url, link_hits=0)
    g.db.add(newLink)
    g.db.commit()

    return newLink.link_id

def isAlreadyShortLink(url):
    try:
        protocol, url = url.split('://')
        matchDomain = re.compile(short_config.ABS_PATH.split('://')[1])

        if matchDomain.match(url):
            return True

        return False
    except ValueError:
        return True

def isDupe(url):
    results = g.db.query(Shortlinks).filter_by(link_url=url).first()
    if results is None:
        return False

    return results.link_id

def getRandomID():
    character_pool = string.ascii_letters + string.digits
    newID = "".join(random.choice(character_pool) for i in range(5))

    results = g.db.query(Shortlinks).filter_by(link_id=newID).first()
    if results is None:
        return newID

    return getRandomID()

def getShortenedLink(id):
    results = g.db.query(Shortlinks).filter_by(link_id=id).first()
    if results is None:
        return 'No link for %s' % id

    results.link_hits += 1
    g.db.commit()

    return redirect(results.link_url, code=302)

def getProtocolBool(url):
    try:
        protocol, url = url.split('://')

        if protocol in ('http', 'https'):
            return True
        
        return False
    except ValueError:
        # We're assuming it's http. For example, going to the location bar and appending the short linker.
        return 'unknown'

def getStatusCodeBool(url):
    try:
        r = requests.get(url)
        statusCode = r.status_code

        if statusCode < 400:
            return True
    except requests.exceptions.ConnectionError:
        return False

    return False

def getGglSafeBrowsingStatus(url):
    r = requests.get('https://sb-ssl.google.com/safebrowsing/api/lookup?client=%s&key=%s&appver=1.5.2&pver=3.1&url=%s' % (short_config.SB_APP_NAME, short_config.SB_API_KEY, url))

    if r.status_code != 204:
        return [r.status_code, r.text]

    return 'ok'

if __name__ == '__main__':
    app.debug = short_config.DEBUG
    app.run()