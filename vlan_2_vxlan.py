#!/usr/bin/python3

# script to convert junos vlan stanza to apstra csv for automated import.
# get src_config with show configuration vlan | display json

# import necessary python modules
import json
import csv

dc_vniprefix = 1000000
ill_charset = "!.#"

# import JSON
input_json = 'src_config.json'
with open(input_json, 'r') as f:
    data = json.load(f)

field_names = ['vn_node_id', 'vn_name', 'rz_name', 'vn_type', 'vn_id', 'reserved_vlan_id', 'dhcp_service', 'ipv4_enabled', 'ipv6_enabled', 'virtual_gateway_ipv4_enabled', 'virtual_gateway_ipv6_enabled', 'ipv4_subnet', 'ipv6_subnet', 'virtual_gateway_ipv4', 'virtual_gateway_ipv6', 'l3_mtu', 'bound_to_dc1_rack_0101_leaf_pair1', 'bound_to_dc1_rack_0102_leaf_pair1', 'bound_to_dc1_rack_0103_leaf_pair1']

# open CSV and append line
with open("DC1-BLUEPRINT_VNs.csv", 'a', newline='', encoding='utf-8') as csvfile:
    csv_data = csv.reader(csvfile, delimiter=',', quotechar='|')
    dictwriter_object = csv.DictWriter(csvfile, fieldnames=field_names)
    for item in data['configuration']['vlans']['vlan']:
        print(item)
        # remove ill chars from vlan names
        for ill_char in ill_charset:
            item['name'] = item['name'].replace(ill_char, "")

        dict = {'vn_id': dc_vniprefix + int(item['vlan-id']), 'vn_name': item['name'], 'vn_type': 'vxlan', 'rz_name': 'DC1-RZ1', 'bound_to_dc1_rack_0101_leaf_pair1': item['vlan-id'], 'bound_to_dc1_rack_0102_leaf_pair1': item['vlan-id'], 'bound_to_dc1_rack_0103_leaf_pair1': item['vlan-id']}
        dictwriter_object.writerow(dict)

        # oldname print(item['name']['data'])
        # vlan id print(item['vlan-id'][0]['data'])

    csvfile.close()
