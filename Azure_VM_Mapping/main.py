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

def get_subscriptions_list() -> dict:
    subscriptions_json = az_cli("account list")
    subscriptions = {}
    for _subscription in subscriptions_json:
        subscriptions[_subscription["id"]] = _subscription["name"]
    
    return subscriptions

def main():
    '''
        Pegar a lista de vnets e subnets em dict
        mapear as vnets e subnets da vm pelo dict
    '''

    subs = get_subscriptions_list()

    dict_nics = {}

    for _sub in subs.keys():
        print(f"Reading subscription '{subs[_sub]}' = '{_sub}'")
        json_nics = az_cli(f"network nic list --subscription {_sub}")

        if type(json_nics) != list:
            print("No NICs found!")
            continue

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

    with open(FILENAME, "w") as f:
        f.write("subscription, resource_group, region, vm_name, vnet_name, subnet_name, nic_name\n")
        for _sub in subs.keys():
            print(f"Reading subscription '{subs[_sub]}' = '{_sub}'")
            json_vms = az_cli(f"vm list --subscription {_sub}")

            if type(json_vms) != list:
                print("No VMs found!")
                continue

            for vm in json_vms:
                if len(vm['networkProfile']['networkInterfaces']) == 0:
                    f.write(f"{subs[_sub]}, {vm['resourceGroup']}, {vm['location']}, {vm['name']}, null, null, null\n")
                    continue

                for nic in vm['networkProfile']['networkInterfaces']:
                    f.write(f"{subs[_sub]}, {vm['resourceGroup']}, {vm['location']}, {vm['name']}, {dict_nics[nic['id']][0]}, {' '.join(dict_nics[nic['id']][1])}, {nic['id'].split('/')[-1:][0]}\n")
            

if __name__ == "__main__":
    main()