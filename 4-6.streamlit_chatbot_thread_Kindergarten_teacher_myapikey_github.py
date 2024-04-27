from openai import OpenAI
import streamlit as st
import time

# 배포용 깃허브 시크릿으로 감춤
assistant_id = st.secrets["assistant_id"]
thread_id = st.secrets["thread_id"]
openai_api_key_value = st.secrets["openai_api_key_value"]

with st.sidebar:
    
    st.link_button("더 좋은 컨텐츠를 위해 후원하기", "https://toss.me/kimfl")
    st.link_button("쿠팡 홈", "https://link.coupang.com/a/bzr5o5")
        
    my_cupanghome_link_html = "https://link.coupang.com/a/bzr8L0" # 다이슨 청소기 링크-샘플
    st.markdown(my_cupanghome_link_html, unsafe_allow_html=True) 
    st.info("이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.")
    
    ### 아래는 카테고리 배너 생성인데 작동이 안됨???
    iframe_html = """<iframe src="https://ads-partners.coupang.com/widgets.html?id=775429&template=banner&
    trackingCode=AF1125071&subId=&width=160&height=50" width="160" height="50" frameborder="0" scrolling="no" 
    referrerpolicy="unsafe-url" browsingtopics></iframe>"""
    st.markdown(iframe_html, unsafe_allow_html=True)    
    
    openai_api_key = st.text_input("OpenAI API KEY", type="password",value = openai_api_key_value) 
    client = OpenAI(api_key = openai_api_key)

    thread_id = st.text_input("Thread ID", value = thread_id)
    
    thread_make_btn = st.button("Create a new thread") 

    if thread_make_btn:
        # 쓰레드 생성
       thread = client.beta.threads.create()
       thread_id =  thread.id 
       st.subheader(f"{thread_id}", divider = "rainbow")
       st.info("새로운 쓰레드가 생성되었습니다.")
       
    
st.title("My ChatBot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "저는 유치원 선생님입니다, 무엇이든 물어보세요?"}]

print(f"st.session_state\n{st.session_state}")
print()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input()
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=prompt)
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
    run_id = run.id
    
    while True:
       # Step 5: Check the Run status
       run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id )
       if run.status == 'completed':
           break
       
       else:
           time.sleep(2)
    
    thread_messages = client.beta.threads.messages.list(thread_id)
    assistant_content = thread_messages.data[0].content[0].text.value
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_content})
    st.chat_message("assistant").write(assistant_content)
    
    print(st.session_state.messages)
