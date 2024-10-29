# TODOs:
- [x] pick framework
- [x] pick db
- [x] implement API
  - [x] users
    - [x] unique id assignment
      - currently POST and PUT are the same until i get rid of the id param in POST 
    - [x] error codes on /users
  - [x] posts
- [x] write tests
- [x] deploy
- [X] write documentation

- [X] unify json responses? (n/a)

# Task: Build restful API for managing users and posts
- options:
    - /users, /posts
    /users:
        - GET: get all users = id, name, email
        - POST: create a new user; return user in JSON with unique id
    /users/:id:
        - GET, 404 if not found
        - PUT: update user by id; return updated user in JSON, or 404 if not found
        - DELETE: delete user by id; return 204 if successful, 404 if not found

    - /posts:
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
- [x] Framework or no?
    - Normally I'd go for Flask to do this quickly, but I've never used FastAPI, might as well use an interview problem as a chance to learn and see if it poses challenges i didn't expect
        - *On the job I'd evaluate requirements*
        - interesting FastAPI features: type hinting, data validation, doc generation, starlette/pydantic under the hood

- [X] DB? probably going with in-memory
    - ~~debating between sqlite and mongo. *if this was a production app, relational would be my goto because scaling NoSQL has numerous pain points*~~
- Deploy cloud?
    - maybe aws or netlify, cross that bridge when I get there
- Testing?
    - Starlette makes pytest easy so lets go with that


```
curl -X POST http://localhost:8000/users/ \
     -H 'Content-Type: application/json' \
     -d '{"id": 1, "name": "Ankeet", "email": "my@email.address"}'
     
```
works! 


Rather enjoying the straightforwardness of FastAPI so far. Makes JSON-based RESTful design pretty easy

Challenges of using a new framework are showing up:
- since it does abstract away a bunch of stuff to give REST-first data models i wonder if i should create a custom class for JSON responses (eg indicate success)
- i gave user_id as an input parameter and kind of steamed ahead, assuming i'd refactor later, but now i'm going to have to refactor most user tests

1 hour in, let's take a break.
Okay, starting up with posts. I'll probably do the ID refactoring now
- wasn't too bad, just need to create an intermediary object

- FastAPI auto generates swagger docs at /docs


