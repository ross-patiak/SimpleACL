import csv, sys
import pandas as pd

# to do: output all users in a specific group, check if group exists

def main():
    if(len(sys.argv)) != 3:
        return 'Missing objectname or objectgroupname'
    
    name = sys.argv[1]
    group = sys.argv[2]

    # get groups
    group_table = pd.read_csv('./tables/objects.csv', index_col='groupname')

    # tmp is a way to check if a group exists
    tmp = None
    try:
        tmp = group_table.loc[group]
    except:
        pass

    # group_objects are list of objects in group
    try:
        group_objects = tmp['object'].values
    except:
        if tmp is not None:
            group_objects = tmp['object']
        else:
            group_objects = []
    
    #if object is in the list, task accomplished
    if name in group_objects:
        print('Success! Object already in group.')
        return
    else:
        # else add it to entire dataframe
        data = pd.DataFrame(data={'object': [name]}, index=[group])
        group_table = group_table.append(data, sort=False)
        group_table.index.name = 'groupname'
        tmp = group_table.loc[group]

    group_table.to_csv('./tables/objects.csv')
    print('Success! Object added.\n\nObjects in ' + group + ':')

    # update objects list
    try:
        group_objects = list(tmp['object'].values)
    except:
        group_objects = [tmp['object']]

    # print objects in group
    groupstr = str(group_objects)[1:-1]
    print(groupstr.replace(',', '\n'))

if __name__=='__main__':
    main()