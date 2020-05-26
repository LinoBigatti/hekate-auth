# Architecture description

## User authentication
1. User inputs username and password.
2. They are hashed before being send out to the frontend.
3. Frontend relays them to the auth script.
4. Auth script reads from SHAs.json file.
5. It tries to get the entry which id corresponds to the username hash.
5.1 If nothing is found, return [False, None].
5.2 Else, proceed to step 6.
6. Compare password hash stored corresponds with the password hash sent.
6.1 If it does not match, return [False, None].
6.2 Else, proceed to step 7.
7. Generate a random 64-bit number to use as a session token.
8. Return [True, token].
