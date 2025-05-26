import gradio as gr
import requests
from datetime import datetime, timedelta, timezone

def get_weather(city="서울"):
    API_KEY = "jb14LGSONSwtrptaTUfUlGp3fAc0f1MJ78s/tRyt0OiffhCXohmDlqutYyCKdHiOTQblmUoVaw27l/MYJBN29g=="
    nx, ny = 60, 127  # 서울시청 격자 좌표
    now = datetime.now(timezone.utc) + timedelta(hours=9)  # KST 기준
    base_date = now.strftime('%Y%m%d')

    # 가장 가까운 발표 시간 선택
    hour = now.hour
    if hour < 2:
        base_time = "2300"
        base_date = (now - timedelta(days=1)).strftime('%Y%m%d')
    elif hour < 5:
        base_time = "0200"
    elif hour < 8:
        base_time = "0500"
    elif hour < 11:
        base_time = "0800"
    elif hour < 14:
        base_time = "1100"
    elif hour < 17:
        base_time = "1400"
    elif hour < 20:
        base_time = "1700"
    elif hour < 23:
        base_time = "2000"
    else:
        base_time = "2300"

    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
    params = {
        'serviceKey': API_KEY,
        'numOfRows': '1000',
        'pageNo': '1',
        'dataType': 'JSON',
        'base_date': base_date,
        'base_time': base_time,
        'nx': nx,
        'ny': ny
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        items = data['response']['body']['items']['item']

        today = now.strftime('%Y%m%d')
        target_time = now.strftime('%H') + "00"

        temperature = None

        for item in items:
            if item['fcstDate'] == today and item['fcstTime'] == target_time:
                if item['category'] == 'TMP':
                    temperature = item['fcstValue']
                    break

        if temperature:
            return f"{city}의 현재 기온: {temperature}°C"
        else:
            return "기온 정보를 찾을 수 없습니다."

    except Exception as e:
        return f"날씨 정보 오류: {e}"

def greet(name, enthusiasm):
    weather_info = get_weather()
    return f"Cheer Up! {name} {'🔥'* enthusiasm}\n{weather_info}"

demo = gr.Interface(
    fn=greet,
    inputs=[
        gr.Textbox(label="이름", value="홍길동"),
        gr.Slider(minimum=1, maximum=5, step=1, label="열정도")
    ],
    outputs=gr.Textbox(label="인사말"),
    title="Simple Greetings app",
    description="이름을 입력하고 열정도를 선택하면 응원 문구와 서울의 기온을 보여줍니다."
)

if __name__ == "__main__":
    demo.launch()
