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

Limitations
===========
WarcProxy only creates an HTTP proxy, not HTTPS. This means that any traffic
sent using end-to-end encryption will not be saved to a WARC file. To overcome
this limitation, the Python [mitmproxy library](http://mitmproxy.org/) could be
used. One possible drawback to using mitmproxy is that it does not appear to use
a robust asynchronous socket library like Tornado or Twisted.
