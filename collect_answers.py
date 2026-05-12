import requests
import json
import csv
import time
import os
import subprocess

API_URL = "http://127.0.0.1:8000/ask"

def get_answer(id_exp, text):
    try:
        resp = requests.post(API_URL, json={"id_exp": id_exp, "text": text}, timeout=120)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("answer", ""), data.get("question_type")
        else:
            return f"HTTP {resp.status_code}: {resp.text}", None
    except Exception as e:
        return f"Exception: {str(e)}", None

def collect(test_set_path, output_csv):
    if not os.path.exists(test_set_path):
        print(f"Ошибка: {test_set_path} не найден")
        return
    with open(test_set_path, 'r', encoding='utf-8') as f:
        test_set = json.load(f)
    results = []
    for i, item in enumerate(test_set, 1):
        print(f"[{i}/{len(test_set)}] {item['question_text'][:50]}...")
        answer, pred_type = get_answer(item["id_exp"], item["question_text"])
        results.append({
            "id_exp": item["id_exp"],
            "question": item["question_text"],
            "expected_type": item["expected_type"],
            "predicted_type": pred_type,
            "answer": answer
        })
        time.sleep(1)
    # Запись на рабочий стол
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    output_csv = os.path.join(desktop, "answers.csv")
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["id_exp","question","expected_type","predicted_type","answer"])
        writer.writeheader()
        writer.writerows(results)
    print(f"Файл сохранён: {output_csv}")
    subprocess.Popen(f'explorer /select,"{output_csv}"')


if __name__ == "__main__":
    collect("test_questions.json", "")