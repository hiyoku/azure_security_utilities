from azure.cli.core import get_default_cli
from time import strftime

FILENAME = "nsg_mapping_" + strftime("%Y%m%d") + ".csv"

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
    
    with open(FILENAME, 'w') as f:
        f.write("subscription, resource_group, location, name, type, direction, priority, source_port, source_address, destination_port, destination_address, access\n")
        for _sub in subs.keys():
            print(f"Reading subscription '{subs[_sub]}' = '{_sub}'")
            dict_nsgs = az_cli(f"network nsg list --subscription {_sub}")

            if type(dict_nsgs) != list:
                print("No NSGs Found!")
                continue

            for nsg in dict_nsgs:
                # Lendo as regras padroes
                rules_inbound = {}
                rules_outbound = {}
                for default_rule in nsg['defaultSecurityRules']:
                    f.write(f"{subs[_sub]}, {nsg['resourceGroup']}, {nsg['location']}, {nsg['name']}, default, {default_rule['direction']}, {default_rule['priority']}, {default_rule['sourcePortRange']}, {default_rule['sourceAddressPrefix']}, {default_rule['destinationPortRange']}, {default_rule['destinationAddressPrefix']}, {default_rule['access']}\n")

                for custom_rules in nsg['securityRules']:
                    source_ports = custom_rules['sourcePortRange'] if "sourcePortRange" in custom_rules.keys() else ""
                    source_ports += (";".join(custom_rules['sourcePortRanges']))
                    
                    source_addresses = custom_rules['sourceAddressPrefix'] if "sourceAddressPrefix" in custom_rules.keys() else ""
                    source_addresses += (";".join(custom_rules['sourceAddressPrefixes']))
                    
                    destination_ports = custom_rules['destinationPortRange'] if "destinationPortRange" in custom_rules.keys() else ""
                    destination_ports += (";".join(custom_rules['destinationPortRanges']))

                    destination_addresses = custom_rules['destinationAddressPrefix'] if "destinationAddressPrefix" in custom_rules.keys() else ""
                    destination_addresses += (";".join(custom_rules['destinationAddressPrefixes']))

                    f.write(f"{subs[_sub]}, {nsg['resourceGroup']}, {nsg['location']}, {nsg['name']}, custom, {custom_rules['direction']}, {custom_rules['priority']}, {source_ports}, {source_addresses}, {destination_ports}, {destination_addresses}, {custom_rules['access']}\n")

if __name__ == "__main__":
    main()
    # IaC = Infrastructure as Code
    # Terraform HC, Ansible RH, 