from azure.cli.core import get_default_cli
from time import strftime

FILENAME = "vm_mapping_" + strftime("%Y%m%d") + ".csv"

def az_cli (args_rec: str):
    args = (args_rec + " --output none").split()
    cli = get_default_cli()
    cli.invoke(args)
    if cli.result.result:
        return cli.result.result
    elif cli.result.error:
        raise cli.result.error
    return True

def main():
    '''
        Pegar a lista de vnets e subnets em dict
        mapear as vnets e subnets da vm pelo dict
    '''
    json_nics = az_cli("network nic list") # [0]['ipConfigurations'][0]['subnet']
    dict_nics = {}
    for nic in json_nics:
        if 1 == len(nic['ipConfigurations']):
            list_id = nic['ipConfigurations'][0]['subnet']['id'].split('/')
            dict_nics[nic['id']] = [list_id[8], [list_id[10]]]
        else:
            for configs in nic['ipConfigurations']:
                list_id = configs['subnet']['id'].split('/')
                if nic['id'] in dict_nics.keys():
                    if list_id[8] == dict_nics[nic['id']][0] and list_id[10] not in dict_nics[nic['id']][1]:
                        dict_nics[nic['id']][1].append(list_id[10])
                else:
                    dict_nics[nic['id']] = [list_id[8], [list_id[10]]]

    json_vms = az_cli("vm list")
    with open(FILENAME, "w") as f:
        f.write("resource_group, region, vm_name, vnet_name, subnet_name\n")
        for vm in json_vms:
            if len(vm['networkProfile']['networkInterfaces']) == 0:
                f.write(f"{vm['resourceGroup']}, {vm['location']}, {vm['name']}, null, null\n")
                continue

            for nic in vm['networkProfile']['networkInterfaces']:
                f.write(f"{vm['resourceGroup']}, {vm['location']}, {vm['name']}, {dict_nics[nic['id']][0]}, " + " ".join(dict_nics[nic['id']][1]) + "\n")
            

if __name__ == "__main__":
    main()