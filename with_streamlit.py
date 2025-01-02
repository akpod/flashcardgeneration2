import streamlit as st
import ollama
import PyPDF2

st.set_page_config(page_title="AI Based Flashcard Generator", page_icon="📚")


def extract_text_from_pdf(pdf_file, pages):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in pages:
        if page_num < len(reader.pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def generate_flashcards(book):
    promot = f"""Generate flashcards from the following text like try to make it more on definations or just words just try to generate flashcard style questions from the following text and make sure to not add any additional things like saying okay, or hi there and stuff, or anything like Here are the flashcards generated from the provided text, Here are the flashcards generated from the provided text, like don't say anything at the start, straight to the flashcards, it will be fed to another machine so any extra things will make it not work so no additional things only the flashcards, go straigt to the spitting out the questions for the flashcard and, also make it with the following format
                    <Here Term> ~ <Here Definition>
                    <Here Term> ~ <Here Definition> 
                    <Here Term> ~ <Here Definition>
                    and also try to take out like terms not random sentence, try to take out some unique terms, not a sentence, like make the terms 1 - 3 words that have definations, and also don't make the term a sentence, instead a word that has defination, no sentence like saying when this happens, this happens, not like that, make the term that has a defination
                    and also don't say this is the term this is the defination, nothing from you
                    Below the thing that is striped by ``` ```is the text you are going to process and also all the texts after this are the things you are going to process and generate flashcards and also as I said don't say anything at the start or at the end no extra things other than the flashcard like Here are the flashcards:, Here is this this this, I don't want anything like that, only the flash cards
                    
                    ```
                    {book}
                    ```
                    Please remove any intros you add, no intros or outros like Here are the flashcards, just list them out, please make it really good questions, and please don't say note that I have added this this stuff, only the questions I want, pleaseeee
            """
    flashcards = ollama.process_data(promot)
    return flashcards

def split_ranges(start, end, chunk_size=10):
    return [(i, min(i + chunk_size - 1, end)) for i in range(start, end + 1, chunk_size)]

def process_pdf_in_chunks(file_name, page_range):
    start_page, end_page = page_range
    ranges = split_ranges(start_page, end_page)

    for start, end in ranges:
        book_data = extract_text_from_pdf(file_name, [start, end])
        chunk_output = generate_flashcards(book_data)
        clean_output = remove_empty_lines(chunk_output)
        return clean_output

def remove_empty_lines(text):
    return "\n".join([line.strip() for line in text.splitlines() if line.strip()])



# Streamlit App
st.title("AI Based Flashcard Generator")
st.header("AI Based Flashcard Generator")



uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    total_pages = len(PyPDF2.PdfReader(uploaded_file).pages)
    st.write(f"Total Pages in PDF: {total_pages}")

    start_page = st.number_input("Start Page", min_value=1, max_value=total_pages, value=1)
    end_page = st.number_input("End Page", min_value=start_page, max_value=total_pages, value=total_pages)
    chunk_size_input = st.number_input("Chunk Size", min_value=5, max_value=20, value=10)

    if st.button("Process PDF"):
        page_ranges = split_ranges(start_page - 1, end_page - 1, chunk_size_input)  # Adjust for 0-based index
        all_flashcards = ""

        for idx, (start, end) in enumerate(page_ranges):
            st.write(f"Processing pages {start + 1} to {end + 1}...")
            clean_output = process_pdf_in_chunks(uploaded_file, (start_page, end))
            all_flashcards += clean_output + "\n"

        st.code(all_flashcards, language='text')
        #st.download_button("Copy Flashcards", all_flashcards, file_name="flashcards.txt")

        st.success("Processing complete!")

