import os

import pexpect
from dotenv import load_dotenv

load_dotenv()
proxy_host = os.getenv("PROXY_HOST")
proxy_username = os.getenv("PROXY_USERNAME")
proxy_password = os.getenv("PROXY_PASSWORD")

final_host = os.getenv("DEV_WAS1_HOST")
final_username = os.getenv("DEV_WAS_USERNAME")
final_password = os.getenv("DEV_WAS_PASSWORD")


def ssh_command(user, host, proxy_user=None, proxy_host=None):
    if proxy_user and proxy_host:
        return f"ssh -o ProxyJump={proxy_user}@{proxy_host} {user}@{host}"
    else:
        return f"ssh {user}@{host}"


def wait_password(user, host):
    return f"{user}@{host}'s password:"


try:
    # Connect to the final host through the proxy
    child = pexpect.spawn(ssh_command(final_username, final_host, proxy_username, proxy_host))
    child.setwinsize(400, 400)

    # Handle proxy password prompt
    child.expect(wait_password(proxy_username, proxy_host), timeout=10)
    child.sendline(proxy_password)

    # Handle final host password prompt
    child.expect(wait_password(final_username, final_host), timeout=10)
    child.sendline(final_password)

    child.interact()
    child.close()
except pexpect.TIMEOUT:
    print("Connection timed out.")
