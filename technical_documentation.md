Quick Start Guide:
- Unpack prs.zip to a folder of your choice. Inside prs you'll find the following structure:
    - db --> Database Folder
    L- exampleDB.db --> use this file as db if you want to start with some registered users, uploaded and rated papers (with really inventive test-names)
    - static --> css files
    - templates --> html files
    app.py --> main program containing program logic, config and routes
    forms.py --> contains the wtforms
    requirements.txt --> pip freeze of required packages
    
- Make sure you have all packages installed as specified in requirements.txt
- Open app.py and specify a path to a db file of your choice in line 14
- Start the app (e.g. <python app.py>)
- Open a browser and navigate to http://localhost:5000/ | Remark: This program was developed and tested using Chrome
- No matter if you use the example db or a new db an admin user will be created with username 'admin', email 'admin@test.de' and password 'admin'. See lines 204ff in app.py. Login as an admin to access restricted sites
- You can signup as a new user by navigating to http://localhost:5000/signup or simply clicking on signup 
- As user you can access the first three items in the nav bar to the left:
    -> Overview -> Shows the status of submitted papers as well as the papers the logged in user can review
    -> Submit a paper -> Lets the user specify and submit a paper
    -> Rate a paper -> Lets the user rate papers he is eligble to rate
- As admin you can access the other two nav-items:
    -> Assign reviewers -> here youn can assign up to three authors to be reviewers of a paper
    -> Score overvierw -> Shows you a table with information about uploaded papers and their ratings. Here you can decide whether a paper gets accepted or not.
   

Design decisions:

- The PRS was developed using Python, the Framework flask and SqlAlchemy. 
- We used flask_bootstrap for easily extending a base.html as well as css. dashboard.html is basically our main html-template, most of the other .html-files derive from it (except for sites like login, 404...)
- For designing and displaying forms we used flask_wtf; for designing and displaying tables as in score_overview.html we used flask_table
- For access control we used flask_login and werkzeug.security for password hashing
- The many2many-relationships of PaperAuthors and PaperReviews are designed via association tables, and we created an extra table "Score" with key to the respective reviewer and paper containing the scores for a paper    