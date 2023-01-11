from azure.cli.core import get_default_cli
from time import strftime, time

FILENAME_USERS = "users_list_" + strftime("%Y%m%d") + ".csv"
FILENAME_GROUPS = "groups_list_" + strftime("%Y%m%d") + ".csv"
FILENAME_USERS_GROUPS = "users_groups_list_" + strftime("%Y%m%d") + ".csv"
FILENAME_EMPTY = "empty_list_" + strftime("%Y%m%d") + ".csv"

def az_cli(args_rec: str):
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
    dict_groups = {}
    dict_users = {}

    # Getting Group List
    print("Reading all groups from actual tenant...", end="", flush=True)
    st = time()
    with open(FILENAME_GROUPS, mode="w", encoding="utf8") as group_file:
        group_file.write("Group ID, Group Name, Created Datetime\n")
        group_list = az_cli("ad group list")
        for group in group_list:
            str_print = f"{group['id']},{group['displayName']},{group['createdDateTime']}\n"
            group_file.write(str_print)
            dict_groups[group["id"]] = {"displayName": group["displayName"], "createdDateTime": group["createdDateTime"]}
            # print(str_print, endl="")

    print(f" Done in: {time() - st} seconds")
    print("Reading all users from actual tenant...", end="", flush=True)
    st = time()
    # Gettint User List
    with open(FILENAME_USERS, mode="w", encoding="utf8") as user_file:
        user_file.write("User ID, User Name, Job Title, PrincipalName, Domain\n")
        user_list = az_cli("ad user list")

        for user in user_list:
            domain_name = user['userPrincipalName'].split("@")[1]
            if domain_name == "usebitz.onmicrosoft.com":
                domain_name = user['userPrincipalName'].split("@")[0].split("#")[0].split("_")[1]

            str_print = f"{user['id']},{user['displayName']},{user['jobTitle']},{user['userPrincipalName']},{domain_name}\n"
            user_file.write(str_print)
            dict_users[user['id']] = {"displayName": user['displayName'], "domainName": domain_name}

    # Getting
    #az_cli(f"az ad user get-member-groups --id '{}'")
    list_used_groups = []
    print(f" Done in: {time() - st} seconds")
    print("Reading all users and groups from actual tenant...")
    st = time()

    with open(FILENAME_EMPTY, mode="w", encoding="utf8") as empty_file:
        empty_file.write("Type, id, name\n")
        with open(FILENAME_USERS_GROUPS, mode="w", encoding="utf8") as users_groups_file:
            users_groups_file.write("User ID, User Name, Domain, Group ID, Group Name, Group Creation Datetime\n")
            total_users = len(dict_users.keys())
            count = 0
            for u_key, u_values in dict_users.items():
                count += 1
                print(f"Reading user {count}/{total_users}...", end="\r")
                user_groups = az_cli(f"ad user get-member-groups --id {u_key}")
                if type(user_groups) == list:
                    if len(user_groups):
                        for _group in user_groups:
                            if _group['id'] not in list_used_groups:
                                list_used_groups.append(_group['id'])
                            users_groups_file.write(f"{u_key},{u_values['displayName']},{u_values['domainName']},{_group['id']},{_group['displayName']}\n")
                    else:
                        print("User have 0 groups")
                        empty_file.write(f"User,{u_key},{u_values['displayName']}\n")
                else:
                    empty_file.write(f"User,{u_key},{u_values['displayName']}\n")

            for g_key in dict_groups.keys():
                if g_key not in list_used_groups:
                    empty_file.write(f"Group,{g_key},{dict_groups[g_key]['displayName']}\n")
                

    print(f"\nDone in: {time() - st} seconds")

if __name__ == "__main__":
    main()