# MasterQ Content Converter
This application uses Streamlit, to convert .docx files into CSV format.

## Usage

The application provides a sidebar where you can select the subjects. Then, you can upload your .docx files using the file uploader in the main area of the application.

Once you've selected a subject and uploaded the files, the application will start processing the files. It will extract the content from each file, split the content into questions and answers, and store the data in a data frame. The data frame includes columns for the question, options, correct answer, explanation, subject, topic, level, board, source file, whether the question has an image or not, and whether the question has a mathematical equation or not.

Finally, the application converts the DataFrame into a CSV file and provides a download button to download the CSV file.

Application URL: https://masterq-cmxqr2fkdjnbky5jbnceni.streamlit.app/
