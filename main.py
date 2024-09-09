import asyncio

from src.redirect import start_proxy_dofus_config

if __name__ == "__main__":
    asyncio.run(start_proxy_dofus_config(True))
