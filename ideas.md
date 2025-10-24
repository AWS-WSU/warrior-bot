# Ideas
This document will serve as a centralized place to brainstorm features and improvements for the CLI in order to make usage for users faster, more convienent, and complete.

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
`where ___` (building, restaurant, rec centers) -> address or building location
- ex. `where panda-express` -> "Wayne State University's very own Panda Express TM is located in the Student Center."
- ex. `where student-center` -> "The student center is located in the middle of campus. Look for the tall flag poles and ..."

`what ___` (schools, programs, clubs) -> general summary of that topic, ask to select a subtopic in particular and expand
- ex. `what programs` -> Lists WSU Academic Programs
- ex. `what clubs` -> Little bit about why participation in clubs is beneficial, list popular WSU clubs, resources (link to [GetInvolved](https://getinvolved.wayne.edu/)) to join clubs

`go ___` (campus-map, canvas, academic, degreeworks, class-schedule, academic-calendar, get-involved) -> direct link opens in web browser

Further hard-coded information ideas can be found by just looking at the WSU website, especially the [student subsection](https://wayne.edu/students), could implement web scraping with beautifulsoup or selenium if restricted, no API, or HTTP requests are blocked.

## CLI Useage
`about` -> summary of program, example commands, then suggestions of recommended usage
`help ___` (topic)