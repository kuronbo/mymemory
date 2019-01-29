import os
from functools import lru_cache


class Category:
    def __init__(self):
        self.id_values = {}

        path = os.path.join(os.path.dirname(__file__), 'category.cnf')
        with open(path, encoding='utf-8') as f:
            for line in f.readlines():
                id, name, color = line.strip().split(',')
                self.id_values[id] = (name, color)

    @lru_cache()
    def lookup_by_id(self, id):
        return self.id_values.get(id)

    @lru_cache()
    def lookup_by_name(self, name):
        for k, values in self.id_values.items():
            if values[0] == name:
                return id
