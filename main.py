import streamlit as st

def main():
    st.title("File reader")

    uploaded_file = st.file_uploader("Upload file", type=[ "pdf"])

    if uploaded_file:
        temp_file = f'./{uploaded_file.name}'
        with open(temp_file, "wb") as file:
            file.write(uploaded_file.getvalue())

    question = st.text_input("Enter your question")

    if st.button("Ask"):
        if not question:
            st.error("Please enter a question")
        else:
            answer = process_question(question
            
            st.subheader("Answer:")
            st.write(answer)

    st.subheader("Answers")
    st.text_area("Answers will be displayed here", height=200)

    

def process_question(question):
    return "This is just a placeholder answer."

if __name__ == "__main__":
    main()
