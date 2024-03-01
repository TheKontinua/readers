import subprocess
from django.shortcuts import get_object_or_404

from mentapp.models import Chapter_Loc


# Converts quiz object to volume string (just the number)
def quizToDataString(quiz, type):
    if type == "volume":
        strObject = str(quiz.volume)
    elif type == "chapter":
        strObject = str(quiz.chapter)
    start = strObject.find("(")
    end = strObject.find(")")
    return strObject[start + 1 : end]


# Converts page size to vspace
# TODO: Calculate VSpace based on number of pages
def pagesRequiredToSpacing(pages):
    return "6cm"


"""
Takes in latex information and returns a pdf quiz

latex_question_list: list of question objects
quiz_data: quiz object
"""


def latex_to_pdf(latex_question_list, quiz_data):
    output_file = open("docs\latex\output_quiz.tex", "w")
    output_file.write(r"\documentclass[letterpaper,12pt,addpoints]{exam}" + "\n")
    output_file.write(r"\usepackage[utf8]{inputenc}" + "\n")
    output_file.write(r"\usepackage[english]{babel}" + "\n\n")
    output_file.write(
        r"\usepackage[top=0.5in, bottom=1in, left=0.75in, right=0.75in]{geometry}"
        + "\n"
    )
    output_file.write(r"\usepackage{amsmath,amssymb}" + "\n")
    output_file.write(r"\usepackage{mdframed}" + "\n")
    output_file.write(r"\usepackage{graphicx}" + "\n\n")
    output_file.write(r"\pagestyle{headandfoot}" + "\n")
    output_file.write(r"\firstpageheader{}{}{}" + "\n")
    output_file.write(
        r"\firstpagefooter{}{\fontfamily{phv}\selectfont\thepage\ of \numpages}{\fontfamily{phv}\selectfont 8A23B1CC5}"
        + "\n"
    )
    volume_id = quizToDataString(quiz_data, "volume")
    output_file.write(
        r"\runningfooter{\fontfamily{phv}\selectfont Kontinua "
        + volume_id
        + r" (X/X)}{\fontfamily{phv}\selectfont\thepage\ of \numpages}{\fontfamily{phv}\selectfont 8A23B1CC5}"
        + "\n\n\n"
    )

    output_file.write(r"\begin{document}" + "\n\n")
    output_file.write(r"{\fontfamily{phv}\selectfont" + "\n")
    output_file.write(r"\noindent \parbox{0.65\textwidth}{" + "\n")
    output_file.write(r"Name: \hrulefill \\" + "\n\n")
    output_file.write(r"\vspace{0.2cm}" + "\n\n")
    output_file.write(r"Date:\ \hrulefill" + "\n\n")
    output_file.write(r"\vspace{1.0cm}" + "\n\n\n\n")

    output_file.write(r"\textbf{Kontinua " + volume_id + r" (X/X)}" + "\n\n")

    chapter_name = get_object_or_404(Chapter_Loc, chapter=quiz_data.chapter).title
    output_file.write(r"\Large \textbf{" + chapter_name + r"}" + "\n\n" + r"}" + "\n")

    output_file.write(r"\parbox{0.35\textwidth}{" + "\n\n")

    output_file.write(r"\begin{flushright}" + "\n")
    output_file.write(r"\bgroup" + "\n")
    output_file.write(r"\def\arraystretch{1.8}" + "\n")
    output_file.write(r"\begin{tabular}{c|c|c}" + "\n")
    output_file.write(r"\hline" + "\n")
    output_file.write(r"Question & Points & Score \\" + "\n")
    output_file.write(r"\hline" + "\n")
    question_number = 1
    total = 0
    for question_loc in latex_question_list:
        point = int(question_loc.question.point_value)
        total += point
        output_file.write(str(question_number) + r" & " + str(point) + r" & \\" + "\n")
        output_file.write(r"\hline" + "\n")
        question_number += 1
    output_file.write(r"\hline" + "\n")
    output_file.write(r"Total & " + str(total) + r" & \\" + "\n")
    output_file.write(r"\hline" + "\n")
    output_file.write(r"\end{tabular}" + "\n")
    output_file.write(r"\egroup" + "\n")
    output_file.write(r"\medskip" + "\n\n")

    time_required = str(quiz_data.time_required_mins)
    output_file.write(r"Duration: " + time_required + r" minutes" + "\n\n")

    calculator = quiz_data.calculator_allowed
    computer = quiz_data.computer_allowed
    internet = quiz_data.internet_allowed
    book = quiz_data.book_allowed
    if calculator:
        output_file.write(r"Calculator allowed" + "\n\n")
    if computer:
        output_file.write(r"Computer allowed" + "\n\n")
    if internet:
        output_file.write(r"Internet allowed" + "\n\n")
    if book:
        output_file.write(r"Book allowed" + "\n\n")

    output_file.write(r"\end{flushright}" + "\n")
    output_file.write(r"}" + "\n")
    output_file.write(r"} %Ends helvetica" + "\n")

    # TODO: Supports here

    output_file.write(r"\begin{enumerate}" + "\n\n")
    # output_file.write(r"\clearpage" + "\n")
    output_file.write(r"\vspace{0.25cm}" + "\n")

    for question_loc in latex_question_list:
        latex_question = question_loc.question_latex
        point = int(question_loc.question.point_value)
        output_file.write(
            r"\item (" + str(point) + r" points) " + latex_question + "\n\n"
        )
        pages_required = question_loc.question.pages_required
        spacingString = pagesRequiredToSpacing(pages_required)
        output_file.write(r"\vspace{" + spacingString + r"}" + "\n\n")

    output_file.write(r"\end{enumerate}" + "\n")
    output_file.write(r"\end{document}" + "\n")

    output_file.close()

    # Path to pdflatex command
    pdflatex_path = r"C:\tools\TinyTeX\bin\windows\pdflatex"

    # Path to LaTeX file
    latex_file_path = (
        r"C:\Users\nrave\OneDrive\Documents\GitHub\mentoris\docs\latex\output_quiz.tex"
    )

    # Run pdflatex command
    process = subprocess.Popen(
        [pdflatex_path, latex_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    output, error = process.communicate()

    if error:
        print("Error occurred:")
        print(error.decode("utf-8"))
    else:
        print("PDF 1 generated successfully.")

    # Run twice to get the page numbers to load correctly
    process = subprocess.Popen(
        [pdflatex_path, latex_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = process.communicate()

    if error:
        print("Error occurred:")
        print(error.decode("utf-8"))
    else:
        print("PDF 2 generated successfully.")
