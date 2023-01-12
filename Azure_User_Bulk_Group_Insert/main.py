from azure.cli.core import get_default_cli
from time import strftime, time

FILENAME_USERS = "Azure_User_Bulk_Group_Insert/user_list.txt"
_GROUP_ID = "GROUP_ID"

def az_cli(args_rec: str):
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

    # Getting Group List
    print(f"Reading all users from {FILENAME_USERS}")
    st = time()

    with open(FILENAME_USERS, mode="r", encoding="utf8") as remove_file:
        group_info = az_cli(f"ad group show -g {_GROUP_ID}")

        for line_id in remove_file.readlines():
            _user_id = str(line_id.split()[0])
            user_info = az_cli(f"ad user show --id {_user_id}")
            print(f"Add user ID: {_user_id} - {user_info['displayName']} to GroupID: {group_info['id']} - {group_info['displayName']}... ", end="")
            res = az_cli(f"ad group member add -g {_GROUP_ID} --member-id {_user_id}")
            print(res, flush=True)

    print(f"Done in: {time() - st} seconds")

if __name__ == "__main__":
    main()