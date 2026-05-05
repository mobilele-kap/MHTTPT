from collections import deque


class LimitedQueue:
    def __init__(self, max_size):
        """
        Инициализация очереди с ограниченным размером.

        Args:
            max_size (int): максимальный размер очереди
        """
        if max_size <= 0:
            raise ValueError("Размер очереди должен быть больше 0")
        self.max_size = max_size
        self.queue = deque(maxlen=max_size)

    def put(self, item):
        """
        Добавление элемента в очередь.
        Если очередь переполнена, самый старый элемент удаляется автоматически.

        Args:
            item: элемент для добавления
        """
        self.queue.append(item)

    def get(self):
        """
        Получение самого старого элемента из очереди.

        Returns:
            элемент из начала очереди

        """
        if self.is_empty():
            return None
        return self.queue.popleft()

    def peek(self):
        """
        Просмотр самого старого элемента без удаления.

        Returns:
            элемент из начала очереди

        """
        if self.is_empty():
            return None
        return self.queue[0]

    def is_empty(self):
        """Проверка, пуста ли очередь."""
        return len(self.queue) == 0

    def is_full(self):
        """Проверка, заполнена ли очередь."""
        return len(self.queue) == self.max_size

    def size(self):
        """Текущий размер очереди."""
        return len(self.queue)

    def clear(self):
        """Очистка очереди."""
        self.queue.clear()

    def to_list(self):
        """Возвращает очередь в виде списка (от самого старого к новому)."""
        return list(self.queue)

    def __str__(self):
        return f"LimitedQueue({list(self.queue)})"

    def __len__(self):
        return len(self.queue)