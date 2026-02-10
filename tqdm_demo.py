import time

def test(n):
    for i in range(n):
        print(f"Hi {i}")
        yield i

for i in test(5):
    time.sleep(0.05)
    print(i)
