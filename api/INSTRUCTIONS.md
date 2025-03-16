# Change instructions

Follow all of the instructions in this file exactly.

## Ticket 1

Refactor the FileSystemDatabase class in db.py to return actual FileModel objects instead of dictionaries of derived values. If you need to calculate derived data, put that on the file model class itself and call it where it is needed, including in a template. 

The FileSystemDatabase should primarily implement a wrapper around the file system model layer. it should not be doing any calculation