# ms3eh

Commonly needed "extras" stored in miniseed3 extra headers

This aims to define a common set of json keys for storing very simple, but very commonly needed values inside of a miniseed3 seismogram
using the extra headers. For example, if a seismogram is associated
with an event, having the event latitude, longitude, depth and a magnitude without having to parse a second file makes processing less cumbersome. Similar, knowing the latitude, longitude, depth, azimuth and dip of the recording channel helps.

See the [documentation](https://crotwell.github.io/ms3eh) for details.


# Rebuild Schema docs, etc

```
pip install json-schema-for-humans
generate-schema-doc --config template_name=md  schema docs
generate-schema-doc --config template_name=js  schema docs/html
cd typescript && npm run tots && cd ..
```
