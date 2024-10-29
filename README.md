# TODOs:
- [x] pick framework
- [ ] pick db
- [ ] implement API
- [ ] write tests
- [ ] deploy
- [ ] write documentation



# Task: Build restful API for managing users and posts
- options:
    - /users, /posts
    /users:
        - GET: get all users = id, name, email
        - POST: create a new user; return user in JSON with unique id
    /users/:id:
        - PUT: update user by id; return updated user in JSON, or 404 if not found
        - DELETE: delete user by id; return 204 if successful, 404 if not found


    /posts:
        - GET: get all posts = id, title, content, user_id
        - POST: create a new post with above params; return post in JSON with unique id. if user_id is not found, return 400
    /posts/:id:
        - GET: get post by id; return post in JSON, or 404 if not found
        - PUT: update post by id, with title, content, user_id in request body; return updated post in JSON, or 404 if not found. 400 if user_id not found
        - DELETE: delete post by id; return 204 if successful, 404 if not found

- storage options: any (in-memory, file, relational db, etc)
- clear and concise documentation including
    - expected request/response formats
    - assumptions
    - possible error codes and messages
- write unit tests
Bonus: deploy to any cloud platform
    - Provide a public URL for API
    - Ensure accessible and functional
    - brief deploy explanation
    - writeup steps, tools, challenges


# Notes

Design Decisions:
- Framework or no?
    - Normally I'd go for Flask to do this quickly, but I've never used FastAPI, might as well use an interview problem as a chance to learn
        - *On the job I'd evaluate requirements*


- DB?
    - debating between sqlite and mongo. *if this was a production app, relational would be my goto because scaling NoSQL has numerous pain points*

- Deploy cloud?
    - maybe aws or netlify, cross that bridge when I get there
