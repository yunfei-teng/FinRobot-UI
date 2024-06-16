import re
import base64
import streamlit as st

def add_pdf_to_assistant(client, assistant, pdf_path):
    my_file = client.files.create(
        file=open(pdf_path, "rb"),
        purpose='assistants'
    )
    client.beta.assistants.update(assistant.id, file_ids=[my_file.id])

def query(client, assistant, question):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=question
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    while run.status !="completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    content = messages.data[0].content[0].text.value
    cleaned_content = re.sub(r"【\d+†source】", "", content)
    cleaned_content = cleaned_content.strip()
    return cleaned_content

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    
def set_custom_style():
    ''' UI design '''

    st.set_page_config(page_title="FinRobot", page_icon="images/FinRobot.png")
    with st.sidebar:
        st.logo('icons/AI4Finance.png')
        st.write()
        st.markdown("🙌 **Hi, I'm FinRobot! I can assist with providing information and engaging in conversations.**")
        st.image('images/FinRobot.png')

        st.write()
        st.markdown("""<hr style="height:3px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        st.markdown("<big style='color: grey'>Developed by</big>", unsafe_allow_html=True)
        st.image('images/AI4Finance.jpeg', use_column_width=True)
    st.title("FinRobot ")

    st.markdown(
        """
        <style>
            h1 {
                font-size: 40px !important;
            }
            p {
                font-size: 20px !important;
            }
            .stButton button {
                font-size: 25px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )