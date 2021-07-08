import RipNetInterfaces

rn = RipNetInterfaces.RipNetInterfaces


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def get_interfaces():
    int_list = rn.list_interfaces()
    rn.descr_interfaces(int_list)


if __name__ == '__main__':
    print_hi('PyCharm')
    int_dict = get_interfaces()
