allowlist = []


def read_allowlist(filepath="allowlist.txt"):
    global allowlist
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file.readlines():
            if len(line) > 0:
                allow(line.strip())


def allow(id):
    global allowlist
    allowlist.append(int(id))


def auth(author):
    global allowlist
    try:
        return int(author.id) in allowlist
    except:
        return False
