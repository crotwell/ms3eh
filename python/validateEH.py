#!/usr/bin/env python3

import argparse
from simplemseed import MSeed3Header, MSeed3Record
import simplemseed
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
        for rec in simplemseed.mseed3.readMSeed3Records(infile):
            if rec.eh is not None and len(rec.eh) > 0:
                print(json.dumps(rec.eh, indent=2) )
                jsonschema.validate(instance=rec.eh, schema=ehschema, registry=registry)
                print("Got valid miniseed3 eh in record")
            else:
                print("Got miniseed3 record with no eh")

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
    schemaFiles = [ "../schema/ms3extraheaders.schema.json",
                   "../schema/bag.schema.json"
                   ]
    if args.schema is not None:
        schemaFiles = schemaFiles + args.schema
    for sfile in schemaFiles:
        if not os.path.exists(sfile):
            print(f"File {sfile} does not seem to exist, cowardly quitting...")
            return
        registry = loadSchema(sfile, registry)
    validator = jsonschema.validators.Draft202012Validator(schema, registry=registry)
    validate(args.file, schema, registry)
    print("done")

if __name__ == "__main__":
    main()
