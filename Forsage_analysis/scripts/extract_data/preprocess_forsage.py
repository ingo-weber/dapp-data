import sys

tx_limit = 10000
forsage_address = '0x5acc84a3e955bdd76467d3348077d003f00ffb97'

#preprocess.py <address file> <status file> <TXs normal file> <TXs internal file>
file_name_addresses = sys.argv[1]
file_name_status = sys.argv[2]
file_name_txs_normal = sys.argv[3]
file_name_txs_internal = sys.argv[4]
file_name_txs_normal_cleaned = file_name_txs_normal[:-4] + '_cleaned.csv'
file_name_txs_internal_cleaned = file_name_txs_internal[:-4] + '_cleaned.csv'
file_name_num_txs = 'num_txs.csv'

fd_status = open(file_name_status, 'r')
for line in fd_status:
    [start_block, end_block, num_normal, num_internal] = line.split(',')
    if int(num_normal) == tx_limit or int(num_internal) == tx_limit:
        print(line)
fd_status.close()

#Read list of addresses to check
fd_addresses =  open(file_name_addresses, 'r')

first_line = True
addresses = {}
num_address = 0
for line in fd_addresses:
    if first_line:  #Skip header
        first_line = False
        continue
    
    [users, no_events] = line.split(',')
    addresses[users] = [0, 0]
    num_address += 1
print('No of addresses read', num_address)
fd_addresses.close()

#Preprocess normal TXs
fd_txs_normal = open(file_name_txs_normal, 'r')
fd_txs_normal_cleaned = open(file_name_txs_normal_cleaned, 'w')

first_line = True

for line in fd_txs_normal:
    if first_line:  #Header
        fd_txs_normal_cleaned.write(line)
        first_line = False
        continue
    [blockNo, timeStamp, hash, nonce, fromAdd, toAdd, value, gas, gasUsed, gasPrice, isError, input] = line.split(',')

    if toAdd != forsage_address and toAdd in addresses:
        fd_txs_normal_cleaned.write(line)
        addresses[toAdd][0] += 1

    if fromAdd != forsage_address and fromAdd in addresses:
        fd_txs_normal_cleaned.write(line)
        addresses[fromAdd][0] += 1
 
fd_txs_normal.close()
fd_txs_normal_cleaned.close()

#Preprocess internal TXs
fd_txs_internal = open(file_name_txs_internal, 'r')
fd_txs_internal_cleaned = open(file_name_txs_internal_cleaned, 'w')

first_line = True
for line in fd_txs_internal:
    if first_line:  #Header
        fd_txs_internal_cleaned.write(line)
        first_line = False
        continue
    [blockNo, timeStamp, hash, fromAdd, toAdd, value, gas, gasUsed, isError, input] = line.split(',')

    if toAdd != forsage_address and toAdd in addresses:
        fd_txs_internal_cleaned.write(line)
        addresses[toAdd][1] += 1

    if fromAdd != forsage_address and fromAdd in addresses:
        fd_txs_internal_cleaned.write(line)
        addresses[fromAdd][1] += 1
            
fd_txs_internal.close()
fd_txs_internal_cleaned.close()

#No of TXs for each address
fd_num_txs = open(file_name_num_txs, 'w')
fd_num_txs.write('address,normal_forsage,internal_forsage\n')

for a in addresses:
    num_txs_str = a + ',' + str(addresses[a][0]) + ',' + str(addresses[a][1]) + '\n'
    fd_num_txs.write(num_txs_str)

fd_num_txs.close()
