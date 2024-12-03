import os
import sys

if sys.platform == "win32":
    import wexpect as pexpect
else:
    import pexpect

from dotenv import load_dotenv

load_dotenv()
proxy_hosts = os.getenv("PROXY_HOSTS", "").split(",")
proxy_username = os.getenv("PROXY_USERNAME")
proxy_password = os.getenv("PROXY_PASSWORD")

dev_hosts = os.getenv("DEV_WAS_HOSTS", "").split(",")
dev_username = os.getenv("DEV_WAS_USERNAME")
dev_password = os.getenv("DEV_WAS_PASSWORD")

prd_hosts = os.getenv("PRD_WAS_HOSTS", "").split(",")
prd_username = os.getenv("PRD_WAS_USERNAME")
prd_password = os.getenv("PRD_WAS_PASSWORD")

qa_hosts = os.getenv("QA_WAS_HOSTS", "").split(",")
qa_username = os.getenv("QA_WAS_USERNAME")
qa_password = os.getenv("QA_WAS_PASSWORD")


def ssh_command(user, host, proxy_user=None, proxy_host=None):
    if proxy_user and proxy_host:
        return f"ssh -o StrictHostKeyChecking=no -o ProxyJump={proxy_user}@{proxy_host} {user}@{host}"
    else:
        return f"ssh -o StrictHostKeyChecking=no {user}@{host}"


def wait_password(user, host):
    return f"{user}@{host}'s password:"


def run_ssh(env_name, host_index):
    host_num = int(host_index) - 1
    try:
        if env_name == "prd":
            proxy_host = proxy_hosts[1]
            final_host = prd_hosts[host_num]
            final_username = prd_username
            final_password = prd_password

        elif env_name == "qa":
            proxy_host = proxy_hosts[1]
            final_host = qa_hosts[host_num]
            final_username = qa_username
            final_password = qa_password
        else:
            proxy_host = proxy_hosts[0]
            final_host = dev_hosts[host_num]
            final_username = dev_username
            final_password = dev_password

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


if __name__ == "__main__":
    env_name = "dev"
    server_number = 1
    if len(sys.argv) == 3:
        env_name = sys.argv[1]
        server_number = sys.argv[2]
    elif len(sys.argv) == 2:
        env_name = sys.argv[1]

    run_ssh(env_name, server_number)
