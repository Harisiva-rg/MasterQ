import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import re
from docx import Document as Docx_doc
from docxlatex import Document as Doc_latex

def doclatex_converter(file_path):
    temp_doc = Doc_latex(file_path)
    text = temp_doc.get_text()
    temp_doclatex_converted_docx = Docx_doc()
    temp_doclatex_converted_docx.add_paragraph(text)
    return temp_doclatex_converted_docx

# def temp_docx_remover(file_name):
#     if os.path.exists('temp_doclatex_converted.docx'):
#         os.remove('temp_doclatex_converted.docx')
#         return ("Temp File of ",file_name," deleted")
#     else:
#         return ("Temp file does not exist")

def content_extractor(doc):
    contents = ""
    for para in doc.paragraphs:
        txt = para.text.strip()
        contents += txt + "¥"
    return contents

def question_splitter(qn_list_updated):
    qns = []
    for entry in qn_list_updated:
        item = entry.split("@")
        qns.append(item)
    return qns

def aggregation(level):
    return ', '.join(level)

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False, encoding="utf-8-sig")

df_columns = ['Question','Option_A','Option_B','Option_C','Option_D','Option_E','Correct_answer','Explanation',
                'Subject','Topic','Level','Board','Source_file','has_image','has_maths']
df = pd.DataFrame(columns=df_columns)

st.set_page_config(page_title="Content Converter", layout="wide")

st.subheader("Content Coverter")

with st.sidebar:
    subject = st.sidebar.selectbox('Select a Subject', ['Mathematics', 'Chemistry', 'Physics'])



uploaded_files  = st.file_uploader("Upload your docx file(s)", type='docx', accept_multiple_files= True)
if uploaded_files  is not None:
    for uploaded_file in uploaded_files:
        ct = 1
        st.write("Processing ",uploaded_file.name)
        
        if subject == "Mathematics":
            doclatex_conv = doclatex_converter(uploaded_file)
            doc = doclatex_conv
        else:
            doc = Docx_doc(uploaded_file)
        content = content_extractor(doc)

        # print(content)
        qn_list = content.split("@#")
        
        qn_list_tmp = [i for i in qn_list if not re.match(r'^[ ¥]*$', i)]
        qn_list_updated = [re.sub(r'¥+', r'¥', i) for i in qn_list_tmp]
        
        qns = question_splitter(qn_list_updated)
        for entry in qns:
            try:
            # print(entry)
                qn = entry[0].strip().replace('¥', '\n').replace("â€™", "'").replace("â€˜", "'")
                options_all = entry[1].strip().replace("â€™", "'").replace("â€˜", "'")
                answer = entry[2].strip().replace('¥', '').replace("â€™", "'").replace("â€˜", "'")
                # answer = entry[2]
                explanation = entry[3].strip().replace('¥', ' ').replace("â€™", "'").replace("â€˜", "'")
                image = entry[4].replace('\\n', "").replace("Image:", "").strip()
                equation = entry[5].replace('\\n', '').replace("Equation:", "").strip()
            
                # print(options_all)

                question = qn.split(")",1)[1].strip()

                # print(qn.split(")",1)[0], equation)
                
                options = options_all.split('¥')
                options = list(filter(None, options))
                # print(options)

                row = {
                        'Question': question,
                        'Option_A': options[1][2:] if len(options) > 1 else '',
                        'Option_B': options[2][2:] if len(options) > 2 else '',
                        'Option_C': options[3][2:] if len(options) > 3 else '',
                        'Option_D': options[4][2:] if len(options) > 4 else '',
                        'Option_E': options[5][2:] if len(options) > 5 else '',
                        'Correct_answer': answer[7:] if len(options) > 1 else '',
                        'Explanation': explanation[9:],
                        'Subject': subject,
                        'Topic': "topic", 
                        'Level': 'GCSE', 
                        'Board': "board", 
                        'Source_file': uploaded_file.name, 
                        'has_image': image, 
                        'has_maths': equation 
                    }
                ct += 1
            except IndexError:
                st.write("Error in Q",ct)

            df = pd.concat([df, pd.DataFrame(row, index=[0])], ignore_index=True)

csv_file = convert_df(df)

print(type(csv_file))



if uploaded_files:
    st.write("File(s) Converted")
    st.download_button(
    "Press to Download",
    csv_file,
    "file.csv",
    "text/csv",
    key='download-csv'
    )
