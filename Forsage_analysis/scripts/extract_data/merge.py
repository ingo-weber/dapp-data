#Merge 2 TXs dumps without duplicates

import sys;

#merge.py <TXs normal file source> <TXs normal destination> <TXs internal file source> <TXs internal file destination>
file_name_source_normal = sys.argv[1]
file_name_destnation_normal = sys.argv[2]
file_name_source_internal = sys.argv[3]
file_name_destnation_internal = sys.argv[4]

tx_hash_normal = {}
tx_hash_internal = {}

#Normal TXs
fd_destination_normal =  open(file_name_destnation_normal, 'a+')

#Load TX hash in destination file
first_line = True
for line in fd_destination_normal:
    if first_line:
        first_line = False
        continue
    
    [blockNo, timeStamp, hash, nonce, fromAdd, toAdd, value, gas, gasUsed, gasPrice, isError, input] = line.split(',')
    assert(hash not in tx_hash_normal), 'Duplicate TX hash'
    tx_hash_normal[hash] = None

#Load TXs from source file
fd_source_normal =  open(file_name_source_normal, 'r')

first_line = True
for line in fd_source_normal:
    if first_line:
        first_line = False
        continue
    
    [blockNo, timeStamp, hash, nonce, fromAdd, toAdd, value, gas, gasUsed, gasPrice, isError, input] = line.split(',')

    if hash not in tx_hash_normal:
        fd_destination_normal.write(line)

fd_source_normal.close()
fd_destination_normal.close()


#Internal TXs
fd_destination_internal =  open(file_name_destnation_internal, 'a+')

#Load TX hash in destination file
first_line = True
for line in fd_destination_internal:
    if first_line:
        first_line = False
        continue
    
    [blockNo, timeStamp, hash, fromAdd, toAdd, value, gas, gasUsed, isError, input] = line.split(',')
    assert((hash not in tx_hash_internal) or (tx_hash_internal[hash] != toAdd)), 'Duplicate TX hash'
    tx_hash_internal[hash] = toAdd

#Load TXs from source file
fd_source_internal =  open(file_name_source_internal, 'r')

first_line = True
for line in fd_source_internal:
    if first_line:
        first_line = False
        continue
    
    [blockNo, timeStamp, hash, fromAdd, toAdd, value, gas, gasUsed, isError, input] = line.split(',')

    if (hash not in tx_hash_internal) or (tx_hash_internal[hash] != toAdd):
        fd_destination_internal.write(line)

fd_source_internal.close()
fd_destination_internal.close()