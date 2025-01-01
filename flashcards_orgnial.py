import ollama
import PyPDF2

def extract_text_from_pdf(pdf_path, pages):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        text = ""
        
        # Extract text from specified pages
        for page_num in pages:
            # Ensure the page number is within the bounds of the PDF
            if page_num < len(reader.pages):
                page = reader.pages[page_num]
                text += page.extract_text()
        
    return text

def generate_flashcards(book):
    # Use the ollama API to generate flashcards

    promot = f"""Generate flashcards from the following text like try to make it more on definations or just words just try to generate flashcard style questions from the following text and make sure to not add any additional things like saying okay, or hi there and stuff, or anything like Here are the flashcards generated from the provided text, Here are the flashcards:, Here are the flashcards generated from the provided text:, Here are the flashcards generated from the provided text, like don't say anything at the start, straight to the flashcards, it will be fed to another machine so any extra things will make it not work so no additional things only the flashcards, go straigt to the spitting out the questions for the flashcard and, also make it with the following format
                    question $$
                    answer
                    ~
                    question $$
                    answer
                    ~
                    question $$
                    answer
                    ~
                    and also try to take out like terms not random sentence, try to take out some unique terms, not a sentence, like make the terms 1 - 3 words that have definations, and also don't make the term a sentence, instead a word that has defination, no sentence like saying when this happens, this happens, not like that, make the term only a word that has a defination
                    Below is the text you are going to process and also all the texts after this are the things you are going to process and generate flashcards and also as I said don't say anything at the start or at the end no extra things other than the flashcard
                    
                    {book}"""
    flashcards = ollama.process_data(promot)
    return flashcards

book_data = extract_text_from_pdf("chemo.pdf", [66, 70])
output = generate_flashcards(book_data)

print(output)