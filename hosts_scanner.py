import asyncio
import json
import os
import paramiko
import sys
import asyncssh


class AsyncTask():

    def __init__(self):
        self.hosts_data = None

    def readFromJsonFile(self):
        hosts_data = json.loads('hosts.json')
        return hosts_data['hosts']

    async def takeGitDataFromClient(self, server, user, userpass):
        async with asyncssh.connect(server, username=user, password=userpass) as conn:
            result = (await conn.run('cd ~/bw/ ; git branch -vv', check=True)).split(' ')[:2]
            if result.startwith('fatal'):
                result = await conn.run('cd ~/bw/ ; svn info', check=True)
                """
                добавить фильтр на входные значения
                """
            repos_data_branch = {'branch': result.split(' ')[0]}
            repos_data_revision = {'revision': result.split(' ')[1]}
        return repos_data_branch, repos_data_revision

    async def takeSubVersionDatafromClient(self, server, user, userpass):
        async with asyncssh.connect(server, username=user, password=userpass) as conn:
            result = await conn.run('cd ~/bw/ ; svn info', check=True)
            return result

    ...


"""
    async def sshClient(self, host, username, passwd, command):
        async with asyncssh.connect(host, username=username, password=passwd, known_hosts=None) as conn:
            return await conn.run(command, check=True)

    async def multi_client(self, list_input):
        hosts = list_input

        tasks = (AsyncTask.sshClient(host, 'show ver') for host in hosts)
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for dev, result in enumerate(results, 1):
            file = open(hosts[dev - 1] + '.json', 'w+')
            if isinstance(result, Exception):
                print('Task %d failed: %s' % (dev, str(result)))
            elif result.exit_status != 0:
                print('Task %d exited with status %s:' % (dev, result.exit_status))
                print(result.stderr, end='')
            else:
                print('Task %d succeeded for device %s:' % (dev, hosts[dev - 1]))
                # print(result.stdout + '\n', end='')
                file.write(result.stdout + '\n')

            print(25 * '#')
"""


def main():
    """
    devs = ['dev1', 'dev2']
    cmds = ['show mod', 'show ver']

    passwd = getpass.getpass("passwd: ")
    startTime = datetime.now()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(AsyncTask.multi_client(devs))
    print('\nElapsed: ', datetime.now() - startTime)
    """

    ...


if __name__ == '__main__':
    main()
