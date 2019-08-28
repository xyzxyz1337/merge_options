MERGE_OPTIONS
=====
This script merge two files with options in the format: option=value.
If you need script for python version 2, switch branch to python2.
Usage
====
```
$ python3 merge_option.py prod.txt -c dev.txt 
```
This command take options from prod.txt and print options which not in prod.txt. 
This is do with *difference mode* by default. 

The script have two mode: *difference* and *concatenate*. To understand a difference between him, take two files: prod.txt and dev.txt.

```
$ cat prod.txt

java.mem=16g
java.nonheapmem=1g
clustermode=true
```
```
$ cat dev.txt

java.mem=20g
clustermode=true
cluster.name=java_cluster
```

Difference
===
```
$ python3 merge_option.py prod.txt -c dev.txt --mode difference

cluster.name=java_cluster
```

Why java.mem not in output? Because this filed exist in prod file. Difference not overwrite options.

Concatenate
===
```
$ python3 merge_option.py prod.txt -c dev.txt --mode concatenate

cluster.name=java_cluster
clustermode=true
java.mem=20g
java.nonheapmem=1g
```

So look this we lose a sequence, but all options was merged.
