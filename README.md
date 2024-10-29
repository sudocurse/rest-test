# Takehome


Prod: https://ankeet-lightbox.vercel.app/

Docs: https://ankeet-lightbox.vercel.app/docs

Repo: https://www.github.com/sudocurse/rest-test


To run locally:
```
## in your python env, python=3.10+
pip install -r requirements.txt
fastapi dev app/main.py
```

to test:
```
pytest app/tests
```

## Design Decisions
* Used FastAPI to try something new, worked out surprisingly well
    * Pydantic for data validation
    * pytesting is easy with TestClient
    * Docs autogenerated, just need to add to the annotations
* Data in-memory for simplicity and workflow speed


* Devlog is in devlog.md for more thoughts, you can examine git commits as well

## Assumptions and Challenges
- Assumptions I've made: 
  - Dummy project so no auth or  security, no availability, no pagination or filtering
    - eg anyone can attest a post to any user
  - Data is not persistent
  - User IDs are UUIDs while post IDs are incrementing ints based on length of posts dict
    - This means that if post 2 is deleted, the next post will still be 2, so non-unique in that sense
 
- Slowdowns were mostly in bug fixes, type hinting and tests came in handy immediately

- Deployment:
  - Learned netlify no longer supports python serverless functions
  - Vercel for deployment was very quick: make a vercel.json & push to git

## Testing commands

```
# Create a user
curl -iLX POST http://ankeet-lightbox.vercel.app/users/ -H 'Content-Type: application/json' -d '{"name": "Name", "email": "abcd"}'

# List all users
curl -iL http://ankeet-lightbox.vercel.app/users/

# Grab ID from last user
ID=$(curl -L http://ankeet-lightbox.vercel.app/users/ | jq -r '.[-1].id')

# Get a specific user by ID
curl -iL http://ankeet-lightbox.vercel.app/users/$ID

# Update a specific user by ID
curl -iLX PUT http://ankeet-lightbox.vercel.app/users/$ID -H 'Content-Type: application/json' -d '{"name": "Changed Name", "email": "abcd"}'

# Delete a specific user by ID
curl -iLX DELETE http://ankeet-lightbox.vercel.app/users/$ID

# Attempt to get the deleted user to confirm deletion
curl -iL http://ankeet-lightbox.vercel.app/users/$ID

# Create another user to associate posts with
ID=$(curl -LX POST http://ankeet-lightbox.vercel.app/users/ -H 'Content-Type: application/json' -d '{"name": "Name", "email": "abcd"}' | jq -r '.id')

# Create a post with the user ID extracted
curl -iLX POST http://ankeet-lightbox.vercel.app/posts/ \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Title\", \"content\": \"Content\", \"user_id\": \"$ID\"}"

# List all posts
curl -iL http://ankeet-lightbox.vercel.app/posts/

# Grab the post ID
POST_ID=$(curl -L http://ankeet-lightbox.vercel.app/posts/ | jq -r '.[-1].id')

# Get a specific post by ID
curl -iL http://ankeet-lightbox.vercel.app/posts/$POST_ID

# Update a specific post by ID
curl -iLX PUT http://ankeet-lightbox.vercel.app/posts/$POST_ID \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"Changed Title\", \"content\": \"Changed Content\", \"user_id\": \"$ID\"}"


# Delete a specific post by ID
curl -iLX DELETE http://ankeet-lightbox.vercel.app/posts/$POST_ID

# Attempt to get the deleted post to confirm deletion
curl -iL http://ankeet-lightbox.vercel.app/posts/$POST_ID

```