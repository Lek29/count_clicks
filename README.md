# VK Link Shortener and Click Counter

## Описание

Этот проект позволяет создавать короткие ссылки с помощью VK API и считать количество кликов по этим ссылкам. Если введена длинная ссылка, программа создаст короткую ссылку.
Если введена уже короткая ссылка, программа посчитает количество кликов по ней.

## Необходимые переменные окружения
| Переменная окружения| Описание | Пример |
|---------------------|----------|--------|
| VK_SERVICE_KEY      | API из приложения VK         |     your API   |

## Запуск программы.
* Скачайте код.
* Установите зависимости командой `pip install -m requirements.txt`.
* Получите API в VK

## Переменные окружения.

Создайте файл `.env` в корне вашего проекта и добавьте в него следующие переменные окружения:
```python
VK_SERVICE_KEY=your API
```

## Примеры корректного запуска и выполнения программы.
Запустите скрипт, чтобы создать короткую ссылку или посчитать количество кликов:
```
python main.py -l https://dvmn.org/

```

Output:
```
Короткая ссылка: https://vk.cc/cx0cHv
```

Input:
```
python main.py -l https://vk.cc/cx0cHv
```
Output:
```
Количество кликов: 2
```
