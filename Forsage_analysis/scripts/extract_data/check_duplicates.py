import sys

#check_duplicates.py <TXs normal file> <TXs internal file>
file_name_txs_normal = sys.argv[1]
file_name_txs_internal = sys.argv[2]

fd_txs_normal = open(file_name_txs_normal, 'r')
fd_txs_normal_clean = open(file_name_txs_normal[:-4] + '_cleaned.csv', 'w')
fd_txs_internal = open(file_name_txs_internal, 'r')
fd_txs_internal_clean = open(file_name_txs_internal[:-4] + '_cleaned.csv', 'w')

txs_normal = {}
first_line = True
num_duplicates_normal = 0
for line in fd_txs_normal:
    if first_line:
        first_line = False
        fd_txs_normal_clean.write(line)
        continue

    if line not in txs_normal:
        txs_normal[line] = None
        fd_txs_normal_clean.write(line)
    else:
        num_duplicates_normal += 1
fd_txs_normal.close()

txs_internal = {}
first_line = True
num_duplicates_internal = 0
for line in fd_txs_internal:
    if first_line:
        first_line = False
        fd_txs_internal_clean.write(line)
        continue

    if line not in txs_internal:
        txs_internal[line] = None
        fd_txs_internal_clean.write(line)
    else:
        num_duplicates_internal += 1
fd_txs_internal.close()

print(num_duplicates_normal, num_duplicates_internal)