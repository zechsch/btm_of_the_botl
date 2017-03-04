# botl
A location based social messaging service. Created by:

+ [Stephen Kline](mailto:srkline@umich.edu)
+ [Kevin Kuang](mailto:kkuang@umich.edu)
+ [Bahru Negash](mailto:bahrut@umich.edu)
+ [Zechariah Schneider](zechsch@umich.edu)
+ [Joshua Spigelman](jlspige@umich.edu)

# Endpoints:

/api/new_post
methods: POST
required parameters: 5
JSON object for request:
{
    "latitude": Lat,
    "longitude": Long,
    "message": msg,
    "thread_id": thread,
    "user_id": uid,
}
