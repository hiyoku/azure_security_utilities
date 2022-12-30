from azure.cli.core import get_default_cli
from time import strftime

FILENAME = "azure_network_mapping_" + strftime("%Y%m%d") + ".csv"

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
    subs = get_subscriptions_list()

    with open(FILENAME, "w") as f:
        f.write("subscription, resource_group, region, vnet_name, subnet_name, vnet_address_range, subnet_address_prefix\n")

        for _sub in subs.keys():
            print(f"Reading subscription '{subs[_sub]}' = '{_sub}'")
            networks_json = az_cli(f"network vnet list --subscription {_sub}")
            if type(networks_json) != list:
                print("No VNETs found!")
                continue

            for network in networks_json:
                for subnet in network['subnets']:
                    line_file = [subs[_sub],
                                network['resourceGroup'], 
                                network['location'],
                                network['name'], 
                                subnet['name'],
                                " ".join(network['addressSpace']['addressPrefixes']),
                                str(subnet['addressPrefix'])]
                    f.write(", ".join(line_file) + "\n")

if __name__ == "__main__":
    # s = get_subscriptions_list()
    # for _s in s.keys():
    #     print(f"{_s} - {type(_s)}")

    main()