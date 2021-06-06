from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep, time


def foo(t):
    sleep(t)


s = time()
for x in range(8):
    foo(0.5)
print("Total {}".format(time() - s))

task = []
executor = ThreadPoolExecutor(max_workers=8)

s = time()

for x in range(8):
    a = executor.submit(foo,0.5)
    task.append(a)

for t in task:
    while t.done() is False:
        pass

print("Total {}".format(time() - s))
