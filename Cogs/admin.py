import interactions


class Admin(interactions.Extension):
    def __init__(self, client):
        self.client = client





def setup(client):
    Admin(client)
