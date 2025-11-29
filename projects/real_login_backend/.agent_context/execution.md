
## Execution Result
```
Command: cd app && ls -la requirements.txt database.py models.py auth.py main.py
Stdout:
-rw-r--r--@ 1 abu  staff  1084 Nov 29 22:36 auth.py
-rw-r--r--@ 1 abu  staff   647 Nov 29 22:36 database.py
-rw-r--r--@ 1 abu  staff  3027 Nov 29 22:36 main.py
-rw-r--r--@ 1 abu  staff   710 Nov 29 22:36 models.py
-rw-r--r--@ 1 abu  staff    98 Nov 29 22:36 requirements.txt

Stderr:

```

## Execution Result
```
Command: cd app && pip install -r requirements.txt && uvicorn main:app --reload --host 0.0.0.0 --port 8000
Stdout:

Stderr:
/bin/sh: pip: command not found

```

## Execution Result
```
Command: cd app && curl -X 'POST' 'http://127.0.0.1:8000/register' -H 'Content-Type: application/json' -d '{"email":"test@example.com","password":"password123"}' && curl -X 'POST' 'http://127.0.0.1:8000/login' -H 'Content-Type: application/json' -d '{"email":"test@example.com","password":"password123"}'
Stdout:

Stderr:
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
curl: (7) Failed to connect to 127.0.0.1 port 8000 after 0 ms: Couldn't connect to server

```
