from pathlib import Path

from sklearn.naive_bayes import GaussianNB
import pickle

MODEL_FILE = Path(__file__).parent / 'model.pkl'

def word_count(text):
    keywords = ["ปกติ", "ตามปกติ", "ได้รับการแก้ไข", "นำออกจากระบบให้บริการ", "เคลื่อนที่ได้แล้ว", "สรุป", "ได้ตามปกติ", "กลับสู่สภาวะปกติ",
        "ใช้งานได้แล้ว", "มีความล่าช้า", "ส่งผลกระทบ", "ความเร็วต่ำ",
        "เกิดเหตุ", "ขัดข้อง", "จะล่าช้า", "แก้ไข", "เผื่อเวลา", "ช่วยเหลือ", "@"]
    return [text.count(keyword) for keyword in keywords]

def classify(text):
    labels = [None, 'normal', 'delay', 'disrupted']
    x = [word_count(text)]

    with MODEL_FILE.open('rb') as fp:
        clf = pickle.load(fp)

    return labels[clf.predict(x)[0]]
