import texts


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return texts.user_profile.format(name=self.name, age=self.age)
