from injector import Injector

from src.config import Config


def main():
    container = Injector()
    config = container.get(Config)
    print(config.database)


if __name__ == "__main__":
    main()
