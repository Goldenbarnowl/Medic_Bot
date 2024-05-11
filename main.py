import asyncio
import logging
import sys

from config import main
import UserHandler


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
