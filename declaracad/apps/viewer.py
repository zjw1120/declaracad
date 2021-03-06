"""
Copyright (c) 2018, Jairus Martin.

Distributed under the terms of the GPL v3 License.

The full license is in the file LICENSE, distributed with this software.

Created on July 28, 2018

@author: jrm
"""
import sys
import json
import traceback
import qt5reactor

import faulthandler
faulthandler.enable()

from declaracad import occ
occ.install()
from declaracad.core.utils import JSONRRCProtocol

import enaml
from enaml.qt.qt_application import QtApplication
from enaml.application import timed_call
with enaml.imports():
    from declaracad.occ.view import ViewerWindow

from twisted.internet.stdio import StandardIO


class ViewerProtocol(JSONRRCProtocol):
    """ Use stdio as a json-rpc interface to communicate with external
    processes.
    
    """
    def __init__(self, view):
        self.view = view
        self._exit_in_sec = 60
        super(ViewerProtocol).__init__()
        
    def connectionMade(self):
        self.send_message({'result': self.handle_window_id(),
                           'id': 'window_id'})
        if self.view.frameless:
            self.schedule_close()
        
    def handle_window_id(self):
        return int(self.view.proxy.widget.winId())
        
    def handle_filename(self, filename):
        self.view.filename = filename
    
    def handle_version(self, version):
        self.view.version = version
        
    def handle_ping(self):
        self._exit_in_sec = 60
        return True
        
    def __getattr__(self, name):
        """ The JSONRRCProtocol tries to invoke 'handle_<attr>' on this class
        to handle JSON-RPC requests. This is invoked if such a method doesn't 
        exist and attempts to redirect the getattr to the window or viewer.
        
        """
        if not name.startswith('handle_'):
            raise AttributeError(name)
        attr = name[len('handle_'):]  # Strip handle_
        
        # Lookup matching methods on the window and viewer
        for target in (self.view, self.view.viewer):
            handler = getattr(target, attr, None)
            if handler is not None and callable(handler):
                return handler
        
        # Replace any set_<attr> with a setattr 
        if attr.startswith('set_'):
            attr = attr[len('set_'):]
            for target in (self.view, self.view.viewer):
                handler = getattr(target, attr, None)
                if handler is not None and not callable(handler):
                    return lambda v: setattr(target, attr, v)
        raise AttributeError(name)
        
    def schedule_close(self):
        """ A watchdog so if the parent is killed the viewer will automatically
        exit. Otherwise it will hang around forever.
        """
        if self._exit_in_sec <= 0:
            # Timeout
            print("WARNING: Ping timeout expired, closing")
            sys.exit(1)
        else:
            timed_call(self._exit_in_sec*1000, self.schedule_close)
            self._exit_in_sec = 0  # Clear timeout
    

def main(**kwargs):
    app = QtApplication()
    qt5reactor.install()
    view = ViewerWindow(filename=kwargs.get('file', '-'),
                        frameless=kwargs.get('frameless', False))
    view.protocol = ViewerProtocol(view)
    view.show()
    app.deferred_call(lambda: StandardIO(view.protocol))
    app.start()
    
    
if __name__ == '__main__':
    main()
