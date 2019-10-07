import json
import time
from pprint import pprint

from datetime import datetime
import requests

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
s = datetime.now()


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

    def groups_getbyid(self, gid):
        params = self.get_params()
        params['group_ids'] = gid
        params['fields'] = 'members_count'
        response = requests.get(
            F'{self.base_url}groups.getById',
            params
        )
        return response.json()

    def users_search(self, user_name):
        params = self.get_params()
        params['q'] = user_name
        response = requests.get(
            F'{self.base_url}users.search',
            params
        )
        # print(response.json())
        return response.json()

    def execute(self, code='return "Nothing set yet";'):
        params = self.get_params()

        params['code'] = code
        response = requests.get(
            F'{self.base_url}execute',
            params
        )
        return response.json()


user1 = User(TOKEN)
groups = []

dif_groups = []
mutual_groups = []


def enter_user():
    input_user = (input("Введите имя пользователя или его ИД: "))
    print(s)
    return input_user


def check_user(input_user):
    user_ids = int(user1.users_search(input_user)['response']['count'])
    if input_user.isdigit():
        cur_user = input_user
        print(f'current userID is {cur_user}')
        return cur_user
    else:
        if user_ids != 0:
            cur_user = int(user1.users_search(input_user)['response']['items'][0]['id'])
            print(f'current userID is {cur_user}')
            return cur_user
        else:
            raise ValueError


# getting groups of current user

def get_groups(cur_user):
    user_list = user1.user_list(cur_user)['response']['items']
    cur_groups = user1.get_groups(cur_user)['response']['items']
    count_users = len(user_list)
    print(f'user has {count_users} friends')
    print('user has ', len(cur_groups), ' groups')
    return user_list, cur_groups, count_users


# getting list of groups of friends

def friend_groups(user_list):
    counter = 0
    error_counts = 0
    for u in user_list:
        counter += 1
        if counter % 100 == 0:
            print(f'{counter} of {len(user_list)}')
        else:
            print('.', end='')
        time.sleep(0.35)
        get_group = user1.get_groups(u)
        for k in get_group.keys():
            # print(k)
            if k == 'response':
                for g in get_group['response']['items']:
                    if g not in groups:
                        groups.append(g)
            else:
                error_counts += 1
    print()
    print(f'{error_counts} friend restricted permission to view their groups')
    return groups


# extracting not matching groups

def compare(cur_groups, f_groups):
    for cg in cur_groups:
        if cg not in f_groups:
            dif_groups.append(cg)
        else:
            mutual_groups.append(cg)
    print()
    print(f' rest of friends has {len(groups)} groups')
    pprint(f'unique groups are{dif_groups} and total is {len(dif_groups)}')
    pprint(f'mutual groups are {mutual_groups} and total is {len(mutual_groups)}')


def write_results(dif_groups_list):
    time.sleep(1)
    y = '{0:%Y%m%d-%H%M}'.format(s)
    groups_info = user1.groups_getbyid(str(dif_groups_list).strip('[]'))
    with open(f'groups{y}.json', 'w+', encoding='utf-8') as data:
        json.dump(groups_info, data)
        pprint('feel free to check out thr result in  groups.json')


def main():
    cuf, cug, cou = get_groups(check_user(enter_user()))
    fg = friend_groups(cuf)
    compare(cug, fg)


if __name__ == '__main__':
    try:
        main()
    except ValueError:
        print('entered userID or login has not found in VK, please try one more time ')
    finally:
        write_results(dif_groups)
        e = datetime.now()
        print(e)
        print(e - s)
