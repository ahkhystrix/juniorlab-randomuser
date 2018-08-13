import requests


def get_randomuser(count):
    """Get users from https://randomuser.me/ in JSON"""
    url = "https://randomuser.me/api/?results=" + str(count)
    r = requests.get(url=url)
    users = r.json()
    return users


if __name__ == "__main__":
    users = get_randomuser(2)
    print(users)
