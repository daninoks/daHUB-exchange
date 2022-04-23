class UserPropeties:
    def __init__(self):

        try:
            users_dict
        except NameError:
            self.users_dict = {}
            print("in exception")
        self.users_dict["user_id"] = {
                "lang": "rus",
                "pay_cur": "",
                "get_cur": "",
                "value_cur": ""
                }

    def create_if_empty(self, user_id):
        if user_id not in self.users_dict.keys():
            self.users_dict[user_id] = {
                    "lang": "rus",
                    "pay_cur": "",
                    "get_cur": "",
                    "value_cur": ""
                    }

    def set_lang(self, user_id, value):
        self.create_if_empty(user_id)
        self.users_dict[user_id]['lang'] = value
        # self.lang = self.users_dict[user_id].get('lang')

    def set_pay_cur(self, user_id, value):
        self.create_if_empty(user_id)
        self.users_dict[user_id]['pay_cur'] = value
        # self.lang = self.users_dict[user_id].get('pay_cur')

    def set_get_cur(self, user_id, value):
        self.create_if_empty(user_id)
        self.users_dict[user_id]['get_cur'] = value
        # self.lang = self.users_dict[user_id].get('get_cur')

    def set_value_cur(self, user_id, value):
        self.create_if_empty(user_id)
        self.users_dict[user_id]['value_cur'] = value
        # self.lang = self.users_dict[user_id].get('value_cur')

    def get_lang(self, user_id):
        self.create_if_empty(user_id)
        user_lang = self.users_dict[user_id].get('lang')
        return user_lang

    def get_pay_cur(self, user_id):
        self.create_if_empty(user_id)
        user_pay_cur = self.users_dict[user_id].get('pay_cur')
        return user_pay_cur

    def get_get_cur(self, user_id):
        self.create_if_empty(user_id)
        user_get_cur = self.users_dict[user_id].get('get_cur')
        return user_get_cur

    def get_value_cur(self, user_id):
        self.create_if_empty(user_id)
        user_value_cur = self.users_dict[user_id].get('value_cur')
        return user_value_cur
