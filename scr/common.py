import json
from pathlib import Path

import requests

PROJECT_PATH = Path(__file__).parent


def get_llm_response(query, conversation_id=""):
    # return "测试", 123
    response = requests.post(
        url=r"https://api.dify.ai/v1/chat-messages",
        headers={"Authorization": "Bearer app-v4HBS8GOdOQAaOmWbvfa20Hk", "Content-Type": "application/json"},
        json={
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "conversation_id": conversation_id,
            "user": "abc-123",
        },
    )
    conversation_id = json.loads(response.content)["conversation_id"]
    answer = json.loads(response.content)["answer"].strip()
    return answer, conversation_id


def get_merged_plot(plot_dict):
    following_plot = r""
    for player, lines in plot_dict:
        following_plot += f"{player}: {lines} \n"
    return following_plot


def make_start_conversation(user_role, system_role):
    return f"现在，我扮演的是{user_role},你需要扮演{system_role}"
