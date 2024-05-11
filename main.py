import logging
import streamlit as st

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

def main():
    try:
        st.title("File Reader")
        logging.debug("App started successfully")

        question = st.text_input("Enter your question")
        if st.button("Ask"):
            if not question:
                st.error("Please enter a question")
                logging.warning("User clicked 'Ask' without entering a question")
            else:
                answer = "Processing answer"
                st.subheader("Answer:")
                st.write(answer)
                logging.debug("Processed question: %s", question)

    except Exception as e:
        logging.error("An error occurred", exc_info=True)
        st.error("An unexpected error occurred")

if __name__ == "__main__":
    main()