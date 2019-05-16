# magickMARCer

Scripts to help us move filemaker (csv) bibliographic data into MARC for batch loading into our OPAC. This is for a specific collection of sound recordings, but I hope to be able to modify it for any collection of very similar material that we can get a CSV of bibliographic data about.

The input data is expected to be a custom CSV exported from FileMaker (well, it could be any source) that is nicely massaged by OpenRefine (details to come on that process). The mapping is defined in a dictionary in `MARCmapper.py`, as is the collection-specific details that populate various fields, along with some fields that apply to all the records in thes collection. My thought currently is that if I need to adapt it for a different collection, I can just rewrite the hyper-specific functions and obv. redo the mapping.

`fields.py` has some very generic classes defining Data Fields, Subfields, and Fixed Field data. The base `Record` class is also very generic, though it includes a dictionary where you can define collection-specific details like format and so on.

The output JSON data structure is inspired by the [MARC-in-JSON](https://github.com/marc4j/marc4j/wiki/MARC-in-JSON-Description) spec  that seemed reasonable (and that seems abandoned?) with some modifications. This will be fed into MARCEdit to generate a MARC collection file we can provide to the campus library systems office for batch loading to our OPAC.
