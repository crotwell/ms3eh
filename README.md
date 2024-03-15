# ms3eh
Commonly needed "extras" stored in miniseed3 extra headers

This aims to define a common set of json keys for storing very simple, but very commonly needed values inside of a miniseed3 seismogram
using the extra headers. For example, if a seismogram is associated
with an event, having the event latitude, longitude, depth and a magnitude without having to parse a second file makes processing less cumbersome. Similar, knowing the latitude, longitude, depth, aziumth and dip of the recording channel helps.
Another very common need is to save and display time markers on seismograms, be they picks by the user or predicted arrival times based on a model. Knowing the units of the timeseries values allows proper display. The display needs to know if the timeseries is in counts, or has the gain been applied so the units are m/s.

A motivator for this is the SAC file format, that included header fields for these types of data, like the EVLA, STLA and the Tn headers. Miniseed3, with the flexibility of JSON, allows us to store similar information, but without a common structure and common keys, interoperability is difficult.

The current schema addresses these, and there is the possibility of future expansion to other important metadata and storage for common measurements made on the seismograms.

Overview:
- KISS principle (no deep object hierarchies)
- The root key is `bag`, like a sack of useful things (got a better name?)
- Small keys are preferred (space and easy typing vs legibility as text?)
- Not intended to duplicate all metadata from StationXML or QuakeML (see KISS above)

See also the standard [FDSN extra headers](http://docs.fdsn.org/projects/miniseed3/en/latest/extra-headers.html) for mapping miniseed2 blockettes to miniseed3.

# Schema

JSON-Schema file is [here](https://github.com/crotwell/ms3eh/blob/main/schema/bag.schema.json) and documentation can be viewed [here](https://github.com/crotwell/ms3eh/blob/main/docs/bag.schema.md).

# Typescript

Generate typescript types from schema for use in javascript with:
```
cd typescript ; npm run tots
```

See [seisplotjs](https://github.com/crotwell/seisplotjs) for javascript usage.

# Python

Create test data:
```
python createTestData.py
```

Validate records:
```
python validateEH.py -f testeh.ms3
```

Show extra headers, using mseed3details from [simplemseed](https://github.com/crotwell/simplemseed):
```
mseed3details --eh testeh.ms3
```
```
          FDSN:XX_FAKE__H_H_Z, version 0, 4322 bytes (format: 3)
                       start time: 2024-01-01T15:13:55.123456Z (001)
                number of samples: 1000
                 sample rate (Hz): 40.0
                            flags: [00000000] 8 bits
                              CRC: 0xEBE510DE
              extra header length: 263 bytes
              data payload length: 4000 bytes
                 payload encoding: 32-bit integer (val: 3)
                    extra headers: {
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
                  "lo": -80.7,
                  "dp": 1.68
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

Total 1000 samples in 1 records
```

See extra header handling in python in [simplemseed](https://github.com/crotwell/simplemseed).

# Java

See extra header handling in the [seisFile](https://github.com/crotwell/seisFile) project. Version 3.0 (not yet released), can use bag headers for travel time
calculations and set markers in miniseed3 files via `taup setmseed3`.


# Rebuild Schema docs
```
pip install json-schema-for-humans
generate-schema-doc --config template_name=md  schema docs
```
