import json
import time
from pprint import pprint

import requests

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'


class User:

    def __init__(self, access_token):
        self.access_token = access_token
        self.base_url = 'https://api.vk.com/method/'

    def get_params(self):
        return {
            'access_token': self.access_token,
            'v': 5.101
        }

    def user_list(self, user_id):
        params = self.get_params()
        params['user_id'] = user_id
        params['count'] = 1000
        response = requests.get(
            F'{self.base_url}friends.get',
            params
        )
        return response.json()

    def get_groups(self, user_id):
        params = self.get_params()
        params['user_id'] = user_id
        response = requests.get(
            F'{self.base_url}groups.get',
            params
        )
        return response.json()

    exec("""
def groups_getById(self,gid):
    params = self.get_params()
    params['group_ids'] = gid
    params['fields'] = 'members_count'
    response = requests.get(
        F'{self.base_url}groups.getById',
        params
    )
    return response.json()
        """)

    def users_search(self, user_name):
        params = self.get_params()
        params['q'] = user_name
        response = requests.get(
            F'{self.base_url}users.search',
            params
        )
        # print(response.json())
        return response.json()


if __name__ == '__main__':
    try:
        counter = 0
        user1 = User(TOKEN)
        input_user = (input("Введите имя пользователя или его ИД: "))
        if input_user.isdigit():
            cur_user = input_user
            print(f'current userID is {cur_user}')
        else:
            if int(user1.users_search(input_user)['response']['count']) != 0:
                cur_user = int(user1.users_search(input_user)['response']['items'][0]['id'])
                print(f'current userID is {cur_user}')
            else:
                raise ValueError

        user_list = user1.user_list(cur_user)['response']['items']
        groups = []
        error_counts = 0

        # getting groups of current user
        cur_groups = user1.get_groups(cur_user)['response']['items']
        count_users = len(user_list)
        print(f'user has {count_users} friends')
        dif_groups = []
        mutual_groups = []
        print('user has ', len(cur_groups), ' groups')
        # getting list of groups of friends

        exec("""
for u in user_list:
    counter += 1
    if counter % 100 == 0:
        print(f'{counter} of {count_users}')
    else:
        print('.', end='')
    get_group = user1.get_groups(u)
    for k in get_group.keys():
        # print(k)
        if k == 'response':
            for g in get_group['response']['items']:
                if g not in groups:
                    groups.append(g)
        else:
            error_counts += 1
            """)

        # extracting not matching groups
        for cg in cur_groups:
            if cg not in groups:
                dif_groups.append(cg)
            else:
                mutual_groups.append(cg)

        # pprint(groups)
        print()
        print(f'{error_counts} friend restricted permission to view their groups')
        print(f' rest of friends has {len(groups)} groups')
        pprint(f'unique groups are{dif_groups} and total is {len(dif_groups)}')
        pprint(f'mutual groups are {mutual_groups} and total is {len(mutual_groups)}')
        # dif_groups = [134709480, 8564, 101522128, 27683540]
        time.sleep(1)
        exec("groups_info = user1.groups_getById(str(dif_groups).strip('[]'))")
        # groups_info = user1.groups_getById(str(dif_groups).strip('[]'))
        with open('groups.json', 'w+', encoding='utf-8') as data:
            json.dump(groups_info, data)

        print('')
        pprint('feel free to check out thr result in  groups.json')
    except ValueError:
        print('entered userID or login has not found in VK, please try one more time ')
