from reposter import create_client

if __name__ == '__main__':
    with open('token.txt', 'r') as token_file:
        token = token_file.read()

    client = create_client()
    client.run(token)
