#!/usr/bin/env python3
#
import math
import crc32c
import array
import json
array.array('i')
from simpledali import MSeed3Header, Mseed3Record
import simpledali
import struct
output_file = 'output.mseed'


def crcAsHex(crc):
    return "0x{:08X}".format(crc)

eh = {
        "bag": {
            "y": {
                "proc": "raw",
                "si": "count"
            },
            "st": {
                "la": 34.65,
                "lo": -80.46
           },
           "ev": {
               "origin": {
                   "time": "2024-02-06T11:30:03Z",
                   "la": 34.17,
                   "lo": -80.70,
                   "dp": 1.68,
               },
               "mag": {
                   "val": 1.74,
                   "type": "md"
               }
            }
        }
    }
ehStr = json.dumps(eh)


data = array.array('i',( (i%99-49) for i in range(0,1000)))
data = array.array('i',( (77) for i in range(0,10)))
#data = [(i%99-49) for i in range(0,1000)]
header = simpledali.MSeed3Header()
header.starttime = "2024-01-01T15:13:55.123456Z"
header.identifier = "FDSN:XX_FAKE__H_H_Z"
header.encoding = simpledali.seedcodec.INTEGER
header.sampleRatePeriod = 40
header.numSamples = len(data)
header.extraHeadersStr = ehStr
encodedData = simpledali.compress(header.encoding, data).dataView
header.dataLength = len(encodedData)
record = simpledali.Mseed3Record(header, encodedData)
recordBytes = record.pack()

(head_crc,) = struct.unpack("<I", recordBytes[simpledali.CRC_OFFSET:simpledali.CRC_OFFSET+4])
struct.pack_into("<I", recordBytes, simpledali.CRC_OFFSET, 0);
crc = crc32c.crc32c(recordBytes)
print(f"crc: head: {crcAsHex(header.crc)}  extract: {crcAsHex(head_crc)} calc: {crcAsHex(crc)}")
struct.pack_into("<I", recordBytes, simpledali.CRC_OFFSET, crc);


outRecord = simpledali.unpackMSeed3Record(recordBytes)
decomp_data = outRecord.decompress()
assert len(decomp_data) == len(data)


with open("testeh.ms3", "wb") as of:
    of.write(record.pack())

print(record)

with open("testeh.ms3", "rb") as infile:
    rec_bytes = infile.read()
    rec = simpledali.mseed3.unpackMSeed3Record(rec_bytes)
    print(f"testeh rec.crc: {crcAsHex(rec.header.crc)}")
    recordBytes = bytearray(rec_bytes)
    (head_crc,) = struct.unpack("<I", recordBytes[simpledali.CRC_OFFSET:simpledali.CRC_OFFSET+4])
    struct.pack_into("<I", recordBytes, simpledali.CRC_OFFSET, 0);
    crc = crc32c.crc32c(recordBytes)
    print(f"testeh crc: head: {crcAsHex(rec.header.crc)} ")
    print(f"  extract: {crcAsHex(head_crc)} ")
    print(f"   calc: {crcAsHex(crc)}  {crc}")

    with open("testeh_nocrc.ms3", "wb") as of:
        of.write(recordBytes)

if False:
    with open("reference-sinusoid-FDSN-Other.mseed3", "rb") as infile:
        rec_bytes = infile.read()
        recordBytes = bytearray(rec_bytes)
        rec = simpledali.mseed3.unpackMSeed3Record(rec_bytes)
        (head_crc,) = struct.unpack("<I", recordBytes[simpledali.CRC_OFFSET:simpledali.CRC_OFFSET+4])
        struct.pack_into("<I", recordBytes, simpledali.CRC_OFFSET, 0);
        crc = crc32c.crc32c(recordBytes)
        print(f"refdata crc: head: {crcAsHex(rec.header.crc)} ")
        print(f"  extract: {crcAsHex(head_crc)} ")
        print(f"   calc: {crcAsHex(crc)}")
        print(f"refdata crc: head: {crcAsHex(rec.header.crc)}  extract: {crcAsHex(head_crc)} calc: {crcAsHex(crc)}")
        with open("reference.mseed3_roundtrip", "wb") as outfile:
            rec.header.crc = 0

            outfile.write(rec.pack())
            recordBytes = bytearray(rec.pack())
