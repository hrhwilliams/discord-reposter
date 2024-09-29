allowlist = []


def allow(id):
    global allowlist
    allowlist.append(int(id))


def auth(author):
    global allowlist
    return author.id in allowlist
