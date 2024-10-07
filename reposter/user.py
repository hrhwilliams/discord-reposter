user_file = {}
user_fmt = {}
user_posting = {}


def set_user_open_file(author, open_file, fmt):
    global user_file, user_fmt
    id = int(author.id)
    user_file[id] = open_file
    user_fmt[id] = fmt


def get_user_open_file(author):
    global user_file, user_fmt
    id = int(author.id)
    if id in user_file:
        return (user_file[id], user_fmt[id])
    return None


def set_user_is_currently_posting(author, status: bool):
    global user_posting
    user_posting[int(author.id)] = status


def get_user_is_currently_posting(author):
    global user_posting
    id = int(author.id)
    if id in user_posting:
        return user_posting[id]
    return False
