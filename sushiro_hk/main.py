import inquirer
import requests


def main():
    questions = [
        inquirer.Text("invitation_code", message="請輸入問卷邀請碼"),
        inquirer.Text("total_price", message="請輸入消費總額"),
        inquirer.List(
            "visited_time",
            message="請選擇到店時間",
            choices=[
                ("~14時", "1"),
                ("14時~17時", "2"),
                ("17時~21時", "3"),
                ("21時~", "4"),
            ],
        ),
    ]
    answers = inquirer.prompt(questions)

    if answers is None:
        return

    invitation_code = answers["invitation_code"]
    total_price = answers["total_price"]
    visited_time = answers["visited_time"]

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
        }
    )

    response = session.get("https://nps.sushiro.com.hk/")

    if response.status_code != 200:
        print("Failed to access the survey page.")
        return

    response = session.post(
        "https://nps.sushiro.com.hk/api/v1/surveys/start",
        json={
            "invitation_code": invitation_code,
            "total_price": total_price,
            "visited_time": visited_time,
        },
        headers={
            "Authorization": "Bearer web:1c263ca9a5b36e58b8a3f3ca02f54f97",
        },
    )

    if response.status_code != 200:
        print("Failed to start the survey.")
        return

    response = session.post(
        "https://nps.sushiro.com.hk/api/v1/surveys/next",
        json={
            "invitation_code": invitation_code,
            "total_price": total_price,
            "visited_time": visited_time,
            "answers": [
                # 請您對此店舖的整體滿意度評分。 -> 非常滿意
                {"mst_question_id": 1, "answered_option_no": "1"},
                # 服務速度 -> 非常滿意
                {"mst_question_id": 5, "answered_option_no": "1"},
                # 食物味道 -> 非常滿意
                {"mst_question_id": 6, "answered_option_no": "1"},
                # 餐點種類 -> 非常滿意
                {"mst_question_id": 7, "answered_option_no": "1"},
                # 食物溫度 -> 非常滿意
                {"mst_question_id": 8, "answered_option_no": "1"},
                # 店舖氣氛 -> 非常滿意
                {"mst_question_id": 9, "answered_option_no": "1"},
                # 職員的待客態度 -> 非常滿意
                {"mst_question_id": 10, "answered_option_no": "1"},
                # 店鋪清潔 -> 非常滿意
                {"mst_question_id": 11, "answered_option_no": "1"},
                # 壽司的分量 -> 非常滿意
                {"mst_question_id": 12, "answered_option_no": "1"},
                # 壽司的賣相 -> 非常滿意
                {"mst_question_id": 13, "answered_option_no": "1"},
                # 整體的性價比 -> 非常滿意
                {"mst_question_id": 14, "answered_option_no": "1"},
                # 本次蒞臨本店消費時，是否有出現突發狀況或問題？ -> 不是
                {"mst_question_id": 17, "answered_option_no": "2"},
                # 會否於3個月内再次光顧本店嗎？ -> 一定會
                {"mst_question_id": 19, "answered_option_no": "1"},
                # 請問您有多大程度會向他人推薦壽司郎？ -> 10
                {"mst_question_id": 20, "answered_option_no": "1"},
                # 請告知在此壽司郎店舖的體驗之中感到非常滿意的理由。
                {"mst_question_id": 23, "answered_option_no": ""},
                # 壽司郎職員是否有提供超乎您期待的服務？ -> 不是
                {"mst_question_id": 24, "answered_option_no": "2"},
                # 職員有否說日文的問候語？ -> 是
                {"mst_question_id": 27, "answered_option_no": "1"},
                # 職員在應對時是否態度親切？ -> 是
                {"mst_question_id": 28, "answered_option_no": "1"},
                # 在過去3個月内，包括今次的來店共惠顧過壽司郎多少次? -> 1次
                {"mst_question_id": 64, "answered_option_no": "1"},
                # 請問這是您第一次光顧這間壽司郎分店嗎？ -> 不是
                {"mst_question_id": 65, "answered_option_no": "2"},
                # 本次來店的原因 -> 因選址方便
                {"mst_question_id": 67, "answered_option_no": "1"},
                # 本次來店用餐的人數 -> 1人
                {"mst_question_id": 68, "answered_option_no": "1"},
                # 希望壽司郎推出的活動或宣傳
                {"mst_question_id": 72, "answered_option_no": ""},
                # 您的性別 -> 不想回答
                {"mst_question_id": 73, "answered_option_no": "3"},
                # 您的年齡 -> 不想回答
                {"mst_question_id": 74, "answered_option_no": "8"},
            ],
            "comments": [],
        },
        headers={
            "Authorization": "Bearer web:1c263ca9a5b36e58b8a3f3ca02f54f97",
        },
    )

    if response.status_code != 200:
        print("Failed to submit the survey.")
        return

    result = response.json()
    print("問卷提交成功！")
    print(f"問卷驗證碼是：{result['data']['code']}")


if __name__ == "__main__":
    main()
