from contract.repository.Base import Base as BaseRepositoryInterface

class User:
    def __init__(self, user_repository: BaseRepositoryInterface):
        self.user_repository = user_repository