import re
import os
import argparse


def build_dict(file, delimiter, base_d=None, custom_d=None):
    """
    Open the file and parse every string.
    Parsed data insert into one of dictionary,
    required of transferred args.
    """
    with open(file, "r") as rfile:
        for string in rfile.readlines():
            if string.startswith("#"):
                continue
            matched = re.findall(
                r"(.+?)\s?{0}\s?(.*)".format(delimiter), string)
            for i in matched:
                i = list(i)  # because i is tuple, immutable
                i[0] = i[0].strip()
                i[1] = i[1].strip()

                if custom_d is None:
                    base_d[i[0]] = i[1]
                else:
                    custom_d[i[0]] = i[1]


def difference(base_d, custom_d):
    """
    Print difference between base file and
    custom file.
    The equivalent fields will be passed.

    Be meant the field in prod-file is unique.
    """

    option = "user configure"
    print(head.format(option.upper()))

    for key, value in custom_d.items():
        if key not in base_d:
            print key + "=" + value 

        # elif value != base_d[key]:
        #     print(key, "=", value, sep="")


def concatenate(base_d, custom_d):
    """
    Print sorted base file + custom file.
    The equivalent key-option value takes from custom file.
    """
    def where_is_dot(string):
        """
        return index of dot
        or length (string)
        """
        dot = string.find(".")

        if dot == -1:
            dot = len(string)
        return dot

    base_d.update(custom_d)  # merge diction
    kv_store_sorted = sorted(base_d.items())
    option = kv_store_sorted[0][0]
    option = option[:where_is_dot(option)]

    print(head.format(option.upper()))

    for key, value in kv_store_sorted:
        dot = where_is_dot(key)

        if option != key[:dot]:
            option = key[:dot]
            print(head.format(option).upper())

        print key + "=" + value


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Script print difference or concatenate between base and custom files, but not overwrite!",
        epilog="Attention! Mode \"concatenate\" sorts keys, you can lose structure")
    parser.add_argument("base_files", metavar="BASE FILES", nargs="*",
                        help="base files also know `prod-file`")

    parser.add_argument("-c", metavar="CUSTOM FILES", nargs="*",
                        help="custom files, which need merge", dest="custom")

    parser.add_argument("--delimiter", metavar="SYMBOL", nargs="?", default="=",
                        help="delimiter between option and value")

    parser.add_argument("--mode", metavar="MODE", default="difference", choices=["difference", "concatenate"],
                        help="exists two mode: difference and changed sum, by default: difference")
    args = parser.parse_args()

    if (args.base_files or args.custom) is None:
        parser.print_help()
        exit(1)

    base = {}
    custom_base = {}
    head = """
###########################################################################
# {}
###########################################################################
"""

    for b in args.base_files:
        if not os.path.exists(b):
            raise Exception('Path not found to file', b)
        build_dict(b, base_d=base, delimiter=args.delimiter)

    for c in args.custom:
        if not os.path.exists(c):
            raise Exception('Path not found to file', c)
        build_dict(c, custom_d=custom_base, delimiter=args.delimiter)

    assert((len(base) or len(custom_base)) >
           0), "The program with this options not found elements.\nOptions: {}".format(args)

    if args.mode == "difference":
        difference(base, custom_base)
    elif args.mode == "concatenate":
        concatenate(base, custom_base)
