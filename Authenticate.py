import sys,re
import pandas as pd

def password_check(password, UserName):

    # calculate the length of the password
    length = (len(password) > 8)

    # search for lowercase
    lowercase = re.search(r"[a-z]", password)

    # search for uppercase
    uppercase = re.search(r"[A-Z]", password)

    # search for digits
    digit = re.search(r"\d", password)

    # search for symbols
    symbol = re.search(r"\W", password)

    # search for name
    name = password.find(UserName) == -1

    password_ok = (length and digit and uppercase and lowercase and symbol and name)

    return password_ok


def main():
    if(len(sys.argv)) != 3:
        return 'Missing user or password'
    
    name = sys.argv[1]
    password = sys.argv[2]

    users_table = pd.read_csv('./tables/users.csv', index_col='user')
    users = users_table.index.values

    # check if ya boy exists
    if name not in list(users):
        print('Error: User does not exist')
        return

    # tmp = users_table.loc['ross', 'password']

    authenticate = password_check(password, name)

    if(authenticate):
        print('Authenticated. Password is ok.')
    else:
        print('Failure: bad password')
    return


if __name__=='__main__':
    main()