def parse_arguments(toot: str):
    # args:
    # set key1 value1, key2
    # key1 is value1, key2 is set to True

    parsed = {
        'lang': 'en',
        'mono': False,
        'flip': False
    }  # default

    for line in [l.strip().lower() for l in toot.splitlines()]:
        if line.startswith('set:'):
            args = [l.strip().split(maxsplit=1)
                    for l in line.replace('set:', '', 1).split(',')]
            if args:
                for arg in args:
                    if len(arg) == 1:
                        parsed[arg[0]] = True
                    elif len(arg) == 2:
                        # arg = (key, value)
                        parsed[arg[0]] = arg[1]

    return parsed
                    
