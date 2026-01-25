class B:
    def __init__(self):
        self.client = None


class A(B):

    def setup(self):
        self.client = "CLIENT"


x = A()
print(x.__dict__)