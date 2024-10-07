allowlist = []


def allow(id):
    global allowlist
    allowlist.append(int(id))


def auth(author):
    global allowlist
    return int(author.id) in allowlist
