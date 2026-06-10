# 🏫 School Dashboard — ระบบ Dashboard รายชื่อโรงเรียน

ระบบ Interactive Dashboard สำหรับแสดงข้อมูลโรงเรียนและนักเรียน พร้อม Visualization แผนที่และกราฟสถิติ

---

## 🎯 Overview

โปรเจคนี้พัฒนา Dashboard ที่สามารถ

- แสดงรายชื่อโรงเรียนบนแผนที่แบบ Interactive
- วิเคราะห์และแสดงข้อมูลนักเรียนในรูปแบบกราฟ
- กรองและค้นหาข้อมูลโรงเรียนได้
- อ่านข้อมูลจากไฟล์ CSV และ JSON

---

## 🗂️ Project Structure

```
Dash-board-/
├── main_app.py        # Main Dashboard application
├── readfile_std.py    # อ่านและประมวลผลข้อมูล
├── student.csv        # ข้อมูลนักเรียน
├── student.json       # ข้อมูลนักเรียน (JSON format)
├── map.csv            # ข้อมูลพิกัดแผนที่โรงเรียน
├── pyproject.toml     # Project dependencies
└── poetry.lock        # Locked dependencies
```

---

## ⚙️ Tech Stack

| Component | Technology |
|---|---|
| Dashboard Framework | Plotly Dash |
| Data Processing | Pandas |
| Map Visualization | Plotly Maps |
| Package Manager | Poetry |
| Language | Python |

---

## 🚀 Installation

**ติดตั้งด้วย Poetry**
```bash
git clone https://github.com/Arifin748/Dash-board-.git
cd Dash-board-
poetry install
poetry run python main_app.py
```

**หรือติดตั้งด้วย pip**
```bash
pip install plotly dash pandas
python main_app.py
```

จากนั้นเปิด browser ที่ `http://localhost:8050`

---

## 📊 Features

- **แผนที่** — แสดงตำแหน่งโรงเรียนบนแผนที่ประเทศไทย
- **ตารางข้อมูล** — รายชื่อโรงเรียนพร้อมรายละเอียด
- **กราฟสถิติ** — วิเคราะห์ข้อมูลนักเรียนแบบ visual

---

## 👤 Author

**Arifin Madstoon** (6410110748) — PSU
