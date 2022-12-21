from azure.cli.core import get_default_cli

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
    pass

if __name__ == "__main__":
    main()