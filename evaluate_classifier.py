import json
from question_classifier import classify_question

def load_test_set(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def evaluate(test_set):
    correct = 0
    confusion = {t: {"TP":0, "FP":0, "FN":0} for t in ["short_info","full_info","history","author","fact"]}
    for item in test_set:
        pred = classify_question(item["question_text"])
        truth = item["expected_type"]
        if pred == truth:
            correct += 1
            confusion[truth]["TP"] += 1
        else:
            confusion[truth]["FN"] += 1
            confusion[pred]["FP"] += 1
    total = len(test_set)
    print(f"Всего примеров: {total}")
    print(f"Правильно: {correct}")
    print(f"Accuracy: {correct/total:.2%}\n")
    print("Метрики по типам:")
    for t in confusion:
        tp = confusion[t]["TP"]
        fp = confusion[t]["FP"]
        fn = confusion[t]["FN"]
        prec = tp/(tp+fp) if (tp+fp)>0 else 0
        rec = tp/(tp+fn) if (tp+fn)>0 else 0
        f1 = 2*prec*rec/(prec+rec) if (prec+rec)>0 else 0
        print(f"{t:12s} Precision={prec:.2%} Recall={rec:.2%} F1={f1:.2%}")

    print("Подробно по типам (реальных примеров в тесте):")
    for t, vals in confusion.items():
        real_count = vals["TP"] + vals["FN"]
        pred_count = vals["TP"] + vals["FP"]
        print(f"{t:12s} реально: {real_count:2d}, предсказано: {pred_count:2d}, TP={vals['TP']:2d}")

if __name__ == "__main__":
    test_set = load_test_set("test_questions.json")
    evaluate(test_set)