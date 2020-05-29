# Architecture description

## User authentication

1. User inputs username and password.
2. Password is hashed via sha256.
3. Frontend relays them to the auth script.
4. Auth script reads from hashes.json file.
5. It tries to get the entry which id corresponds to the username.
	1. If nothing is found, return 1.
	2. Else, proceed to step 6.
6. Compare password's argon2 hash stored corresponds with the password hash sent.
	1. If it does not match, return 1.
	2. Else, proceed to step 7.
7. Generate an argon2 hash based on nanoseconds since epoch to use as a session token.
8. Return the token.

## Signing up

1. User inputs username and password.
2. Password gets hashed via sha256
3. Frontend relays them to the auth script.
4. Auth script checks if the username is taken.
	1. If it is, return 2.
	2. Else, proceed to step 4.
5. Auth script checks if the password is in the most common passwords.
	1. If thats true, return 3.
	2. Else, continue to step 6
6. Auth script hashes password and appends username and hashed password to hashes.json.
7. Return 0.

## Server

1. Server receives the request.
	1. If its GET, go to step 3.
	2. If its POST, continue to step 2.
2. Check for operation number.
	1. If its 0, send name and password and go to user authentication.
		1. If it returns 1, the password or the username are incorrect. Send a 403 error, accompanied of a description.
		2. Else, send a 200 and return the token.
	2. If its 1, send name and password and go to sign up.
		1. If it returns 0, it was successfull. Send a 200 code and inform the user.
		2. If it returns 2, the username is taken. Send a 403 error, accompanied of a description.
		3. If it returns 3, the password is too common. Send a 403 error together with a description.
	3. If its nor 0 or 1, send a 501 error.
	4. If its not a number, send a 400 error and go to step 3.
3. Display the help message.