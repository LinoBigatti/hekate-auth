# Architecture description

## User authentication
1. User inputs username and password.
2. Frontend relays them to the auth script.
3. Auth script reads from hashes.json file.
4. It tries to get the entry which id corresponds to the username.
4.1 If nothing is found, return [False, None].
4.2 Else, proceed to step 5.
5. Compare password hash stored corresponds with the password hash sent.
5.1 If it does not match, return [False, None].
5.2 Else, proceed to step 6.
6. Generate a hash based on nanoseconds since epoch to use as a session token.
7. Return [True, token].

## Signing up
1. User inputs username and password.
2. Frontend relays them to the auth script.
3. Auth script checks if the username is taken.
3.1 If it is, return 1.
3.2 Else, proceed to step 4.
4. Auth script hashes password and appends username and hashed password to hashes.json.
5. Return 0.