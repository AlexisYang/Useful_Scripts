import json
import subprocess

service_ip = '169.254.111.125'

def get_from_API(suffix):
    command = ["curl","-u", "sdbox:sdbox","-s","http://" + service_ip + "/api/"+ suffix]
    proc = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE).communicate()
    tmp = proc[0].split('\n')
    result = json.loads(tmp[0])
    return result

def get_port_stats():
    port_list = []
    command = "sudo ovs-ofctl dump-ports-desc br0"
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()
    for val in  result[0].split('\n'):
        if '(fa' in val:
            port = {}
            port['number'] = val[1:val.index('(')]
            port['name'] = val[val.index('(')+1:val.index(')')]
            port_list.append(port)
    return port_list

suffix = "box/"
result = get_from_API(suffix)
suffix = "box/vnics/"
result2 = get_from_API(suffix)
box_list = []
ports = get_port_stats()
for i, val in enumerate(result):
    box = {}
    box['name'] = (val['name'])
    box['id'] = (val['id'])
    for j, val2 in enumerate(result2):
        if val2['box_id'] == box['id']:
            box['vnic'] = val2['name']
            result2.remove(val2)
            break
    box['port'] = 'None'
    for j, val2 in enumerate(ports):
        if box['vnic'] == val2['name']:
            box['port'] = val2['number']
            ports.remove(val2)
            break
    box_list.append(box)
for i, val in enumerate(box_list):
    print val


