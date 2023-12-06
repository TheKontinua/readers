# Mentoris

The Kontinua Foundation is creating a curriculum for self-paced study
of math, computer science, and physics.

The mentors for the students using this curriculum will need quizzes
(and answer keys) for each chapter. Mentoris is the web app that will
supply them with those quizzes and answer keys.

Here is our [Technical Specification](https://github.com/TheKontinua/mentoris/files/13572053/Technical.Specification.-.Kontinua.docx.pdf) which outlines the entire project in more detail.


## Infrastructure

The web application will be open source. The primary programming
language used in this curriculum is Python, so the web app will be
written in Python using the Django web framework.

We will be using PostgreSQL as the backend database.

The questions and answers will be stored as LaTeX segments. The complete quiz will
need to be typeset using TeX. Preview will be done with MathJAX or KaTeX.

We will deploy the system on Amazon Services.

## Requirements

There are four kinds of users:

-   Newbie: new users who have not been promoted to a mentor
-   Mentor: those who proctor and grade the quizzes
-   QuizMaker: those who assemble the quizzes
-   Admin: those who can promote and disable other users

Things a Newbie needs to be able to do:

-   Edit profile
-   Change password
-   Request endorsements from existing mentors

Things a Mentor needs to be able to do:

-   Everything a Newbie can do
-   Download a PDF of a quiz for a particular chapter in a particular language
-   Suggest a question/answer/rubric for a particular chapter in a particular language in LaTeX
-   Translate a question and answer from one language into another
-   Give feedback on a quiz
-   Give feedback on a chapter
-   See mentor feedback

Things a QuizMaker needs to be able to do:

-   Everything a Mentor can do
-   Browse submitted questions, edit them, and approve them
-   Create supports
-   Assemble approved questions/supports into a quiz
-   Make previously approved questions not visible

Things an Admin needs to be able to do:

-   Everything a Quizmaker can do
-   See a list of Newbies waiting to be Mentors (with any endorsements)
-   Promote, demote, or disable a user
-   Delete quizzes
-   Delete mentor feedback

## Screens

#### Login page

-   Takes your email and password -> Main page
-   Links for create account -> New user page
-   Link for forgot password -> Lost password page

#### New user page

-   gets display name (must be unique), orgname, country code
-   one email
-   password (twice)
-   primary language
-   password is salted with user id and hashed with Argon2
-   Sends email to confirm email
-   Confirmation link takes you to profile page

#### Lost password page

-   Textfield for email address
-   Emailed link to reset password page
-   -   -> "Look in your email!" page

#### All inside pages

-   Account link to edit user info
-   Pending authentications? List of people who requested your authentication
-   Request for question translation? List of questions to be translated
-   Request for quiz feedback?
-   Quizmaker? List of questions needing approval (just admin's languages)
-   Quizmaker? List of new feedback on quizzes
-   Admin? Notification of new Newbies

#### Main page

-   Outline view of volumes/chapters
-   Get test for volume (randomly chosen, 2 PDFS, each to take 45 minutes)
-   Get test for chapter (randomly chosen, 1 PDF to take 45 minutes)
-   Submit question for chapter

#### Edit question page

-   Text area for LaTeX of question
-   Text area for LaTeX of answer
-   Text area for LaTeX of rubrik
-   conceptual difficulty rating
-   time required estimate
-   point_value (should be proportional to time)
-   iso language popup
-   Attachments -- allow uploading images to be included

#### Translate question page

-   Text area for LaTeX of question
-   Text area for LaTeX of answer
-   Text area for LaTeX of rubrik

#### Account page

-   Change password
-   Add/remove email addresses
-   Change primary email
-   Change display name
-   Change org name
-   Request authentication
-   Add/remove languages
-   Change primary language
-   Give lotitude/longitude
-   Change country code

#### Quiz feedback page

-   "You gave your students quiz 56A39B for the chapter 'Induction':
-   Appropriate difficulty?
-   Was supposed to take 45 minutes: Took appropriate amount of time?
-   Other comments?

#### Quiz designer page

-   Quizmakers only
-   Pick Chapter or Volume
-   Click "generate new quiz"
-   See preview
-   Ability to insert, update, delete question choices
-   Most quizzes include a low-difficulty question from previous chapters

### Question approval page

-   Get show question
-   Approve-> Next question needing approval
-   Edit -> Edit QuestionPage

#### Quiz feedback browser:

-   See only new feedback by default
-   Start with most negative feedback
-   Include link to quiz designer to improve quiz

#### Question browser

-   Select a chapter see all questions

## Entity-Relationship Diagram

<img src="docs/Database/er.png" alt="Entity-Relationship Diagram" style="width:1080px;"/>
