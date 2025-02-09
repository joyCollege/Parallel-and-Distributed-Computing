from .add_random_numbers import add_random_numbers

def worker(start, end, result_list):
    partial_sum = add_random_numbers(start, end)
    result_list.append(partial_sum)
    print(f">> Range {start}-{end} finished with sum {partial_sum}")