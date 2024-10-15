from collections import deque

queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")
print(queue)

queue.popleft()
print(queue)