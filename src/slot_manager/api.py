from fastapi import FastAPI
from .load_manager import LoadManager


class ApiServer:
    def __init__(self, manager: LoadManager):
        self.manager = manager
        self.app = FastAPI()
        self.app.add_api_route('/availability', self.availability, methods=['GET'])

    async def availability(self):
        slots = self.manager.available_slots()
        return {"available_slots": slots}
