Current status
--------------

There is a `/predict` endpoint! It works! We tested with a few different images, all SFW because we're in a coworking space and don't want people to think bad things about us...
Preliminary results: cats are safer than dogs xD

Implemented a `/task/<task_id>` endpoint to get the results of the tasks triggered. An example of the interaction:


```
dcaro@vulcanus$ curl -i -X POST -H "Content-Type: multipart/form-data" -F "image=@jura.png" http://127.0.0.1:5000/predict
HTTP/1.1 100 Continue

HTTP/1.1 100 Continue

HTTP/1.1 200 OK
Server: Werkzeug/2.1.2 Python/3.9.13
Date: Fri, 15 Jul 2022 08:19:35 GMT
Content-Type: application/json
Content-Length: 56
Connection: close

{
  "task_id": "0387051d-4bc1-46c8-93c1-4eee2c4e05db"
}

##### Now we ask for the results
10:19 AM ~/Downloads
dcaro@vulcanus$ curl http://127.0.0.1:5000/task/0387051d-4bc1-46c8-93c1-4eee2c4e05db
{
  "error": null,
  "result": "{'prediction': 'suitable', 'confidence': 0.9987327456474304}",
  "state": "SUCCESS",
  "task_id": "0387051d-4bc1-46c8-93c1-4eee2c4e05db"
}
```
