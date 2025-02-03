import timeit
import json
from datasketch import HyperLogLog

def get_unique_ip_set(lines):
    unique_ip_set = set()
    for line in lines:
        try:
            unique_ip_set.add(json.loads(line.strip())['remote_addr'])
        except (json.JSONDecodeError, KeyError):
            continue
    return len(unique_ip_set)

def get_unique_ip_hll(lines):
    hll = HyperLogLog(p=12)
    for line in lines:
        try:
            hll.update(json.loads(line.strip())['remote_addr'].encode('utf-8'))
        except (json.JSONDecodeError, KeyError):
            continue
    return hll.count()

with open('lms-stage-access.log', mode='r') as file:
    log_lines = file.readlines()

set_elements = get_unique_ip_set(log_lines)
hll_elements = get_unique_ip_hll(log_lines)

set_time = timeit.timeit(lambda: get_unique_ip_set(log_lines), number=1)
hll_time = timeit.timeit(lambda: get_unique_ip_hll(log_lines), number=1)

print("+------------------------+----------------------+----------------------+")
print(f"| {'':<22} | {'Set()':<20} | {'HyperLogLog':<20} |")
print("+------------------------+----------------------+----------------------+")
print(f"| {'Унікальні елементи':<22} | {set_elements:<20,} | {hll_elements:<20,} |")
print(f"| {'Час виконання (сек.)':<22} | {set_time:<20.6f} | {hll_time:<20.6f} |")
print("+------------------------+----------------------+----------------------+")
