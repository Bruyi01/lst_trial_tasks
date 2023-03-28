import asyncio
import json
import sys
import asyncssh


class AsyncTask():

    def __init__(self):
        self.hosts_data = None

    def readFromJsonFile(self):
        return json.loads('hosts.json')['hosts']

    async def takeDataFromClient(self, server, user, userpass):
        async with asyncssh.connect(server, username=user, password=userpass) as conn:
            result = (await conn.run('cd ~/bw/ ; git branch -vv', check=True)).split(' ')[:2]
            if result.startwith('fatal'):
                client_data_branch = await conn.run('cd ~/bw/ ; svn info | grep ^Revision',
                                                    check=True).split(': ')[1]
                client_data_revision = await conn.run('cd ~/bw/ ; svn info | grep ^Last Changed Rev',
                                                      check=True).split(': ')[1]
            else:
                client_data_branch = {'branch': result.split(' ')[0]}
                client_data_revision = {'revision': result.split(' ')[1]}
        return client_data_branch, client_data_revision

    def fillDataFromHosts(self):
        hosts_data = self.readFromJsonFile()
        try:
            for item in hosts_data:
                branch, revision = asyncio.get_event_loop().run_until_complete(self.takeDataFromClient(item['host'],
                                                                                                       item['user'],
                                                                                                       item['password']))
                item.set(branch)
                item.set(revision)
        except (OSError, asyncssh.Error) as exc:
            sys.exit(f'SSH connection failed: {str(exc)}')
        with open('hosts.json', 'w') as full_data_file:
            full_data_file.write(hosts_data)
            full_data_file.close()


def main():

    ...


if __name__ == '__main__':
    main()
