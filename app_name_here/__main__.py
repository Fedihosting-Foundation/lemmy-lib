import logging
import os

if os.getenv("LOG_LEVEL") is None:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=int(os.getenv("LOG_LEVEL")))


def print_hi():
    logging.debug("SoP")
    print("Hello world")

def main():
    print_hi()

if __name__ == "__main__":
    print_hi()
