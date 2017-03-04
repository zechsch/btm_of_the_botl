# botl
A location based social messaging service. Created by:

+ [Stephen Kline](mailto:srkline@umich.edu)
+ [Kevin Kuang](mailto:kkuang@umich.edu)
+ [Bahru Negash](mailto:bahrut@umich.edu)
+ [Zechariah Schneider](zechsch@umich.edu)
+ [Joshua Spigelman](jlspige@umich.edu)

# Endpoints:
## New Post
----
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

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{ error : "User doesn't exist" }`
