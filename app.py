import streamlit as st

from chatbot import chatbot


def main():
    st.title("Game of Thrones Chatbot")
    st.write("Ask anything about characters, houses, seasons, or major events!")

    user_input = st.text_input("Your question:")

    if st.button("Ask"):
        response = chatbot(user_input)
        st.write("**Answer:**")
        st.write(response)

if __name__ == "__main__":
    main()
