import requests;
import csv;
import json;
import time;

file_txs_normal = 'txs_normal.csv'
file_txs_internal = 'txs_internal.csv'
file_status = 'status.csv'
block_num_start = 9913531
block_num_end = 12243908
#block_num_end = block_num_start + 200000
block_num_increment = 99
forsage_address = '0x5acc84a3e955bdd76467d3348077d003f00ffb97'
tx_limit = 10000
api_key='ADD Etherscan.io API KEY HERE'
param_api_key = '&sort=asc&apikey=' + api_key
url_part_normal ='https://api.etherscan.io/api?module=account&action=txlist&address=' + forsage_address + '&startblock=' 
url_part_internal ='https://api.etherscan.io/api?module=account&action=txlistinternal&address=' + forsage_address + '&startblock=' 

fd_out_normal = open(file_txs_normal, 'w')
fd_out_internal = open(file_txs_internal, 'w')
fd_status = open(file_status, 'w')
write_csv_normal = csv.writer(fd_out_normal)
write_csv_internal = csv.writer(fd_out_internal)

start_time = time.perf_counter()

header_normal = ['blockNumber', 'timeStamp', 'hash', 'nonce', 'from', 'to', 'value', 'gas', 'gasUsed', 'gasPrice', 'isError', 'input']
header_internal = ['blockNumber', 'timeStamp', 'hash', 'from', 'to', 'value', 'gas', 'gasUsed', 'isError', 'input']
write_csv_normal.writerow(header_normal)
write_csv_internal.writerow(header_internal)

block_num_next_start = block_num_start
blocks_tried = 0
while block_num_next_start <= block_num_end:
    block_num_next_end = block_num_next_start + block_num_increment
    if block_num_next_end > block_num_end:
        block_num_next_end = block_num_end
            
    start_block = str(block_num_next_start)
    end_block = str(block_num_next_end)
    #print(start_block + '\t' + end_block)

    num_normal = 0
    num_internal = 0

    #Normal TXs
    url_normal = url_part_normal + start_block + '&endblock=' + end_block + param_api_key
    #print(url_normal)
    resp_normal = requests.get(url=url_normal)
    data_normal = resp_normal.json()
        
    for r in data_normal["result"]:
        tx_data_normal = [r["blockNumber"], r["timeStamp"], r["hash"], r["nonce"], r["from"], r["to"], r["value"], r["gas"], r["gasUsed"], r["gasPrice"], r["isError"], r["input"]]
        write_csv_normal.writerow(tx_data_normal)
    num_normal = len(data_normal["result"])

    #Internal TXs
    url_internal = url_part_internal + start_block + '&endblock=' + end_block + param_api_key
    #print(url_internal)
    resp_internal = requests.get(url=url_internal)
    data_internal = resp_internal.json()

    for r in data_internal["result"]:
        tx_data_internal = [r["blockNumber"], r["timeStamp"], r["hash"], r["from"], r["to"], r["value"], r["gas"], r["gasUsed"], r["isError"], r["input"]]
        write_csv_internal.writerow(tx_data_internal)
    num_internal = len(data_internal["result"])
        
    fd_status.write(start_block + ',' + end_block + ',' + str(num_normal) + ',' + str(num_internal) + '\n')

    block_num_next_start += (block_num_increment + 1)

    elapsed_time = time.perf_counter() - start_time
    blocks_tried += 1
    print(start_block, end_block, elapsed_time, elapsed_time/blocks_tried)

fd_out_normal.close()
fd_out_internal.close()