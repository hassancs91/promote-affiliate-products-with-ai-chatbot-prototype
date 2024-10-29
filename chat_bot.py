import streamlit as st
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.prompts.messages_template import MessagesTemplate
llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="chatgpt-4o-latest")

# Specify the path to your JSON file
file_path = 'wordpress_hosting_services.json'

# Open the file and read its contents into a string
with open(file_path, 'r') as file:
    json_string = file.read()


affiliate_system_prompt = f"""You are an expert in wordpress hosting services,
 I will provide you with a [JSON_DATA_FILE] containing a list of services with their features and details.
 
 Your task is to keep questioning the user based on the [JSON_DATA_FILE] till you know the best service to suggest for him.
 

 IMPORTANT: 
 Make sure to ask multiple questions for better user experience.
 Ask one question at a time.
 Make sure Return the affiliate link with your suggestion.

 ...

[JSON_DATA_FILE]:
{json_string}

...
 
 
 """

st.title("My AI Affiliate Chatbot 1.0 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
        start_prompt_used = ""


        st.chat_message("user").markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

    
        input_messages = MessagesTemplate()
        for m in st.session_state.messages:   
                if m["role"] == "user":
                    input_messages.add_user_message(m["content"])
                if m["role"] == "assistant":
                    input_messages.add_assistant_message(m["content"])

        messages = input_messages.get_messages()


        response = llm_instance.generate_response(messages=messages,system_prompt=affiliate_system_prompt,full_response=False)


        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


      