import sys

forsage_address = '0x5acc84a3e955bdd76467d3348077d003f00ffb97'
tx_limit = 10000

#preprocess.py <start idx addresses> <end idx addresses> <address file> <TXs normal file> <TXs internal file>
start_idx = int(sys.argv[1])
end_idx = int(sys.argv[2])
file_name_addresses = sys.argv[3]
file_name_txs_normal = sys.argv[4]
file_name_txs_internal = sys.argv[5]
file_name_txs_normal_cleaned = file_name_txs_normal[:-4] + '_cleaned.csv'
file_name_txs_internal_cleaned = file_name_txs_internal[:-4] + '_cleaned.csv'
#file_name_no_txs = 'no_txs.csv'
file_name_num_txs = 'num_txs.csv'
file_name_too_many_txs = 'too_many_txs.csv'
#file_name_no_forsage_txs = 'no_forsage_txs.csv'
file_status = 'status_all.csv'

#Read addresses already downloaded
fd_status = open(file_status, 'r')
downloaded_addresses = {}

for line in fd_status:
    [address, normal_download, normal_txs, internal_download, internal_txs] = line.split(',')
    downloaded_addresses[address] = [normal_download, internal_download]

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
    
    num_address += 1
    if num_address < start_idx:
        continue
    if num_address > end_idx:
        print('No of addresses read', num_address - 1)
        break

    [users, no_events] = line.split(',')
    addresses[users] = [0, 0, 0, 0]

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

    if toAdd == forsage_address:
        fd_txs_normal_cleaned.write(line)
        addresses[fromAdd][1] += 1
    assert(fromAdd != forsage_address), "Forsage is sending a normal TX"

    if fromAdd in addresses:
        addresses[fromAdd][0] += 1
    #if toAdd in addresses:
    #    addresses[toAdd][0] += 1
 
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

    if fromAdd == forsage_address:
        fd_txs_internal_cleaned.write(line)
        addresses[toAdd][3] += 1
    assert(toAdd != forsage_address), "Forsage is receiving an internal TX" 
            
    #if fromAdd in addresses:
    #    addresses[fromAdd][2] += 1
    if toAdd in addresses:
        addresses[toAdd][2] += 1

fd_txs_internal.close()
fd_txs_internal_cleaned.close()

#Find addresses with missing TXs
#fd_no_txs = open(file_name_no_txs, 'w')
#fd_no_txs.write('address,missing_normal,missing_internal\n')
fd_num_txs = open(file_name_num_txs, 'w')
fd_num_txs.write('address,normal_total,normal_forsage,internal_total,internal_forsage,normal_downloaded,internal_downloaded\n')
fd_too_many_txs = open(file_name_too_many_txs, 'w')
fd_too_many_txs.write('address,too_many_normal,too_many_internal\n')
#fd_no_forsage_txs = open(file_name_no_forsage_txs, 'w')
#fd_no_forsage_txs.write('address,normal_total,normal_forsage,internal_total,internal_forsage\n')

max_tx_limit1 = 0
max_tx_limit2 = 0
max_tx_limit3 = 0
max_tx_limit4 = 0

for a in addresses:
    #Mark whether the address is alredy downloaded
    num_txs_str = a + ',' + str(addresses[a][0]) + ',' + str(addresses[a][1]) + ',' + str(addresses[a][2]) + ',' + str(addresses[a][3]) + ','
    if a in downloaded_addresses:
        num_txs_str += downloaded_addresses[a][0] + ',' + downloaded_addresses[a][1] + '\n'
    else:
        num_txs_str += 'False,False\n'
    
    fd_num_txs.write(num_txs_str)
    # result_str_no_txs = ','
    # should_write_no_txs = False

    # if addresses[a][0] == 0:
    #     result_str_no_txs += '1,'
    #     should_write_no_txs = True
    # else:
    #     result_str_no_txs += '0,'

    # if addresses[a][2] == 0:
    #     result_str_no_txs += '1\n'
    #     should_write_no_txs = True
    # else:
    #     result_str_no_txs += '0\n'
    
    # if should_write_no_txs:
    #     fd_no_txs.write(a + result_str_no_txs)

    result_str_max = ','
    should_write_max_txs = False
    if addresses[a][0] >= tx_limit:
        result_str_max += '1,'
        should_write_max_txs = True
    else:
        result_str_max += '0,'

    if addresses[a][2] >= tx_limit:
        result_str_max += '1\n'
        should_write_max_txs = True
    else:
        result_str_max += '0\n'

    if should_write_max_txs:
        fd_too_many_txs.write(a + result_str_max)
    
    if addresses[a][0] > max_tx_limit1:
        max_tx_limit1 = addresses[a][0]
    
    if addresses[a][1] > max_tx_limit2:
        max_tx_limit2 = addresses[a][1]

    if addresses[a][2] > max_tx_limit3:
        max_tx_limit3 = addresses[a][2]

    if addresses[a][3] > max_tx_limit4:
        max_tx_limit4 = addresses[a][3]
    
    #fd_no_forsage_txs.write(a + ',' + str(addresses[a][0]) + ',' + str(addresses[a][1]) + ',' + str(addresses[a][2]) + ',' + str(addresses[a][3]) + '\n')

print(max_tx_limit1, max_tx_limit2, max_tx_limit3, max_tx_limit4)
#fd_no_txs.close()
fd_num_txs.close()
fd_too_many_txs.close()
#fd_no_forsage_txs.close()
