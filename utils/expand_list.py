def expand_int_list(input):
    items = []

    if not input:
        return items

    parts = input.split(',')
    for part in parts:
        if part.strip() != '':
            try:
                if '-' in part:
                    start_stop = part.split('-')
                    start = start_stop[0]
                    stop = start_stop[-1]

                    for number in range(int(start), int(stop)+1):
                        items.append(number)
                else:
                    items.append(int(part))
            except Exception:
                pass

    return items
