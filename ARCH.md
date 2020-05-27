# Architecture description

## User authentication
1. User inputs username and password.
2. Password is hashed via sha256.
3. Frontend relays them to the auth script.
4. Auth script reads from hashes.json file.
5. It tries to get the entry which id corresponds to the username.
5.1 If nothing is found, return [False, None].
5.2 Else, proceed to step 6.
6. Compare password's argon2 hash stored corresponds with the password hash sent.
6.1 If it does not match, return [False, None].
6.2 Else, proceed to step 7.
7. Generate an argon2 hash based on nanoseconds since epoch to use as a session token.
8. Return [True, token].

## Signing up
1. User inputs username and password.
2. Password gets hashed via sha256
3. Frontend relays them to the auth script.
4. Auth script checks if the username is taken.
4.1 If it is, return 1.
4.2 Else, proceed to step 4.
5. Auth script checks if the password is in the most common passwords.
5.1 If thats true, return 2.
5.2 Else, continue to step 6
6. Auth script hashes password and appends username and hashed password to hashes.json.
7. Return 0.