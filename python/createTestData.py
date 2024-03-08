#!/usr/bin/env python3
#
import math
import crc32c
import array
import json
array.array('i')
from simplemseed import MSeed3Header, MSeed3Record
import struct
output_file = 'output.ms3'


def crcAsHex(crc):
    return "0x{:08X}".format(crc)

eh = {
    "bag": {
        "y": {
            "proc": "raw",
            "si": "count"
        },
        "ch": {
            "la": 34.65,
            "lo": -80.46
        },
        "ev": {
            "or": {
                "tm": "2024-02-06T11:30:03Z",
                "la": 34.17,
                "lo": -80.70,
                "dp": 1.68,
            },
            "mag": {
                "v": 1.74,
                "t": "md"
            }
        },
        "mark": [
            {
                "tm": "2024-02-06T11:39:98Z",
                "n": "p",
                "mtype": "md"
            }
        ]
    }
}


data = array.array('i',( (i%99-49) for i in range(0,1000)))
header = MSeed3Header()
header.starttime = "2024-01-01T15:13:55.123456Z"
identifier = "FDSN:XX_FAKE__H_H_Z"
header.sampleRatePeriod = 40
record = MSeed3Record(header, identifier, data, extraHeaders=eh)
recordBytes = record.pack()

with open("testeh.ms3", "wb") as of:
    of.write(record.pack())

print(record.details())
