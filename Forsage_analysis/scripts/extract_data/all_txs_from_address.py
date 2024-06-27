import requests;
import csv;
import json;
import time;

file_addresses = 'accounts_and_events_restructured.csv'
file_txs_normal = 'txs_normal.csv'
file_txs_internal = 'txs_internal.csv'
file_status = 'status.csv'
start_block = '9391531'
end_block = '12243908' #'12243749'
start_idx = 1
end_idx = 10000

api_key='ADD Etherscan.io API KEY HERE'
param_api_key = '&sort=asc&apikey=' + api_key

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
        num_normal = 0
        num_internal = 0

        #Normal TXs
        url_normal = 'https://api.etherscan.io/api?module=account&action=txlist&address=' \
            + address + '&startblock=' + start_block + '&endblock=' + end_block + param_api_key
        #print(url_normal)
        resp_normal = requests.get(url=url_normal)
        data_normal = resp_normal.json()
        
        for r in data_normal["result"]:
            tx_data_normal = [r["blockNumber"], r["timeStamp"], r["hash"], r["nonce"], r["from"], r["to"], r["value"], r["gas"], r["gasUsed"], r["gasPrice"], r["isError"], r["input"]]
            write_csv_normal.writerow(tx_data_normal)
        num_normal = len(data_normal["result"])

        #Internal TXs
        url_internal = 'https://api.etherscan.io/api?module=account&action=txlistinternal&address=' \
            + address + '&startblock=' + start_block + '&endblock=' + end_block + param_api_key
        #print(url_internal)
        resp_internal = requests.get(url=url_internal)
        data_internal = resp_internal.json()

        for r in data_internal["result"]:
            tx_data_internal = [r["blockNumber"], r["timeStamp"], r["hash"], r["from"], r["to"], r["value"], r["gas"], r["gasUsed"], r["isError"], r["input"]]
            write_csv_internal.writerow(tx_data_internal)
        num_internal = len(data_internal["result"])
        
        fd_status.write(address + ',True,' + str(num_normal) + ',True,' + str(num_internal) + '\n')

        elapsed_time = time.perf_counter() - start_time
        print(next_address_count, elapsed_time, elapsed_time/(next_address_count - start_idx + 1))

fd_in.close()
fd_out_normal.close()
fd_out_internal.close()