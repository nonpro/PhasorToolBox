#!/usr/bin/env python3

import sys
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from collections import defaultdict
from common import Common
from timeit import default_timer as timer
import cProfile


class Synchrphasor(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None, _cfg = None):  # Add cfg
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._cfg = _cfg
        self.message = []
        if not self._cfg:
            print('Try parsing without configuration frame.')
        while not self._io.is_eof():
            pkt = Common(self._io, _cfg = self._cfg)
            if pkt.sync.frame_type.name == 'configuration_frame_2':
                self._cfg = pkt.data
            self.message.append(pkt)


def parse_stream():
    file = open('/Users/s/Dropbox/SouceTree/PhasorToolBox/samples/stream.bin', 'rb')
    raw_data = file.read()
    stream = KaitaiStream(BytesIO(raw_data))
    t0 = timer()
    P = Synchrphasor(stream)
    t1 = timer()
    print('Time per message:', (t1 - t0)/len(P.message))

if __name__ == '__main__':
    cProfile.run('parse_stream()')
    #parse_stream()