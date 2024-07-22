# Создайте класс WarehouseManager - менеджера склада, который будет обладать следующими свойствами:
# Атрибут data - словарь, где ключ - название продукта, а значение - его кол-во. (изначально пустой)
# Метод process_request - реализует запрос (действие с товаром), принимая request - кортеж.
# Есть 2 действия: receipt - получение, shipment - отгрузка.
# а) В случае получения данные должны поступить в data (добавить пару, если её не было и изменить значение ключа,
# если позиция уже была в словаре)
# б) В случае отгрузки данные товара должны уменьшаться (если товар есть в data и если товара больше чем 0).
#
# 3.Метод run - принимает запросы и создаёт для каждого свой параллельный процесс, запускает его(start) и замораживает(join).
#
# Пример работы:
# # Создаем менеджера склада
# manager = WarehouseManager()
#
# # Множество запросов на изменение данных о складских запасах
# requests = [
#     ("product1", "receipt", 100),
#     ("product2", "receipt", 150),
#     ("product1", "shipment", 30),
#     ("product3", "receipt", 200),
#     ("product2", "shipment", 50)
# ]
#
# # Запускаем обработку запросов
# manager.run(requests)
#
# # Выводим обновленные данные о складских запасах
# print(manager.data)




from multiprocessing import Process, Queue

class WarehouseManager(Process):
    def __init__(self):
        super().__init__()
        self.data = {}

    def process_request(self, request):

        keys_ = request[0]
        values_ = request[2]
        action = request[1]
        data_1 = {keys_: values_}

        if action == 'receipt':
            if keys_ in self.data.keys():
                self.data[keys_] = self.data[keys_] + data_1[keys_]

            else:
                self.data[keys_] = values_
                self.data.update({keys_: values_})
                print(self.data)

        elif action == 'shipment':
            if keys_ in self.data.keys():
                self.data[keys_] = self.data[keys_] - values_
                print(self.data)


        return self.data


    def run(self, requests):
        for req in requests:
            cargo_process = Process(target=self.process_request, args=(req, ))
            cargo_process.start()
            cargo_process.join()

if __name__ == '__main__':
    manager = WarehouseManager()
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50)
    ]
    manager.run(requests)
    print(manager.data)