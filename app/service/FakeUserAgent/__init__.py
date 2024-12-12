from faker import Faker

CHROME = 'Chrome'

class FakeUserAgent:
    def __init__(self):
        self.fake = Faker()
    
    def get_random_user_agent(self, type: str = CHROME) -> str:
        while True:
            user_agent = self.fake.user_agent()
            if type in user_agent:
                return user_agent
