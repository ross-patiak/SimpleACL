import sys
import pandas as pd
from operations import permissions_list


def main():
    if(len(sys.argv) == 3):
        operation = sys.argv[1]
        usergroup = sys.argv[2]
        objectgroup = None
    elif(len(sys.argv == 4)):
        operation = sys.argv[1]
        usergroup = sys.argv[2]
        objectgroup = sys.argv[3]
    else:
        return 'Error: Missing arguments. Arguments: operation usergroupname [objectgroupname]'

    if operation not in permissions_list:
        print('Error: Invalid operation.')
        return

    # get permissions table
    permissions = pd.read_csv('./tables/permissions.csv', index_col='usergroupname')
    groups = pd.read_csv('./tables/groups.csv', index_col='groupname')

    # check if usergroup exists
    try:
        groups.loc[usergroup]
    except:
        print('Error: usergroup does not exist.')
        return

    # # group_objects are list of objects in group
    # try:
    #     group_users = tmp['object'].values
    # except:
    #     group_users = [tmp['object']]
    
    # if usergroup exists, add permissions
    data = pd.DataFrame(data={'operation': [operation], 'objectgroupname': [objectgroup]}, index=[usergroup])
    permissions = permissions.append(data, sort=False)
    permissions.index.name = 'usergroupname'

    # write to table
    permissions.to_csv('./tables/permissions.csv')
    print('Success! '+usergroup + ' has permission to !' + operation)


if __name__=='__main__':
    main()