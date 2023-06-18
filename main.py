import os
from dotenv import load_dotenv
import openai

# Указание полного пути до файла .env
env_path = r'C:\Users\danii\вход в гильдию\планирование задач с гпт\.env'
load_dotenv(env_path)

# Получение ключа от OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_schedule(tasks, breakfast_time, lunch_time, dinner_time):
    prompt = "Создать расписание на день:\n\n"

    # Добавление времени приема пищи в задачи
    tasks_with_meals = tasks[:]
    tasks_with_meals.insert(0, f"Готовка и поедание завтрака ({breakfast_time})")
    tasks_with_meals.append(f"Готовка и поедание обеда ({lunch_time})")
    tasks_with_meals.append(f"Готовка и поедание ужина ({dinner_time})")

    for task in tasks_with_meals:
        prompt += f"- {task}\n"

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=200,
        temperature=0.7,
        n=1,  # Генерируем только один вариант расписания
        stop=None,
        timeout=10
    )

    schedule = response.choices[0].text.strip().replace('\n', ' ')
    return schedule


def format_schedule(schedule):
    lines = schedule.split('\n')
    formatted_schedule = ""
    for line in lines:
        parts = line.split('-')
        time = parts[0].strip()
        task = '-'.join(parts[1:]).strip()
        formatted_schedule += f"{time} - {task}\n"
    return formatted_schedule


tasks = []

while True:
    task = input("Введите задачу (или нажмите Enter для завершения): ")
    if task:
        tasks.append(task)
    else:
        break

breakfast_time = input("Введите время для завтрака (в формате ЧЧ:ММ): ")
lunch_time = input("Введите время для обеда (в формате ЧЧ:ММ): ")
dinner_time = input("Введите время для ужина (в формате ЧЧ:ММ): ")

schedule = generate_schedule(tasks, breakfast_time, lunch_time, dinner_time)
formatted_schedule = format_schedule(schedule)
print("Ваше расписание на день:")
print(formatted_schedule)