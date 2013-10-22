from tornado.simple_httpclient import SimpleAsyncHTTPClient, _HTTPConnection

from . import warcrecords

import functools

"""
Singleton that handles maintaining a single output file for many connections

"""
class WarcOutputSingleton(object):
    _instance = None

    def __new__(cls, * args, **kwargs):
        if not cls._instance:
            cls._instance = super(WarcOutputSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, filename=None):
        self.use_gzip = True
        self.filename = "out.warc.gz"
        if filename is not None:
            self.filename = filename

        # Make sure init is not called more than once
        try:
            self.__fo
        except AttributeError:
            self.__fo = open(self.filename, 'wb')
            record = warcrecords.WarcinfoRecord()
            record.write_to(self.__fo, gzip=self.use_gzip)

    # Write a given record to the output file
    def write_record(self, record):
        record.write_to(self.__fo, gzip=self.use_gzip)

class Warc_HTTPConnection(_HTTPConnection, object):
    def fake_write(self, data):
        self._block_string += data
        self._real_write(data)

    """
    This method rewrites the self.stream.write method to point to the fake_write
    Then it calls the parent class's _on_connect which writes to stream.write
    
    """
    def _on_connect(self, *args, **kwargs):
        self._block_string = ""
        self._real_write = self.stream.write
        self.stream.write = self.fake_write

        super(Warc_HTTPConnection, self)._on_connect(*args, **kwargs)

        record = warcrecords.WarcRequestRecord(url=self.request.url, block=self._block_string)
        WarcOutputSingleton().write_record(record)

        self.stream.write = self._real_write

    def _on_headers(self, data):
        self._block_string = data
        super(Warc_HTTPConnection, self)._on_headers(data)

    def _on_body(self, data):
        # If data was not chunked, append it
        if self.chunks is None:
            self._block_string += data
        record = warcrecords.WarcResponseRecord(url=self.request.url,
                                                block=self._block_string)
        WarcOutputSingleton().write_record(record)

        super(Warc_HTTPConnection, self)._on_body(data)

    def _on_chunk_length(self, data):
        self._block_string += data
        super(Warc_HTTPConnection, self)._on_chunk_length(data)

    def _on_chunk_data(self, data):
        self._block_string += data
        super(Warc_HTTPConnection, self)._on_chunk_data(data)

class WarcSimpleAsyncHTTPClient(SimpleAsyncHTTPClient):
    def _handle_request(self, request, release_callback, final_callback):
        Warc_HTTPConnection(self.io_loop, self, request, release_callback,
                        final_callback, self.max_buffer_size, self.resolver)
