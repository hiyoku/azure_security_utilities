from pprint import PrettyPrinter

def main():
    unused_vnets = []
    used_vnets = []

    with open("vm_mapping_20221227.csv", "r") as vm_file:
        for vm_line in vm_file.readlines():
            row = vm_line.split(",")
            # Region, VNet, SNet
            used_vnets.append([row[1], row[3], row[4]])

    with open("azure_network_mapping_20221227.csv", "r") as vnet_file:
        for vnet_line in vnet_file.readlines()[1:]:
            row = vnet_line.split(",")
            if [row[1], row[2], row[3]] not in used_vnets and row[3] != " AzureBastionSubnet":
                unused_vnets.append([row[1], row[2], row[3]])
                print(f"{row[1], row[2], row[3]}")
            # Region, VNet, SNet
            # vnets.append(row[1], row[2], row[3])

if __name__ == "__main__":
    main()