from app.main.src.DataLoader.Adapters import ReportLineToModelsAdapter
from app.main.src.DataLoader.ChunkProcessors import ChunkProcessor
from app.main.src.GameManagement.Services import UserService, GameActionService, OfferService


class MongoProcessor(ChunkProcessor):
    def __init__(self):
        self.user_service: UserService = UserService()
        self.action_service: GameActionService = GameActionService()
        self.order_service: OfferService = OfferService()

    def process_line(self, line):
        adapter_result = ReportLineToModelsAdapter(line.split(','))
        update_result = self.user_service.insert_or_update(adapter_result.user)
        if update_result['n'] != 1:
            raise "Cant isert update user"
            return

        adapter_result.game_action.id = self.action_service.insert(adapter_result.game_action)

        if not adapter_result.game_action.id:
            raise "Can't process action"
            return

        self.order_service.insert(adapter_result.offer)

        return True

    def process_chunk(self, line_list):
        for line in line_list:
            self.process_line(line)

    def close(self):
        pass