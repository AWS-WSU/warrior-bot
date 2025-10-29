# Overview
This document will serve as a centralized place to brainstorm features and improvements for the CLI (command line interface) in order to make usage for users faster, more convienent, and complete. Because we all come from different backgrounds with differing experience levels, in order to make the reader's life easier, we have included a brief glossary of acronyms below. You do **not** need to know what they all mean. This list is included to help you create an mental idea of that particular feature and to motivate you to research the subject on your own. 
- CLI - Command Line Interface
- RSS - Really Simple Syndication
- API - Application Programming Interface
- JSON - JavaScript Object Notation
- SQL - Structured Query Language
- XML - Extensible Markup Language (yes, the acronym is a lie \:)
- HTTP - HyperText Transfer Protocol
- HTTPS - HyperText Transfer Protocol Secure

We encourage every reader to learn more about these topics and give in to their own curiosities. This is less of a recommendation when it comes to working on a feature that uses that particular technology. There is always something to learn. You do not need to become a master in a topic by any means, but spend about an hour reading the documentation for each technology and *truly* understanding the associated examples. This helps make sure every contributor is pulling equally for a feature. Your fellow contributors will appreciate the work you put in to actually understanding the technologies and frameworks we work with and reading the documentation. There are so many frameworks, languages, data structures, algorithms, paradigms, VCS's, etc. that in order to build a successful career as a software engineer, one must invest the time to learn and practice these technologies. You will fail often. Try often and don't hesitate to ask questions if you get completely stuck.

# Ideal Feature Implementation Order
#### 1. Base `about` & `help` Commands
Code commands taht are crucial for a smooth user experience by providing a resource to learn.
#### 2. Base `where`, `what`, `whois`, `go` Commands
Code base commands with a couple hard-coded entries for each just to prove each concept and have some examples to build the more complicated, flagged commands for later.
#### 3. RSS Feed
Use [WSU Digital Commons](https://digitalcommons.wayne.edu/open_data/announcements.html) RSS feeds to provide up to date information for general or specific topics (can be configured by user). RSS is provided in XML format so we can use the built-in xml lib for python3 for easy formatting. The feed will need to be polled often to take advantage of what it offers: up to date information.
#### 4. Canvas API
Please see [Canvas API Section](#canvas-api)
#### 5. Web Scraping -> JSON or SQL
This can be used as Plan B if we cannot get Canvas API keys working (as we need admin approval not to mention every user will need to do this for their Canvas feature to work) *but* also as extra information in the case that the Canvas API does work. Contributors can use the beautifulsoup or selenium web scraping libraries to accumlate data that can be stored in either a JSON (for smaller datasets) or an SQL (for larger datasets, preferably SQLite b/c we are running the app on the user's local filesystem) and read from using the native python3 [JSON](https://docs.python.org/3/library/json.html) lib or [sqlite3](https://docs.python.org/3/library/sqlite3.html) lib. The use of automation through scripts is encouraged here and as such there is still a lot of programming to be done. Please see [Gathering Data Section](#gathering-data).
#### 6. Reiterate Over Base Functions (Flags)
At this point we will have an excellent basis for the app and what is left is to continue gathering/updating information, adding features, fixing bugs, and possibly redoing the UI.

## Canvas API
[Canvas API Documentation](https://developerdocs.instructure.com/services/canvas/oauth2/file.oauth)
Need C/IT admin approval to allow students to generate tokens -> Dead End?
#### Possible API Integrations
- Check grades
- View courses
- View schedule
- View people
- View directory of files (modules)
- Download course material

## General, Hard-Coded Information
`about` -> summary of program, example commands, then suggestions of recommended usage

`help ___` (topic) -> explanation + examples for that specific topic

`where ___` (building, restaurant, rec centers) -> address or building location
- ex. `where panda-express` -> "Wayne State University's very own Panda Express TM is located in the Student Center."
- ex. `where student-center` -> "The student center is located in the middle of campus. Look for the tall flag poles and ..."

`what ___` (schools, programs, clubs) -> general summary of that topic, ask to select a subtopic in particular and expand
- ex. `what programs` -> Lists WSU Academic Programs
- ex. `what clubs` -> Little bit about why participation in clubs is beneficial, list popular WSU clubs, resources (link to [GetInvolved](https://getinvolved.wayne.edu/)) to join clubs

`whois ___` (person) -> general summary of WSU admin, faculty, or other important university leaders such as WSUPD chief, department chairs, and department deans
- ex. `whois president` -> Richard A. Bierschbach (Interim)
- ex. `whois Anthony-Holt` -> WSUPD Chief

`go ___` (campus-map, canvas, academic, degreeworks, class-schedule, academic-calendar, get-involved) -> direct link opens in web browser

## Gathering Data
Further hard-coded information ideas can be found by just looking at the WSU website, especially the [student subsection](https://wayne.edu/students), could implement web scraping with [beautifulsoup](https://beautiful-soup-4.readthedocs.io/en/latest/) (also useful for parsing XML) or [selenium](https://selenium-python.readthedocs.io/) if restricted, no API, or HTTP requests are blocked.