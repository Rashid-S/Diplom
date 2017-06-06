import requests
import json
import time


def get_params():
    """
    Формироваине параметров для запросов
    """
    version = '5.64'
    access_token = "d13e692be69592b09fd22c77a590dd34e186e6d696daa88d6d981e1b4e296b14acb377e82dcbc81dc0f22"  # token
    params = {'access_token': access_token,
              'v': version,
              }
    return params


def print_process():
    """
    Показ процесса работы 
    """
    print('.')


def make_request(url, params):
    """
    Отправка запроса
    """
    print_process()
    attempts = 0
    while True:
            response = requests.get(url, params)
            if response.ok:
                response_list = response.json()
                if 'response' in response_list:
                    return response_list
                else:
                    attempts += 1
                    if attempts == 3:
                        print('END')
                        exit()
            time.sleep(0.5)


def get_users_is_members(params, friends_list):
    """
    Является ли пользователь из списка друзей подписчиком группы
    """
    final_list = []
    init_start = 0
    pause = 250
    list_user_ids = params['user_ids'].split(', ')
    while list_user_ids[init_start:pause]:
        params['user_ids'] = str(friends_list['response']['items'][init_start:pause])[1:-1]
        init_start = pause
        pause += 250
        members = make_request('https://api.vk.com/method/groups.isMember', params)
        for member in members['response']:
            final_list.append(member)
    return final_list


def get_group_without_user_friends(params, groups_list, friends_list):
    """
    Формируем лист_групп пользователя в которые не входят ни один из его друзей 
    """
    user_alone = []
    for group in groups_list['response']['items']:
        params['group_id'] = group['id']
        params['user_ids'] = str(friends_list['response']['items'])[1:-1]
        members_group = get_users_is_members(params, friends_list)
        flag = False  # установка флага по умолчанию Не истина
        for member in members_group:
            if member['member'] == 1:
                flag = True
                break
        if not flag:
            params['group_id'] = group['id']
            str_dict = {'name': group['name'], 'gid': group['id'],
                        'members_count': make_request('https://api.vk.com/method/groups.getMembers',
                                                      params)['response']['count']}
            user_alone.append(str_dict)
    return user_alone


def save_json(data):
    """
    Сохранение файла в json
    """
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        print(len(data))


def main():
    params = get_params()
    params['user_id'] = 5030613
    friends_list = make_request('https://api.vk.com/method/friends.get', params)
    params['extended'] = 1
    groups_list = make_request('https://api.vk.com/method/groups.get', params)
    data = get_group_without_user_friends(params, groups_list, friends_list)
    save_json(data)


if __name__ == '__main__':
    main()
