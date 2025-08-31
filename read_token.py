def read_token() -> str:
    token = ""
    with open("./token.txt", "rt") as file:
        token = file.read()
    return token