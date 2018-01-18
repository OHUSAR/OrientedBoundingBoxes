import sys

LOG_BUFFER_LIMIT = 65535

class Logger:
    def __init__( self, stream = sys.stdout, bufferLimit = LOG_BUFFER_LIMIT ):
        self.stream = stream
        self._DEBUG = True

        self.buffer = []
        self.bufferLimit = bufferLimit
        
    def flush(self):
        if self._DEBUG:
            print( ''.join(self.buffer), file = self.stream )
        self.buffer = []
        
    def log( self, message, end = '\n' ):
        if ( len(self.buffer) + len(message) + 1 ) > self.bufferLimit:
            self.flush()
        
        self.buffer.extend( message )
        self.buffer.append( end )

    def setDebug( self, debug ):
        self._DEBUG = debug
        

# import this and use ( a.k.a. "from Core.Utils.Logger import LOGGER" )
LOGGER = Logger()
