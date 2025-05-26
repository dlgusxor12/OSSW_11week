import gradio as gr

def greet(name, enthusiasm):
  """Takes the user's name and returns a cheerful message."""
  return f"Cheer Up! {name} {'🔥'* enthusiasm}"

demo = gr.Interface(
    fn=greet,
    inputs=[
      gr.Textbox(label="이름", value="홍길동"),
      gr.Slider(minimum=1, maximum=5, step=1, label="열정도")
    ],
    outputs=gr.Textbox(label="인사말"),
    title="Simple Greetings app",
    description="이름을 입력하고 열정도를 선택하면 응원 문구를 생성합니다."
)

if __name__ == "__main__":
  demo.launch()