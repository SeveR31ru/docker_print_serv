# Сервер для печати

Данная программа состоит из двух папок:
1. docker-container для легкого запуска программы в контейнере
2. fastapi_print_server для локального развертывания, разработки  и тестирования

Программа расворачивает три endpoint-а для печати в трех разных формата:
    1. Таблица
    2. Текст
    3. Datamatrix-code

Сервер принимает json выбранного образца(его можно посмотреть в docs-api) и на выходе печатает наклейку на выбранном принтере.

Форматы печатаются в виде картинки, поэтому они автоматически адаптируются под разные размеры наклеек, если они внесены в шаблоны печати.
Для таблиц и текста можно выбрать размер шрифта. Текст и таблицы адаптируются под количество введенным данных( но в разумных пределах)

# Как развернуть

## 1. Развертывание CUPS
Шаг 1. Устанавливаете CUPS,для Ubuntu это  команда
```
sudo apt install cups
```

Шаг 2.Подключаете оба принтера к одному компьютеру. На данном шаге на компьютере может не оказаться драйверов под эти принтеры, ищем их на сайте производителя.

Шаг 3. Создаете на основе любого из них два принтера( в будущем буду называть их шаблонами печати). Именуете их в зависимости от типа наклеек, которые на нем будут печататся и задаете им базовые параметры в виде размера наклеек и скорости печати(не советую ставить слишком большую, иначе они начнут грязнить). Крайне нежелательно использовать экранированные символы, если нужны пробелы-ставьте нижние подчеркивания

**при проблемах с этим шагом  откалибруйте принтер по инструкции с официального сайта и почистили головку устройства-отслеживателя зазоров**

Шаг 4. Тестируете принтеры на размеры наклеек(Отключая один из них). Если все хорошо и тестовые изображения по формату подходят к наклейкам-первая часть завершена.

##2.1 Развертывание локально

Используем папку fastapi_print_server

Шаг 1. Находим принтеры в системе и выключаем их без отключения usb. Для этого вводим команду:
```lsusb -t```

Запоминаем порты принтеров и заходим в суперюзер-консоль командой:
```sudo -i```

В ней два раза вводим команду(по одной на каждый порт):

```echo 0 > /sys/bus/usb/drivers/usb/*port принтера*/authorized```

Альтернативно можно сделать аналогичное действие с помощью:

```sudo ./printer_activate.sh 0 *port принтера*```

Для включения принтера обратно выполните аналогичную команду,заменив 0 на 1

Шаг 2. Редактирует setting.ini. Вносим туда названия шаблонов печати(чтобы их посмотреть из консоли, можно ввести):
```lp -d *нажать таб и скопировать нужные*```

Вносим их в файл настроек, как и порты принтера. Желательно убедится, что названия шаблона печати и портов совпадает, иначе будет инвертированная печать. Аналогично переопределяем порт на свободный.

Шаг 3. Сделать

```pip install -r requirements.txt```

для установки зависимостей питона. Желательно изолировать среду(если умеете, иначе ставьте просто командой)

Шаг 4. Запустить
```sudo python3 main.py```

Если вы увидели в консоли ссылку на сайт- значит все сделано верно. При добавлении к адресу /docs(например, 192.168.1.31:6453/docs) вы перейдете в api-docs, где можно посмотреть запросы и формат отправки json-файлов в них. Протестируйте функции печати прямо оттуда и проверьте логи консоли. Если печать не происходит- проделайте шаги части 1. снова, проверьте конфиг и возможность печати с принтеров.

## 2.2  Развертывание в Docker
Используем папку docker_container

Шаг 1. Находим принтеры в системе и выключаем их без отключения usb. Для этого вводим команду:
```lsusb -t```

Запоминаем порты принтеров и заходим в суперюзер-консоль командой:
```sudo -i```

В ней два раза вводим команду(по одной на каждый порт):

```echo 0 > /sys/bus/usb/drivers/usb/*port принтера*/authorized```

Альтернативно можно сделать аналогичное действие с помощью:

```sudo ./printer_activate.sh 0 *port принтера*```

Для включения принтера обратно выполните аналогичную команду,заменив 0 на 1

Шаг 2. Редактирует setting.ini. Вносим туда названия шаблонов печати(чтобы их посмотреть из консоли, можно ввести):
```lp -d *нажать таб и скопировать нужные*```

Вносим их в файл настроек, как и порты принтера. Желательно убедится, что названия шаблона печати и портов совпадает, иначе будет инвертированная печать. Аналогично переопределяем порт на свободный.

Шаг 3. Установить Docker,если он не установлен. Делается командой:

```sudo apt install docker```

Шаг 4. Запускаем скрипт для запуска:

```sudo ./launch.sh *название контейнера*```

При необходимости внутри этого скрипта можно переопределить название созданного образа и порт, на котором откроется контейнер

Шаг 5. Проверяем работоспособность контейнера командой

```sudo docker ps -l```

Если вы видите ваш контейнер и его статус "UP", то он работает. Если оно вышло с  ошибкой:
![Alt text](image.png)

Чтобы посмотреть логи контейнера:
```sudo docker logs *имя контейнера*```

Если случилась ошибка, перед следующей сборкой нужно удалить предыдущий контейнер командой:
``` sudo docker rm *имя контейнера* ```

После фикса ошибок запускаем все с шага 4.

# Как дорабатывать

Если вы нашли ошибку или хотите внести новые функции в программу, необходимо сначала протестировать их локально. После внесения всех изменений необходимо скопировать все файлы, что вы изменили, в папку docker_container в те же места, где эти файлы были изначально. Нарушение местоположения файлов приведет к ошибке при сборке контейнера. Если вы хотите добавить новые файлы и они нужны для  постоянной работы программы- добавляйте их в папку app. Все остальные файлы помещайте просто в папку docker_container и изменяйте Dockerfile по примеру раздела "предварительные действия".


# Как работать

Правило 1. Не печатать параллельно на двух принтерах, только последовательно. Из-за кривых китайских драйверов при подключении двух принтеров одинаковой модели они воспринимаются как единое устройство(потому что у них единый серийник 0000001) и печатает только последний подключенный. Для переключения придуман системный обход, для паралельной печати он невозможен.

По идее параллельная печать невозможна, но кто знает, что выдумает пользователь.

Правило 2. Делайте небольшие задержки между запросами. Иначе может возникнуть ситуация с недостаточно быстрым откликом на выключение принтера и произойдет непредвиденная ситуация. Для этого в саму программу введены задержки для синхронизации, но лучше ему следовать для большей стабильности

Обращаться к endpoint-ам можно через /docs вручную для печатания единичных файлов либо через консоль с помощью curl, пример json-файла для отправки в функции дан в /docs