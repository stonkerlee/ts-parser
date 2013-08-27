'''
Created on Aug 26, 2013

Version2: OOP implementation.
Only can parse 188bytes ts stream.
'''

class TSPacket():
    def __init__(self, bytes):
        self.ts_bytes = bytearray(bytes)
        self.pid = ((self.ts_bytes[1] & 0x1F) << 8) | self.ts_bytes[2]
        


class TSStream():
    def __init__(self, filename):
        self.ts_bytes = bytearray(open(filename, 'rb').read(2*1024))
        self.index_of_1st_packet = self.ts_bytes.find(chr(0x47))
        self.packets = []

    def splittopackets(self):
        for i in xrange(2*1024/188):
            index = self.index_of_1st_packet + 188*i
            p = TSPacket(self.ts_bytes[index:index+188])
            self.packets.append(p)
        return self.packets

    # should support indexing
    def __getitem__(self):
        pass


if __name__ == '__main__':
    ts_stream = TSStream('xh.ts')
    packets = ts_stream.splittopackets()
    for p in packets:
        print 'pid -> %d' % p.pid
    
