import csv, sys
import pandas as pd


#AddUser myname mypassword
def main():
    if(len(sys.argv)) != 3:
        return 'Missing user or password'
    
    name = sys.argv[1]
    password = sys.argv[2]

    users_table = pd.read_csv('./tables/users.csv', index_col='user')
    # print(users_table.at['ross', 'group'])
    # print(users_table.head())
    # print(idx.unique().values)
    users = users_table.index.values

    # search yields a result of an already existing user
    try:
        if name in users:
            raise ValueError()
    except ValueError:
        print('Error: User already exists')
        return

    tmp = pd.DataFrame(data={'password': [password]}, index= [name])
    users_table = users_table.append(tmp, sort=False)
    users_table.index.name = 'user'
    users_table.to_csv('./tables/users.csv')

    print('Sucess! User added.')

if __name__=='__main__':
    main()