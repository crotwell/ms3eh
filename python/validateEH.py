#!/usr/bin/env python3

import argparse
from simpledali import MSeed3Header, Mseed3Record
import simpledali
import json
import jsonschema
import os
from referencing import Registry, Resource
import referencing.jsonschema
#from referencing.jsonschema import DRAFT2020212

def loadSchema(schemafilename, registry):
    with open(schemafilename, "r") as inschema:
        s = json.load(inschema)
        schema = Resource.from_contents(s)
        return schema @ registry

def validate(ms3filename, ehschema, registry):
    with open(ms3filename, "rb") as infile:
        rec = simpledali.mseed3.nextMSeed3Record(infile)
        print(rec.eh)
        jsonschema.validate(instance=rec.eh, schema=ehschema, registry=registry)
        print("Got miniseed3 record")

def do_parseargs():
    parser = argparse.ArgumentParser(
        description=f"Validte ms3 extra headers"
    )
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    parser.add_argument(
        "--version", help="print version", action="store_true"
    )
    parser.add_argument(
        "-f",
        "--file",
        required=True,
        help="miniseed3 file to parse",
    )
    parser.add_argument(
        "-s",
        "--schema",
        action='append',
        required=False,
        help="register JSON Schema file",
    )
    return parser.parse_args()


def main():
    args = do_parseargs()
    if args.version:
        print(__version__)
        return
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    registry = Registry()
    with open("../schema/ms3extraheaders.schema.json", "r") as ms3ehschemaIn:
        schema = json.load(ms3ehschemaIn)
    for sfile in args.schema:
        if not os.path.exists(sfile):
            print(f"File {sfile} does not seem to exist, cowardly quitting...")
            return
        registry = loadSchema(sfile, registry)
    validator = jsonschema.validators.Draft202012Validator(schema, registry=registry)
    validate(args.file, schema, registry)
    print("done")

if __name__ == "__main__":
    main()
