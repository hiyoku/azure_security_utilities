from azure.cli.core import get_default_cli
from time import strftime, time

FILENAME_USERS = "Azure_User_Bulk_Delete/remove_list.txt"
FILENAME_TEST = "Azure_User_Bulk_Delete/remove_test.txt"

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
        for line_id in remove_file.readlines():
            _user_id = str(line_id.split()[0])
            user_info = az_cli(f"ad user show --id {_user_id}")
            print(f"Deleting ID: {_user_id} - {user_info['displayName']}... ", end="")
            res = az_cli(f"ad user delete --id {_user_id}")
            print(res, flush=True)

    print(f"Done in: {time() - st} seconds")

if __name__ == "__main__":
    main()