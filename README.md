# botl
A location based social messaging service. Created by:

+ [Stephen Kline](mailto:srkline@umich.edu)
+ [Kevin Kuang](mailto:kkuang@umich.edu)
+ [Bahru Negash](mailto:bahrut@umich.edu)
+ [Zechariah Schneider](zechsch@umich.edu)
+ [Joshua Spigelman](jlspige@umich.edu)

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
  + thread_id (int)
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

  + thread (int)

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{ 
    thread : [
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

* **Error Response:**

  * **Code:** 500 INTERNAL SERVER ERROR <br />
    **Content:** `{ error : "Internal server error" }`

  * **Code:** 405 METHOD NOT ALLOWED <br />
    **Content:** `{ error : "Method not allowed"}`
