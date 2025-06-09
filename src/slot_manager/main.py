import uvicorn
from .config import load_env
from .load_manager import LoadManager
from .scheduler import Scheduler
from .api import ApiServer


def main():
    load_env()
    manager = LoadManager()
    api = ApiServer(manager)
    scheduler = Scheduler(manager)
    scheduler.start()
    uvicorn.run(api.app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
