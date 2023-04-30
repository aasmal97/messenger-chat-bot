from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from utils.login import login_to_messenger
from utils.logout import logout
from utils.send_message_to_user import send_message_to_user
from utils.send_message_to_active_chat import send_message_to_active_chats
import argparse

driver = webdriver.Chrome(ChromeDriverManager().install())


def parse_args():
    parser = argparse.ArgumentParser(
        prog="Messenger Chat Bot", description="A bot that sends messages through facebook messenger"
    )
    # login args
    parser.add_argument("--email", type=str, help="Email of the user", required=True)
    parser.add_argument("--pw", type=str, help="Password of the user", required=True)
    parser.add_argument("--account_name", type=str, help="Name of the account", default=None)
    # send message args
    parser.add_argument("--message", type=str, help="Message to be sent", required=True)
    parser.add_argument("--message_type", type=str, help="Type of message to be sent", choices=["chat", "user"])
    parser.add_argument("--chat_or_user_name", type=str, help="Name of the chat/user", required=True, default=None)
    parser.add_argument("--chat_option_idx", type=str, help="Index of the chat to be sent after a search", default=None)
    return parser.parse_args()

def send_message(cmd_args: dict):
    login_driver = login_to_messenger(driver, email=cmd_args["email"], pw=cmd_args["pw"])
    if cmd_args["message_type"] == "chat":
        send_message_to_active_chats(
            driver=login_driver,
            message=cmd_args["message"],
            chat_option_idx=cmd_args["chat_option_idx"],
            search_term=cmd_args["chat_or_user_name"],
        )
    if cmd_args["message_type"] == "user":
        send_message_to_user(
            driver=login_driver,
            message=cmd_args["message"],
            chat_option_idx=cmd_args["chat_option_idx"],
            search_term=cmd_args["chat_or_user_name"],
        )
    logout(driver=login_driver)


if __name__ == "__main__":
    cmd_args = parse_args()
    cmd_dict = {
        "message_type": cmd_args.message_type,
        "chat_or_user_name": cmd_args.chat_or_user_name,
        "chat_option_idx": cmd_args.chat_option_idx,
        "message": cmd_args.message,
        "email": cmd_args.email,
        "pw": cmd_args.pw,
        "account_name": cmd_args.account_name,
    }
    send_message(cmd_dict)
