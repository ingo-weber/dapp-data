import sys

file_name_txs_normal = sys.argv[1]
file_name_txs_internal = sys.argv[2]

fd_txs_normal = open(file_name_txs_normal, 'r')
fd_txs_internal = open(file_name_txs_internal, 'r')
fd_txs_internal_gas_price= open(file_name_txs_internal[:-4] + '_gas_price.csv', 'w')

#Get gas price from normal TXs
gas_prices = {}
first_line = True
for line in fd_txs_normal:
    if first_line:  #Header
        first_line = False
        continue
    
    [blockNo, timeStamp, hash, nonce, fromAdd, toAdd, value, gas, gasUsed, gasPrice, isError, input] = line.split(',')
    gas_prices[hash] = [gasUsed, gasPrice]
fd_txs_normal.close()

fd_txs_internal_gas_price.write('hash,gasUsedNormal,gasUsedInternal,gasPriceNormal\n')
first_line = True
no_gas_price_num = 0
for line in fd_txs_internal:
    if first_line:  #Header
        first_line = False
        continue
    
    [blockNo, timeStamp, hash, fromAdd, toAdd, value, gas, gasUsed, isError, input] = line.split(',')
    if hash in gas_prices:
        fd_txs_internal_gas_price.write(hash + ',' + gas_prices[hash][0] + ',' + gasUsed + ',' + gas_prices[hash][1] + '\n')
    else:
        fd_txs_internal_gas_price.write(hash + ',None,' + gasUsed + ',None\n')
fd_txs_internal.close()
fd_txs_internal_gas_price.close()