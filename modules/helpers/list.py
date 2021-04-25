def print_list(arr, seperator):
    str_array = [str(item) for item in arr]
    output = f'{seperator} '.join(str_array)
    print(output)


def shift(list: list() = None, steps: int = None):
    list_copy = list[:]
    for step in range(steps):
        list_copy.append(list_copy.pop(0))
    return list_copy


def find_index_for_first_none_value(iterator):
    return next((index for index, item in enumerate(iterator) if item == None), None)
