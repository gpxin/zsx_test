class ControllablePlayer:
    def __init__(self, zh_name, role_script, rival_player):
        self.zh_name = zh_name
        self.role_script = role_script
        self.rival_player = rival_player
        self.input_history = {}
        self.response_history = {}
        self.sync_time = 1
        self.response_ready = True

    def play(self, user_input):
        self.input_history[self.sync_time] = user_input
        self.response_ready = False

    def response(self, response, chat_turn):
        self.response_history[self.sync_time] = response
        self.response_ready = True
        self.sync_time += chat_turn

    @property
    def history_response(self):
        response_list = [input_str for time_step, input_str in self.response_history.items()]
        return "\n".join(response_list)

    @property
    def last_response(self):
        if not self.response_history:
            return ""
        max_time = max(list(self.response_history.keys()))
        return self.response_history[max_time]

    def get_time_response(self, time):
        return self.response_history[time]

    @property
    def history_input(self):
        input_list = [input_str for time_step, input_str in self.input_history.items()]
        return "\n".join(input_list)

    @property
    def last_input(self):
        if not self.input_history:
            return ""
        max_time = max(list(self.input_history.keys()))
        return self.input_history[max_time]

    def get_time_input(self, time):
        return self.input_history[time]

    def has_been_update(self, system_time):
        # 对于ControllablePlayer来说，其他人对象依赖的是其输入
        if system_time in self.input_history:
            return True
        else:
            return False
