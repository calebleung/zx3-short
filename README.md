# zx3-short

## About

Someone mentioned, in passing, how one would go about creating a link shortner.

I couldn't get it out of my head, so here's a link shortner.

## Requirements

* Python 3.3 (Flask needs 3.3+, 3.5 was used during dev)
* Flask
* SQL Alchemy
* requests
* [Google Safe Browsing API key](https://developers.google.com/safe-browsing/lookup_guide#GettingStarted)

## Usage

Run `python run_once.py` to create the sqlite db, then a `python app.py` will do the trick.

## How-to Link

To create a link, either:

* do a POST to / with form data where the name is 'url' and value is the URL to be shortened. A shortened link will be returned.
* Go to http://example.com/http://linktobe.shortened/here and you will be directed to the info page of the shortened link.