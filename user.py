import texts


class User:
    def __init__(self, id, gender=None, name=None, age=None, match_id=None):
        self.id = id
        self.gender = gender
        self.name = name
        self.age = age
        self.match_id = match_id

    def get_match(self):
        from database import Database
        return Database.load_user(self.match_id)

    @property
    def resolved_gender(self):
        genders = {0: "پسر", 1: "دختر"}
        return genders[self.gender]

    def __str__(self):
        return texts.user_profile.format(gender=self.resolved_gender, name=self.name, age=self.age)

    def needs_registration(self):
        return self.name is None
