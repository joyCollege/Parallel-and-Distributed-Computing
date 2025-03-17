from src.pt2_add_random_numbers import add_random_numbers

def worker(start, end, result_list):
    """
    Computes the sum of random numbers within a given range and stores the result.

    Args:
        start (int): The starting index of the range.
        end (int): The ending index of the range.
        result_list (list): A shared list to store the computed sum.

    Returns:
        None
    """
    partial_sum = add_random_numbers(start, end)
    result_list.append(partial_sum)
    print(f">> Range {start}-{end} finished with sum {partial_sum}")

    partial_sum = add_random_numbers(start, end)
    result_list.append(partial_sum)
    print(f">> Range {start}-{end} finished with sum {partial_sum}")