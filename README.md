# Asura - Server app
Server app for Asura app.

## 🍔 Ingredients
- Django
- Python 3

## 🏈 Build the damn project
### Activate the virtual environment
Navigate to the project root folder, then run the following command (MacOS).
```
source venv/bin/activate
```

### Initialize the database
Run the following command to initialize the database (if not created).
```
python3 manage.py migrate
```

### Run the project
Run the following command to run the server.
```
python3 manage.py runserver
```

## What's on the menu?
### Hello
Simple GET request used for debugging.
```
GET 127.0.0.1/hello/
```

### List users
List multiple users' basic info.
```
GET 127.0.0.1/users/
```

### Sign up
Signs a user up, used for account creation.
```
POST 127.0.0.1/users/
```

### Sign in
Signs a user in.
```
POST 127.0.0.1/users/signin
```

### User search
Search for users based on a keyword.
```
POST 127.0.0.1/users/search/<KEYWORD>
```

### View basic profile
Returns the basic information of a user.
```
GET 127.0.0.1/users/profile/basic
```
or
```
GET 127.0.0.1/users/profile/basic/<UUID>
```

### Update basic profile info
Updates the basic information of a user.
```
POST 127.0.0.1/users/profile/basic
```

### Update password
Updates the password of a user.
```
POST 127.0.0.1/users/password/update
```

### Send message
Sends a message to another user.
```
POST 127.0.0.1/message/send
```

### See conversations
Display all conversations (header) of a user.
```
GET 127.0.0.1/conversations/
```

### See messages
Shows a conversation messages.
```
GET 127.0.0.1/messages/<uuid>
```

### Identify user from token
Retrieves one user's information from their token (even expired).
Used for debbuging.
```
GET 127.0.0.1/token/identify/<key>
```

### Generates new token
Obtain a new valid token from another one.
```
GET 127.0.0.1/token/renew
```
