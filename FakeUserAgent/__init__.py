from faker import Faker

FIREFOX = "Firefox"

class FakeUserAgent:
    def __init__(self):
        self.fake = Faker()
    
    def get_random_user_agent(self, type = FIREFOX):
        while True:
            user_agent = self.fake.user_agent()
            if type in user_agent:
                return user_agent
