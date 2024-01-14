from scr.common import get_llm_response


class Player:
    def __init__(self, zh_name, role_script, chat_setting):
        self.zh_name = zh_name
        self.role_script = role_script
        self.chat_setting = chat_setting
        self.conversation_id = None
        self.response_history = {}
        self.input_history = {}
        self.sync_time = -1

    def play(self, following_plot):
        if self.conversation_id is None:
            answer, self.conversation_id = get_llm_response(following_plot)
        else:
            answer, _ = get_llm_response(following_plot, self.conversation_id)
        self.input_history[self.sync_time] = following_plot
        self.response_history[self.sync_time] = answer
        return answer

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
        return self.response_history[time]

    def has_been_update(self, system_time):
        if system_time == self.sync_time:
            return True
        elif system_time > self.sync_time:
            return False
        else:
            raise ValueError("系统时间存在问题！")
