import csv, sys
import pandas as pd

# to do: output all users in a specific group, check if group exists

def main():
    if(len(sys.argv)) != 3:
        return 'Missing user or groupname'
    
    name = sys.argv[1]
    group = sys.argv[2]

    users_table = pd.read_csv('./tables/users.csv', index_col='user')
    users = users_table.index.values

    # if user exists
    try:
        if name not in users:
            raise ValueError()
    except ValueError:
        print('Error: User does not exist.')
        return

    # get groups
    group_table = pd.read_csv('./tables/groups.csv', index_col='groupname')

    # tmp is a way to check if a group exists
    try:
        tmp = group_table.loc[group]
    except:
        tmp = None


    # group_users are list of users in group
    try:
        group_users = tmp['user'].values
    except:
        if tmp is not None:
            group_users = tmp['user']
        else:
            group_users = []
    
    #if user is in the list, task accomplished
    if name in group_users:
        print('Success! User already in group.')
        return
    else:
        # else add it to entire dataframe
        data = pd.DataFrame(data={'user': [name]}, index=[group])
        group_table = group_table.append(data, sort=False)
        group_table.index.name = 'groupname'
        tmp = group_table.loc[group]

    group_table.to_csv('./tables/groups.csv')
    print('Success! User added.\n\nUsers in ' + group + ':')

    # update users list
    try:
        group_users = list(tmp['user'].values)
    except:
        group_users = [tmp['user']]

    # print users in group
    groupstr = str(group_users)[1:-1]
    print(groupstr.replace(',', '\n'))

if __name__=='__main__':
    main()