# Rule_Dupe

This will find duplicate rules between two device groups based on the supplied xml configuration. 
This comparison is done based on the strings present in the match criteria of each rule. This means 
that there are unhandled cases:


1. Address objects and groups are compared based on name, not value.
2. No expansion of address groups is done.
3. No sub/super netting is performed for explicit source or destination IP addresses.
4. Probably others


## Prerequisits
1. Python 3
2. mmh3 (Python module - https://pypi.org/project/mmh3/)
3. bitarray (Python module - https://pypi.org/project/bitarray/)


## Usage

./dup_finder -t <target_DG> -d <donor_DG> -c <config_file>


Where Target DG is the device group you want  to merge into and Donor DG is the 
device group you merging from.

