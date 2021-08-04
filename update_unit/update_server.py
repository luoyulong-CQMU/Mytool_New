import os

q = os.popen('python -m http.server 5002')
d = q.read()
print(d)