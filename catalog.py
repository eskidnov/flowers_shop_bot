# -*- coding: utf-8 -*-


def hash(astring, tablesize=10000000000000000000):
    sum = 0
    for pos in range(len(astring)):
        sum = sum + ord(astring[pos])

    return sum%tablesize


class Catalog:

    # def __init__(self, item, *categories):
    #     self.text = item
    #     self.categories = {text : subcats for (text, subcats) in categories}

    def __init__(self, item, categories=None):
        self.item = item
        if isinstance(categories, list) or categories==None:
            self.categories = categories
        else:
            print('Неверный формат категорий')
            self.categories = None

    def __view(self, all_categories):
        # print (self.item, self.categories)
        if not self.categories or isinstance(self.categories[0], str):
            return
        all_categories.append(str(hash(self.item)))
        for subcat in self.categories:
            #if not subcat.categories:
                subcat.__view(all_categories)

    def get_all_categories(self):
        all_categories = []
        self.__view(all_categories)
        return all_categories

    def find(self, category):
        print(self.item)
        if str(hash(self.item)) == category or not self.categories or isinstance(self.categories[0], str):
            return self
        for subcat in self.categories:
            a = subcat.find(category)
            if a is None or isinstance(self.categories[0], str):
                continue
            if str(hash(a.item)) == category:
                return a
        return None


    def __items(self, all_items):
        if not self.categories or isinstance(self.categories[0], str):
            all_items.append(self.item)
            return
        for subcat in self.categories:
            subcat.__items(all_items)

    def get_all_items(self):
        all_items = []
        self.__items(all_items)
        return all_items

    def find_item(self, item):
        pass# if self.item == item
    
    def to_str(self, shift=0):
        ans = ' ' * shift + self.item +  ' {\n'
        if not isinstance(self.categories[0], Catalog):
            ans += str(self.categories)
        else:
            for son in self.categories:
                ans += son.to_str(shift + 2)
        ans += '}\n'
        return ans

    def __str__(self):
        return self.to_str(0)