#Return N most max elements for a list
def n_max_elements(list_: list, N: int):
    return sorted(list_, reverse=True)[:N]