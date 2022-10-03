import PyPDF2
import os
import sys
# List all the pdf files in the specified directory
def list_pdf_files(directory):
    pdf_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_files.append(filename)
    return pdf_files

def cleanlist(dictlist):
    current = []
    for line in dictlist:
        if line.endswith("-"):
            current.append(line[:-1])
        elif line.endswith(" "):
            current.append(line)
        else:
            current.append(line)
            yield "".join(current)
            current = []

files = list_pdf_files(sys.argv[1])

# Extract the text from each pdf file
for filename in files:
    print("Extracting text from " + filename)
    pdf_file = open(sys.argv[1]+"/"+filename, "rb")
    file_name_without_extension = filename.split(".")[0]
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    pdf_text = ""
    for page in range(pdf_reader.numPages):
        try:
            pdf_text += "\n".join(cleanlist(pdf_reader.getPage(page).extractText().split("\n")))
        except:
            print("Error extracting text from " + filename, "and page", page)
    pdf_file.close()
    # Write the text to a file
    text_file = open(sys.argv[1]+"/"+file_name_without_extension + ".txt", "w")
    text_file.write(pdf_text)
    text_file.close()