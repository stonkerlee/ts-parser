'''
Created on Aug 15, 2013

Version1: function-based implementation.
Only can parse 188bytes ts stream.
'''

TS_PACKET_SIZE = 188

CODEC_TO_STRING = {
    0x03:'MPEG1 Audio', 
    0x04:'MPEG2 Audio',
    0x0f:'AAC',
    0x11:'AAC LATM',
    0x1b:'H264',
    0x81:'AC3',
    0x8a:'DTS',
    0xea:'VC1',
}

pid_of_pmt = -1

def ts_stream_from_file(filename, length=1024):
    """Return a ts stream of type of bytearray."""
    with open(filename, 'rb') as f:
        return bytearray(f.read(length))


def split_to_packets(ts_stream):
    ts_packets = []
    index_of_1st_packet = ts_stream.find(chr(0x47))
    for i in xrange(len(ts_stream)/TS_PACKET_SIZE):
        ts_packets.append(ts_stream[i*TS_PACKET_SIZE:(i+1)*TS_PACKET_SIZE])
    return ts_packets


def get_pid_of_ts_packet(ts_packet):
    return ((ts_packet[1] & 0x1F) << 8) | ts_packet[2]
    

def get_pid_of_pmt(pat_packet):
#     program_num = (pat_packet[13] << 8) | pat_packet[14]
#     print '  program_num -> %d' % program_num
    return ((pat_packet[15] & 0x1F) << 8) | pat_packet[16]


def parse_pmt(pmt_packet):
    """Print stream type and pid of elementary streams."""
    section_length = ((pmt_packet[6] & 0x0F) << 8 ) | pmt_packet[7]
#     print '  section_length -> %d' % section_length
    num_of_es = (section_length - 4 - 9) / 5
#     print '  num_of_es -> %d' % num_of_es
    
    pos = 17
    for i in xrange(num_of_es):
        stream_type = pmt_packet[pos]
        pid = (pmt_packet[pos+1] & 0x1F) << 8 | pmt_packet[pos+2]
        print '  stream_type: %x(%s), pid: %d' % (stream_type, CODEC_TO_STRING.get(stream_type), pid)
        pos += 5
    

if __name__ == '__main__':
    ts_stream = ts_stream_from_file('xh.ts')
    ts_packets = split_to_packets(ts_stream)
    for p in ts_packets:
        pid = get_pid_of_ts_packet(p)
        if pid == 0: # This is PAT
            pid_of_pmt = get_pid_of_pmt(p)
        elif pid == pid_of_pmt:
            parse_pmt(p)

