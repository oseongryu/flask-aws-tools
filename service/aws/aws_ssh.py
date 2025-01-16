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

dev_api_hosts = os.getenv("DEV_API_HOSTS", "").split(",")
dev_api_username = os.getenv("DEV_API_USERNAME")
dev_api_password = os.getenv("DEV_API_PASSWORD")

dev_web_hosts = os.getenv("DEV_WEB_HOSTS", "").split(",")
dev_web_username = os.getenv("DEV_WEB_USERNAME")
dev_web_password = os.getenv("DEV_WEB_PASSWORD")

dev_was_hosts = os.getenv("DEV_WAS_HOSTS", "").split(",")
dev_was_username = os.getenv("DEV_WAS_USERNAME")
dev_was_password = os.getenv("DEV_WAS_PASSWORD")

prd_api_hosts = os.getenv("PRD_API_HOSTS", "").split(",")
prd_api_username = os.getenv("PRD_API_USERNAME")
prd_api_password = os.getenv("PRD_API_PASSWORD")

prd_web_hosts = os.getenv("PRD_WEB_HOSTS", "").split(",")
prd_web_username = os.getenv("PRD_WEB_USERNAME")
prd_web_password = os.getenv("PRD_WEB_PASSWORD")

prd_was_hosts = os.getenv("PRD_WAS_HOSTS", "").split(",")
prd_was_username = os.getenv("PRD_WAS_USERNAME")
prd_was_password = os.getenv("PRD_WAS_PASSWORD")

qa_api_hosts = os.getenv("QA_API_HOSTS", "").split(",")
qa_api_username = os.getenv("QA_API_USERNAME")
qa_api_password = os.getenv("QA_API_PASSWORD")
qa_web_hosts = os.getenv("QA_WEB_HOSTS", "").split(",")
qa_web_username = os.getenv("QA_WEB_USERNAME")
qa_web_password = os.getenv("QA_WEB_PASSWORD")
qa_was_hosts = os.getenv("QA_WAS_HOSTS", "").split(",")
qa_was_username = os.getenv("QA_WAS_USERNAME")
qa_was_password = os.getenv("QA_WAS_PASSWORD")


def ssh_command(user, host, proxy_user=None, proxy_host=None):
    if proxy_user and proxy_host:
        return f"ssh -o StrictHostKeyChecking=no -o ProxyJump={proxy_user}@{proxy_host} {user}@{host}"
    else:
        return f"ssh -o StrictHostKeyChecking=no {user}@{host}"


def wait_password(user, host):
    return f"{user}@{host}'s password:"


def run_ssh(env_name, host_index, service_name):
    host_num = int(host_index) - 1
    try:
        if env_name == "prd":
            proxy_host = proxy_hosts[1]
            if service_name == "api":
                final_host = prd_api_hosts[host_num]
                final_username = prd_api_username
                final_password = prd_api_password
            elif service_name == "web":
                final_host = prd_web_hosts[host_num]
                final_username = prd_web_username
                final_password = prd_web_password
            elif service_name == "was":
                final_host = prd_was_hosts[host_num]
                final_username = prd_was_username
                final_password = prd_was_password


        elif env_name == "qa":
            proxy_host = proxy_hosts[1]
            if service_name == "api":
                final_host = qa_api_hosts[host_num]
                final_username = qa_api_username
                final_password = qa_api_password
            elif service_name == "web":
                final_host = qa_web_hosts[host_num]
                final_username = qa_web_username
                final_password = qa_web_password
            elif service_name == "was":
                final_host = qa_was_hosts[host_num]
                final_username = qa_was_username
                final_password = qa_was_password
        else:
            proxy_host = proxy_hosts[0]
            if service_name == "api":
                final_host = dev_api_hosts[host_num]
                final_username = dev_api_username
                final_password = dev_api_password
            elif service_name == "web":
                final_host = dev_web_hosts[host_num]
                final_username = dev_web_username
                final_password = dev_web_password
            elif service_name == "was":
                final_host = dev_was_hosts[host_num]
                final_username = dev_was_username
                final_password = dev_was_password

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
    service_name = "was"
    if len(sys.argv) == 4:
        env_name = sys.argv[1]
        server_number = sys.argv[2]
        service_name = sys.argv[3]
    if len(sys.argv) == 3:
        env_name = sys.argv[1]
        server_number = sys.argv[2]
    elif len(sys.argv) == 2:
        env_name = sys.argv[1]

    run_ssh(env_name, server_number, service_name)
