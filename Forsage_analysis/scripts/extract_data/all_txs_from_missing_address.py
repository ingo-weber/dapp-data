import requests;
import csv;
import json;
import time;

file_addresses = 'num_txs.csv' #'accounts_and_events_restructured.csv'
file_txs_normal = 'txs_normal.csv'
file_txs_internal = 'txs_internal.csv'
file_status = 'status.csv'
block_num_start = 9913531
block_num_end = 12243908
block_num_increment = 499
start_idx = 1
end_idx = 14083
both_normal_and_internal_missing_only = False
api_key='ADD Etherscan.io API KEY HERE'param_api_key = '&sort=asc&apikey=' + api_key

fd_out_normal = open(file_txs_normal, 'w')
fd_out_internal = open(file_txs_internal, 'w')
fd_status = open(file_status, 'w')
write_csv_normal = csv.writer(fd_out_normal)
write_csv_internal = csv.writer(fd_out_internal)

start_time = time.perf_counter()
next_address_count = 0

header_normal = ['blockNumber', 'timeStamp', 'hash', 'nonce', 'from', 'to', 'value', 'gas', 'gasUsed', 'gasPrice', 'isError', 'input']
header_internal = ['blockNumber', 'timeStamp', 'hash', 'from', 'to', 'value', 'gas', 'gasUsed', 'isError', 'input']
write_csv_normal.writerow(header_normal)
write_csv_internal.writerow(header_internal)

with open(file_addresses, mode="r") as fd_in: 
    reader = csv.reader(fd_in)
    next(reader) #Skip header
    for item in reader:
        next_address_count += 1
        if next_address_count < start_idx:
            continue
        if next_address_count > end_idx:
            break

        address = item[0]
        get_normal_tx = False
        get_internal_tx = False
        num_normal = 0
        num_internal = 0
        
        # if both_normal_and_internal_missing_only:
        #     if item[1] == '1' and item[2] == '1':
        #         get_normal_tx = True
        #         get_internal_tx = True
        # else:        
        #     if item[1] == '1':
        #         get_normal_tx = True
        #     if item[2] == '1' or item[2] == '1':
        #         get_internal_tx = True

        if both_normal_and_internal_missing_only:
            if item[2] == '0' and item[4] == '0' and item[5] == 'False' and item[6] == 'False':
                get_normal_tx = True
                get_internal_tx = True
        else:        
            if item[2] == '0' and item[5] == 'False':
                get_normal_tx = True
            if item[4] == '0' and item[6] == 'False':
                get_internal_tx = True

        block_num_next_start = block_num_start
        while block_num_next_start <= block_num_end:
            block_num_next_end = block_num_next_start + block_num_increment
            if block_num_next_end > block_num_end:
                block_num_next_end = block_num_end
            
            start_block = str(block_num_next_start)
            end_block = str(block_num_next_end)
            print(start_block + '\t' + end_block)

            #Normal TXs            
            if get_normal_tx:
                url_normal = 'https://api.etherscan.io/api?module=account&action=txlist&address=' \
                    + address + '&startblock=' + start_block + '&endblock=' + end_block + param_api_key
                #print(url_normal)
                resp_normal = requests.get(url=url_normal)
                data_normal = resp_normal.json()
                
                for r in data_normal["result"]:
                    tx_data_normal = [r["blockNumber"], r["timeStamp"], r["hash"], r["nonce"], r["from"], r["to"], r["value"], r["gas"], r["gasUsed"], r["gasPrice"], r["isError"], r["input"]]
                    write_csv_normal.writerow(tx_data_normal)
                num_normal = len(data_normal["result"])

                block_num_next_start += (block_num_increment + 1)

            #Internal TXs
            if get_internal_tx:
                url_internal = 'https://api.etherscan.io/api?module=account&action=txlistinternal&address=' \
                    + address + '&startblock=' + start_block + '&endblock=' + end_block + param_api_key
                #print(url_internal)
                resp_internal = requests.get(url=url_internal)
                data_internal = resp_internal.json()

                for r in data_internal["result"]:
                    tx_data_internal = [r["blockNumber"], r["timeStamp"], r["hash"], r["from"], r["to"], r["value"], r["gas"], r["gasUsed"], r["isError"], r["input"]]
                    write_csv_internal.writerow(tx_data_internal)
                num_internal = len(data_internal["result"])

            block_num_next_start += (block_num_increment + 1)

        if get_normal_tx or get_internal_tx:
            fd_status.write(address + ',' + str(get_normal_tx) + ',' + str(num_normal) + ',' + str(get_internal_tx) + ',' + str(num_internal) + '\n')
        
        elapsed_time = time.perf_counter() - start_time
        print(next_address_count, elapsed_time, elapsed_time/(next_address_count - start_idx + 1))

fd_in.close()
fd_out_normal.close()
fd_out_internal.close()
fd_status.close()