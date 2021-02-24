
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# pybtreecore - B-Tree (core persistence)

`pybtreecore` provides core B-Tree methods for persisting in a `heapfile` / `dllfile`.


# memory / file layout

a list of B-Tree element nodes resides inside a dllfile, and heap node as data part. 
see also 
[`pydllfile`](https://github.com/kr-g/pydllfile/), and
[`pyheapfile`](https://github.com/kr-g/pyheapfile/) 
for layout.


## general node layout

### BTree node 

| name | size / value | description |
| --- | --- | --- | 
| flags| 1 | boolean bit flags to indicate leaf (1<<0) |
| len_high | 1 | key and data len high nibbles combined |
| key_len_low | 1 | key len low byte (2 nibbles) |
| data_len_low | 1 | data len low byte (2 nibbles) |
| key | k bytes | key value |
| data | d bytes | data value, this exists only the leaf == True |
| left | xpos bytes | left node pointer, this exists only if leaf == False |
| right | xpos bytes | right node pointer, this exists only if leaf == False |

a list of nodes is stored as continuously stream of bytes inside a heap node.


### BTree node list  

| name | size / value | description |
| --- | --- | --- | 
| parent | xpos bytes | parent node pointer |
| stream| n bytes | stream of btcore nodes |


## limitation

- see other limits also here [`pydllfile`](https://github.com/kr-g/pydllfile/)
- see other limits also here [`pyheapfile`](https://github.com/kr-g/pyheapfile/)
- key and data field len is limited to 12 bits (3 nibbles) 2**12 == 4096 bytes max len
- 

# Platform

Tested on Python3, and Linux.


# development status

alpha state.
the API or logical call flow might change without prior notice.

read [`CHANGELOG`](https://github.com/kr-g/pybpvtree/blob/main/CHANGELOG.MD)
for latest, or upcoming news.


# installation
    
available on pypi. install with:

    python3 -m pip install pybpvtree
    
