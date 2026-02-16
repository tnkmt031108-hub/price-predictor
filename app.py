

from flask import Flask, render_template, request
import os

app = Flask(__name__)

real_years = [2556,2557,2558,2559,2560,
              2561,2562,2563,2564,2565]

x_years = list(range(1,11))

products = {
    "อาหาร": {
        "ก๋วยเตี๋ยว (บาท/ชาม)": [25,27,30,32,35,38,40,45,50,55],
        "ข้าวแกง (บาท/จาน)": [30,32,34,36,38,40,42,44,46,48],
        "หมูเนื้อแดง (บาท/กก.)": [120,125,130,135,140,145,150,160,170,180],
        "ไข่ไก่ (บาท/ฟอง)": [3,3,3.5,3.5,4,4,4.5,4.5,5,5],
        "ข้าวสาร (บาท/กก.)": [25,26,27,28,29,30,31,32,33,34]
    },
    "เครื่องดื่ม": {
        "กาแฟ (บาท/แก้ว)": [35,38,40,42,45,48,50,55,60,65],
        "น้ำดื่ม (บาท/ขวด)": [7,8,8,9,9,10,10,11,12,12],
        "นมกล่อง (บาท/กล่อง)": [10,10,11,11,12,12,13,13,14,14]
    },
    "ของใช้ประจำวัน": {
        "น้ำมันพืช (บาท/ขวด)": [35,37,38,40,42,45,48,50,55,60]
    }
}

@app.route("/", methods=["GET","POST"])
def home():
    result = ""

    if request.method == "POST":
        try:
            category = request.form["category"]
            item = request.form["item"]
            target_year = int(request.form["year"])

            prices = products[category][item]

            base_year = real_years[0]
            x_target = target_year - base_year + 1

            n = len(x_years)
            x_mean = sum(x_years)/n
            y_mean = sum(prices)/n

            a = sum((x_years[i]-x_mean)*(prices[i]-y_mean)
                    for i in range(n)) / \
                sum((x_years[i]-x_mean)**2
                    for i in range(n))

            b = y_mean - a*x_mean
            result_price = a*x_target + b

            if result_price < 0:
                result_price = 0

            result = f"""
หมวดสินค้า: {category}
สินค้า: {item}

สมการ: y = {a:.2f}x + {b:.2f}

ราคาคาดการณ์ ≈ {result_price:.2f} บาท
"""

        except:
            result = "กรุณากรอกข้อมูลให้ถูกต้อง"

    return render_template("index.html",
                           products=products,
                           result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
