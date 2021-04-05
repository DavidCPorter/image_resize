import os
import argparse
import yaml
from rich import print as rprint
import resizer.resize_img as resizer
import pdb
import pathlib
ROOT = str(pathlib.Path(__file__).parent.absolute())
print(ROOT)

def main_interface():
    """command shims- returns a dict with command functions"""

    def resize_img(**kwargs):
        filename = kwargs.get('filename')
        basewidth =kwargs.get('width')
        outname = kwargs.get('outname')
        resizer.resize_img(filename, basewidth, outname)

    return dict(
        resize_img=resize_img
    )

def interactive_mode(**kwargs):

    if kwargs.get("ansible"):
        pass

    elif kwargs.get("interactive"):
        i_interface = interactive_interface()
        user_command = ""
        while user_command != "exit":
            user_command = input(f"{objects_list[0].name}> ")
            user_command.split()
            user_command.replace("  ", " ")

            if user_command in ("", "exit"):
                continue

            user_command_list = user_command.split(" ")
            if user_command_list[-1] == "":
                user_command_list.pop()

            try:
                load_commands = user_command_list
                # for interactive mode options, need this object
                kwargs.update({"pobject": objects_list[0]})

                if load_commands[0] == "get_attr":
                    kwargs.update({"attr": load_commands[1]})

                if load_commands[0] == "switch":
                    objects_list = [objects_list[1], objects_list[0]]
                    continue

                if len(objects_list) > 1:
                    return_object = i_interface.get(
                        load_commands[0], i_interface.get("bad_input")
                    )(**kwargs)
                    objects_list = [return_object.pop(), objects_list[1]]

                else:
                    objects_list = i_interface.get(
                        load_commands[0], i_interface.get("bad_input")
                    )(**kwargs)

            except (RuntimeError, TypeError, NameError, IndexError) as e:
                traceback.print_exc()
                print("error -> ", e)

    else:
        return


def main():
    # create the top-level parser
    parser = argparse.ArgumentParser(
        description="resizes images"
    )

    subparsers = parser.add_subparsers(title="commands", dest="command")
    with open(ROOT + "/commands.yml") as cmd_file:
        my_commands = yaml.safe_load(cmd_file)

    parser_dict = {cmd: subparsers.add_parser(cmd) for cmd in my_commands.keys()}
    for command, cmd_subparser in parser_dict.items():
        for flag, arg_dict in my_commands.get(command).items():
            cmd_subparser.add_argument(flag, **arg_dict)

    args = parser.parse_args()
    main_api = main_interface()

    if args.command not in main_api.keys():
        print(f"\n{args.command} command has no API\n")
        raise NotImplementedError


    entry_point = main_api.get(args.command)(**vars(args))

    # interactive mode loop.. good for inspection and debugging pobjects
    kwargs = vars(args)
    if kwargs.get("interactive"):
        interactive_mode(**kwargs)


if __name__ == "__main__":
    main()
