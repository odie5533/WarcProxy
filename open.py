from tornado_proxy.proxy import run_proxy
import tornado

port = 8000
run_proxy(port, start_ioloop=False)

ili=tornado.ioloop.IOLoop.instance()
tornado.ioloop.PeriodicCallback(lambda: None,500,ili).start()

print "Opening proxy on port {}".format(port)
ili.start()
