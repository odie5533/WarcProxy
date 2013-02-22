WarcProxy
=========
WarcProxy is a simple HTTP proxy that saves all HTTP traffic to a file. The file
format used is the Web ARChive (WARC) format (ISO 28500). WarcProxy uses the
Tornado HTTP library, owned by Facebook. The library is asynchronous and
scalable.

Prerequisites
=============
WarcProxy requires the [Tornado library](http://www.tornadoweb.org/).

Usage
=====
To start the proxy, run:

    $ python open.py

This will create a local proxy on port 8000 and begin saving traffic to a file
named out.warc.gz.

How to view WARC files
======================
After creating a WARC file, the contents can be played back. One way to view the
saved contents is to use [warc-proxy](https://github.com/alard/warc-proxy).
Warc-proxy creates a proxy that channels traffic from a web browser and responds
to requests to view websites. Rather than sending the live website, warc-proxy
replays the saved contents from the WARC file.

Practical uses
==============
The proxy can be used along with any web browser to archive an entire browsing
session, including any external assets such as images, CSS, or JavaScript.
Because the method uses a full proxy, even JavaScript files that a dynamically
imported by other JavaScript files at runtime will be archived.

One example use would be manually archive individual parts of a website, or
to manually archive a web application that uses dynamic asset retrieval.

Comparison
----------
Archives of http://www.pcgamer.com/ obtained using different methods result in
very different renderings as each crawler uses its own rules to download assets.

An archive using wget was obtained by calling:

    $ wget -E -p -robots=off --warc-file=pcg http://www.pcgamer.com/

An archive using WarcMiddleware was obtained by calling:

    $ python crawler.py --url http://www.pcgamer.com/

An archive using Flashfreeze was obtained by exporting the urls and archiving
them using WarcMiddleware's --url-file argument. Flashfreeze is a simple program
that uses the Ghost.py library to gather asset urls by running a headless
browser and navigating to a url. The headless browser is provided by Qt's
QWebPage.

An archive using WarcProxy was obtained by navigating to the website in
Google Chrome while using the proxy.

A render of a previous version of the website was obtained by visiting
Archive.org's WayBackMachine.

WARC files were then rendered using warc-proxy in Google Chrome. The rendering
of WARC files from different crawlers is significantly different. The only
method used that crawled the Flash ads on the site was using WarcProxy to
manually navigate to the site.

See below for comparison images, or the Compare directory for full size images.

Further application
-------------------
Another example would be to gather external assets from a website after
performing a crawl using a more rudimentary program. The external features of
a site that were not properly crawled, such as Flash content or dynamically
loaded JavaScript, could be archived using WarcProxy and then merged into the
WARC file from the automated crawl. Then when replaying the WARC file, the
external assets would load.

Limitations
===========
WarcProxy only creates an HTTP proxy, not HTTPS. This means that any traffic
sent using end-to-end encryption will not be saved to a WARC file. To overcome
this limitation, the Python [mitmproxy library](http://mitmproxy.org/) could be
used. One possible drawback to using mitmproxy is that it does not appear to use
a robust asynchronous socket library like Tornado or Twisted.

Comparison images
=================
Control:

![Control](https://raw.github.com/iramari/WarcProxy/master/Compare/Control_thumb.png "Control")

wget:

![wget](https://raw.github.com/iramari/WarcProxy/master/Compare/wget_thumb.png "wget")

WayBackMachine:

![alt text](https://raw.github.com/iramari/WarcProxy/master/Compare/WayBackMachine_thumb.png "WayBackMachine")

WarcMiddleware:

![alt text](https://raw.github.com/iramari/WarcProxy/master/Compare/WarcMiddleware_thumb.png "WarcMiddleware")

Flashfreeze:

![alt text](https://raw.github.com/iramari/WarcProxy/master/Compare/Flashfreeze_thumb.png "Flashfreeze")

WarcProxy:

![alt text](https://raw.github.com/iramari/WarcProxy/master/Compare/WarcProxy_thumb.png "WarcProxy")
