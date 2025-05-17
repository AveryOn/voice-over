# TTS. текст -> аудио
---

- Применяется в качестве вспомогательной системы для локального AI-ассистента.
- Это не окончательное production решение а только сырая наработка как отдельный модуль, для упрощения тестировния и разработки

## Установка

```bash
python -m venv silero-venv
source silero-venv/bin/activate  # или .\silero-venv\Scripts\activate на Windows
pip install -r requirements.txt
```


## Запуск

```bash
# Запуск в разработке
python ./src/speak.py "Я твой локальный ассистент. Слушаю внимательно"   #  или python3 если на Windows
```

```bash
# Собрать список зависимостей python
pip freeze > requirements.txt
```
