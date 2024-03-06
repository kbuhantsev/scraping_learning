from fake_useragent import UserAgent


if __name__ == "__main__":

    ua = UserAgent()
    for _ in range(3):
        print(ua.random)
