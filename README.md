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

## Endpoints

| Method | Endpoint | Example | Info
| :---:  | ---      | ---  |
|   GET  |  /*&lt;URL to shorten here&gt;* | http://example.com/https://google.com/  | Creates new shortened link if one doesn't already exist. Redirects to info page for new link |
| POST | / | http://example.com/ <br />`url:google.com` | Send with `url` form parameter where `url`'s value is the target URL | 
| GET | /*&lt;short link&gt;* | http://example.com/DnEQg | Redirects to target URL |
| GET | /*&lt;short link&gt;*+ | http://example.com/DnEQg+ | Instead of redirecting to target URL, accesses short link info (hit count, target URL) |

