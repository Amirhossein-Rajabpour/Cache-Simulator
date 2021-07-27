# Cache Simulator
**Computer Architecture project**

This project is a cache simulator with LRU replacement policy.

**It takes input in the following format:**

```
<block size> - <architecture> - <associativity> - <write hit policy> - <write miss policy>
<cache(s) size>
<request type> <address> <optional description - will be ignored>
```
`<block size>`: Should be in power of 2<br>
`<architecture>`: 0 for von Neumann (unified I-D cache) - 1 for Harvard (split I-D cache)<br>
`<associativity>`: Should be in power of 2<br>
`<write hit policy>`: wt for Write Through - wb for Write Back<br>
`<write miss policy>`: wa for Write Allocate - nw for No Write Allocate (Write Around)<br>
`<cache(s) size>`: Should be in power of 2. Separated by - in case of Harvard architecture<br>

`<request type>`:
<table>
<thead>
  <tr>
    <th>type</th>
    <th>description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>0</td>
    <td>data read request</td>
  </tr>
  <tr>
    <td>1</td>
    <td>data write request</td>
  </tr>
  <tr>
    <td>2</td>
    <td>instruction read request</td>
  </tr>
</tbody>
</table>

## Sample input
```text
16 - 0 - 1 - wb - wa
256
0 00000 data read miss (compulsory)
0 00001 data read hit (same cache block as 00000 for block size >=2)
0 00002 data read hit (same cache block as 00000 for block size >=4)
0 00003 data read hit (same cache block as 00000 for block size >=4)
0 00004 data read hit (same cache block as 00000 for block size >=8)
0 00005 data read hit (same cache block as 00000 for block size >=8)
0 00006 data read hit (same cache block as 00000 for block size >=8)
0 00007 data read hit (same cache block as 00000 for block size >=8)
0 00008 data read hit (same cache block as 00000 for block size >=16)
0 0000a data read hit (same cache block as 00000 for block size >=16)
0 0000b data read hit (same cache block as 00000 for block size >=16)
0 0000c data read hit (same cache block as 00000 for block size >=16)
0 0000d data read hit (same cache block as 00000 for block size >=16)
0 0000e data read hit (same cache block as 00000 for block size >=16)
0 0000f data read hit (same cache block as 00000 for block size >=16)
0 00010 data read miss (compulsory, next cache block for block size 16)
0 00011 data read hit (same cache block as 00010 for block size >=2)
0 00012 data read hit (same cache block as 00000 for block size >=4)
0 00013 data read hit (same cache block as 00000 for block size >=4)
0 00014 data read hit (same cache block as 00000 for block size >=8)
0 00018 data read hit (same cache block as 00000 for block size >=16)
0 0001f data read hit (same cache block as 00000 for block size >=16)
```
## Sample output
```text
***CACHE SETTINGS***
Unified I- D-cache
Size: 256
Associativity: 1
Block size: 16
Write policy: WRITE BACK
Allocation policy: WRITE ALLOCATE

***CACHE STATISTICS***
INSTRUCTIONS
accesses: 0
misses: 0
miss rate: 0.0000 (hit rate 0.0000)
replace: 0
DATA
accesses: 22
misses: 2
miss rate: 0.0909 (hit rate 0.9091)
replace: 0
TRAFFIC (in words)
demand fetch: 8
copies back: 0
```

Full description [here](https://github.com/amirhoseinRj/Cache_simulator/blob/master/Cache.pdf).

