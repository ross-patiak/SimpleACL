import sys
import pandas as pd
from operations import permissions_list


def main():
    if(len(sys.argv) == 3):
        operation = sys.argv[1]
        user = sys.argv[2]
        object_ = None
    elif(len(sys.argv) == 4):
        operation = sys.argv[1]
        user = sys.argv[2]
        object_ = sys.argv[3]
    else:
        return 'Error: Missing arguments. Arguments: operation user [object]'

    if operation not in permissions_list:
        print('Error: Invalid operation.')
        return

    # get permissions table
    permissions = pd.read_csv('./tables/permissions.csv', index_col='usergroupname')
    user_groups = pd.read_csv('./tables/groups.csv', index_col='groupname')
    object_groups = pd.read_csv('./tables/objects.csv', index_col='groupname')

    # find groups user belongs in
    user_groups.where(user_groups['user']==user, inplace = True)
    user_groups = user_groups.dropna()
    usergroup_list = user_groups.index.values

    # find groups object belongs in
    object_groups.where(object_groups['object']==object_, inplace = True)
    object_groups = object_groups.dropna()
    objectgroup_list = object_groups.index.values
    can_access = False

    # check if group lists are empty. if empty then user or object does not belong in a group
    if len(usergroup_list) == 0:
        print('Error: User does not belong in any usergroup')
        return
    elif object_ is not None and len(objectgroup_list) == 0:
        print('Error: Object does not belong in any objectgroup')
        return
    else:
        if object_ is None:
            for usergroup in usergroup_list:
                try:
                    tmp = permissions.loc[usergroup]
                    tmp.where(tmp['operation']==operation, inplace=True)
                    tmp2 = tmp['objectgroupname'].values
                    tmp2 = [x for x in list(tmp2) if isinstance(x, str)]

                    # if there is no instance where the operation is tied to another object(that is not null), grant access
                    if(not tmp2):
                        can_access = True
                        break
                except:
                    continue
        else:
            for usergroup in usergroup_list:
                for objectgroup in objectgroup_list:
                    try:
                        tmp = permissions.loc[usergroup]
                        filter1 = tmp['operation']==operation
                        filter2 = tmp['objectgroupname']==objectgroup
                        tmp.where(filter1 & filter2, inplace=True)
                        tmp = tmp.dropna()

                        if(tmp.empty is False):
                            can_access = True
                            break
                    except:
                        continue
                   
    if(can_access):
        print(user + ' can access this object.')
        return
    else:
        print(user + ' cannot access this object.')
        return


if __name__=='__main__':
    main()