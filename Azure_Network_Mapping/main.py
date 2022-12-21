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

def main():
    networks_json = az_cli("network vnet list")
    with open(FILENAME, "w") as f:
        f.write("resource_group, region, vnet_name, subnet_name, vnet_address_range, subnet_address_prefix\n")
        for network in networks_json:
            for subnet in network['subnets']:
                line_file = [network['resourceGroup'], 
                             network['location'],
                             network['name'], 
                             subnet['name'],
                             " ".join(network['addressSpace']['addressPrefixes']),
                             str(subnet['addressPrefix'])]
                f.write(", ".join(line_file) + "\n")

if __name__ == "__main__":
    main()