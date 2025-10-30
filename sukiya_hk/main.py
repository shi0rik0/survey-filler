import re

import inquirer
import requests


def main():
    questions = [
        inquirer.Text("shop_code", message="請輸入店鋪編號"),
        inquirer.Text("visit_date", message="請輸入到店日期 (例如: 0831)"),
        inquirer.Text("visit_time", message="請輸入到店時間 (例如: 0930)"),
        inquirer.Text("receipt_code", message="請輸入收據編號"),
    ]
    answers = inquirer.prompt(questions)
    if answers is None:
        return
    shop_code = answers["shop_code"]
    visit_date = answers["visit_date"]
    visit_time = answers["visit_time"]
    receipt_code = answers["receipt_code"]
    visit_month = visit_date[:2]
    visit_day = visit_date[2:]
    visit_hour = visit_time[:2]
    visit_minute = visit_time[2:]

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
        }
    )

    response = session.get("https://hk-sukiya.csfeedback.net/sv/")

    if response.status_code != 200:
        print("Failed to access the survey page.")
        return

    response = session.post(
        "https://hk-sukiya.csfeedback.net/sv/",
        data={
            "mode": "init",
            "shop_code": shop_code,
            "day": visit_day,
            "month": visit_month,
            "select_visit_hour": visit_hour,
            "select_visit_minute": visit_minute,
            "visit_hour": f"{visit_hour}:{visit_minute}",
            "receipt_code": receipt_code,
            "agree": "on",
        },
    )

    if response.status_code != 200:
        print("Failed to start the survey.")
        return

    survey_answers = [
        {
            "page": 1,
            "answers": {
                # 請問您是否會將「すき家」推薦給朋友或同事? -> 非常推薦
                "28013": "10",
            },
        },
        {
            "page": 2,
            "answers": {
                # 您光顧【本店】的頻率是？ -> 大約每星期1次
                "28014": "4",
            },
        },
        {
            "page": 3,
            "answers": {
                # 以下哪一個是您這次的消費方式呢？ -> 堂食
                "28015": "1",
            },
        },
        {
            "page": 4,
            "answers": {
                # 與誰一同光顧本店呢？ -> 一個人
                "28016": "1",
            },
        },
        {
            "page": 6,
            "answers": {
                # 以下哪一款是您這次享用的主食餐點呢？ -> 其他
                "28018": "999",
            },
        },
        {
            "page": 20,
            "answers": {
                # 關於您這次光顧的店舖評價。 -> 全部非常滿意
                "28039": "1",
                "28040": "1",
                "28041": "1",
                "28042": "1",
                "28043": "1",
                "28044": "1",
            },
        },
        {
            "page": 21,
            "answers": {
                # 店鋪的整體評價 -> 非常滿意
                "28045": "1",
            },
        },
        {
            "page": 22,
            "answers": {
                # 請詳述您對這次享用的餐點及本店的意見、需要改善或感到不滿的地方。
                "28046": "",
                "28047": "",
            },
        },
        {
            "page": 23,
            "answers": {
                # 您是透過哪些途徑認識SUKIYA呢？ -> 其他
                "28048": "8",
            },
        },
        {
            "page": 24,
            "answers": {
                # 這次，您是透過哪些途徑決定光顧SUKIYA呢？ -> 其他
                "28049": "10",
            },
        },
        {
            "page": 25,
            "answers": {
                # 性別 -> 不想回答
                "28050": "997",
                # 年齡 -> 不想回答
                "28051": "997",
                # 職業 -> 其他
                "28052": "12",
            },
        },
        {
            "page": 26,
            "answers": {
                # 個人每月收入 -> 不想回答
                "28053": "997",
            },
        },
        {
            "page": 27,
            "answers": {
                # 請選擇您所住的地方在地圖上相應的數字。 -> 1
                "28054": "1",
            },
        },
        {
            "page": 28,
            "answers": {
                # 以地理位置來說，您選擇本店的理由是什麼？ -> 離屋企近
                "28055": "1",
            },
        },
    ]

    for a in survey_answers:
        response = session.post(
            "https://hk-sukiya.csfeedback.net/sv/",
            data={
                "page": a["page"],
                "q[]": list(a["answers"].keys()),
                **{f"q_{k}": v for k, v in a["answers"].items()},
            },
        )

        if response.status_code != 200:
            print(f"Failed to submit answers for page {a['page']}.")
            return

    result_page = response.text

    match = re.search(r'<p class="number">(.*?)</p>', result_page)
    if match:
        code = match.group(1)
        print("問卷提交成功！")
        print(f"問卷驗證碼是：{code}")
    else:
        print("Failed to retrieve the survey code.")


if __name__ == "__main__":
    main()
