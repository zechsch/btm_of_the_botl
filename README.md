# botl
A location based social messaging service. Created by:

+ [Stephen Kline](mailto:srkline@umich.edu)
+ [Kevin Kuang](mailto:kkuang@umich.edu)
+ [Bahru Negash](mailto:bahrut@umich.edu)
+ [Zechariah Schneider](zechsch@umich.edu)
+ [Joshua Spigelman](jlspige@umich.edu)

# To deploy:
* **Botl Devs**
Push to Heroku with
    git push heroku master

* **Others**
You can deploy this API by creating a heroku account and app,
adding the postgresql plugin, pushing all code to Heroku, and running initialization scripts with
```
heroku pg:psql
\i postsinit.sql;
\i create_user_tables.sql;
```

Viola! Your API is deployed and running.

# Endpoints:
## New Post
  Adds a new post.

* **URL**

  /api/new_post

* **Method:**

  `POST`

* **Data Params**

  + latitude (long)
  + longitude (long)
  + message (string)
  + user_id (int)

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ status : OK }`

* **Error Response:**

  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{ error : "User doesn't exist" }`

  * **Code:** 405 METHOD NOT ALLOWED <br />
    **Content:** `{ error : "Method not allowed"}`

## Rate Post
  Edits rating for a post

* **URL**

  /api/rate_post

* **Method:**

  `POST`

* **Data Params**

  + post (int)
  + vote (string) [up/down]

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ status : OK }`

* **Error Response:**

  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{ error : "Internal server error" }`

  * **Code:** 405 METHOD NOT ALLOWED <br />
    **Content:** `{ error : "Method not allowed"}`

## Reply
  Reply to a post

* **URL**

  /api/reply

* **Method:**

  `POST`

* **Data Params**

  + thread (int)
  + message (string)
  + user (int)

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ status : OK }`

* **Error Response:**

  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{ error : "Internal server error" }`

  * **Code:** 405 METHOD NOT ALLOWED <br />
    **Content:** `{ error : "Method not allowed"}`

## Get Thread
  Get an entire thread. Returns every message in a thread

* **URL**

  /api/get_thread

* **Method:**

  `POST`

* **Data Params**

  + post_id (int)

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
    "Status":"OK,
    "thread_id":thread_id,
    "thread" : [
      {
        "message":"original Message",
        "user":Op user_id
      },
      {
        "message":"response 1",
        "user":response owner
      }
      ...
      ]
      }`
## Get Posts
  Get nearby posts in a given radius. Returns a list of messages.

* **URL**

  /api/get_posts

* **Method:**

  `POST`

* **Data Params**

  + distance  (float)
  + num_posts (int)
  + latitude  (float)
  + longitude (float)

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{
    "Status":"OK,
    "posts" : [
      {
        "post_id"=post_id,
        "user_id"=user_id,
        "latitude"=latitude,
        "longitude"=longitude,
        "rating"=rating,
        "message"=msg
      },
      {
      "post_id"=post_id,
        "user_id"=user_id,
        "latitude"=latitude,
        "longitude"=longitude,
        "rating"=rating,
        "message"=msg
      }
      ...
      ]
      }`

* **Error Response:**

  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{ error : "Internal server error" }`

  * **Code:** 405 METHOD NOT ALLOWED <br />
    **Content:** `{ error : "Method not allowed"}`
