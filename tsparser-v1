'''
Created on Aug 15, 2013

Version1: function-based implementation.
Only can parse 188bytes ts stream.
'''

NUM_OF_PACKETS = 100
pid_of_pmt = -1
CODEC_TO_STRING = {0x1b:'AVC', 0x0f:'AAC', 0x03:'MPEG Audio', 0x04:'MPEG Audio'}

def bytearray_from_file(filename, length=2*1024*1024):
    """Construct a bytearray from filename."""
    return bytearray(open(filename, 'rb').read(length))


def parse_ts_header(header):
    """Return pid."""
    pid = ((header[1] & 0x1F) << 8) | header[2]
    print 'pid -> %d' % pid
    return pid


def parse_pat(pat_packet):
    """Return pid of pmt."""
    bytearray_of_program_num = pat_packet[13:15] # 13th,14th bytes of pat packet is program_num
    program_num = (bytearray_of_program_num[0] << 8) | bytearray_of_program_num[1]
    print '  program_num -> %d' % program_num
    bytearray_of_program_pid = pat_packet[15:17]
    pid_of_pmt = ((bytearray_of_program_pid[0] & 0x1F) << 8) | bytearray_of_program_pid[1]
    print '  pid_of_pmt -> %d' % pid_of_pmt
    return pid_of_pmt


def parse_pmt(pmt_packet):
    """Print stream type and pid of elementary streams."""
    bytearray_of_section_length = pmt_packet[6:8]
    section_length = ((bytearray_of_section_length[0] & 0x0F) << 8 ) | bytearray_of_section_length[1]
#     print '  section_length -> %d' % section_length
    num_of_es = (section_length - 4 - 9) / 5
    print '  num_of_es -> %d' % num_of_es
    
    start_pos_of_es = 17
    for i in xrange(num_of_es):
        stream_type = pmt_packet[start_pos_of_es]
        pid_of_es = (pmt_packet[start_pos_of_es+1] & 0x1F) << 8 | pmt_packet[start_pos_of_es+2]
        print '  stream_type: %x(%s), pid: %d' % (stream_type, CODEC_TO_STRING.get(stream_type), pid_of_es)
        
        start_pos_of_es += 5
    

if __name__ == '__main__':
    bytearray_of_stream = bytearray_from_file('dblm.ts', 188*NUM_OF_PACKETS)
    
    start_pos = bytearray_of_stream.find(chr(0x47))
#     print 'start_pos -> %d' % start_pos

    for i in xrange(NUM_OF_PACKETS):
        ts_packet = bytearray_of_stream[start_pos:start_pos+188]
        pid = parse_ts_header(ts_packet[0:4])
        
        if pid == 0:  # This is PAT
            pid_of_pmt = parse_pat(ts_packet)
        elif pid == pid_of_pmt:
            parse_pmt(ts_packet)
        
        start_pos += 188
