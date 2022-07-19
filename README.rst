Current status
--------------

There is a `/predict` endpoint! It works! We tested with a few different images, all SFW because we're in a coworking space and don't want people to think bad things about us...
Preliminary results: cats are safer than dogs xD

Implemented a `/task/<task_id>` endpoint to get the results of the tasks triggered. An example of the interaction::


  dcaro@vulcanus$ curl -i -X POST -H "Content-Type: multipart/form-data" -F "image=@myimage.png" http://127.0.0.1:5000/predict
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

Implemented also a GET version of `/predict` that accepts a `image_url` parameter (url from https://upload.wikimedia.org)::


 dcaro@vulcanus$ curl -vv 'http://127.0.0.1:5000/predict?image_url=https://upload.wikimedia.org/wikipedia/commons/5/57/Puesta_de_sol%2C_desierto_de_Namib%2C_Namibia%2C_2018-08-05%2C_DD_84-90_PAN.jpg'
 < HTTP/1.1 200 OK
 < Server: Werkzeug/2.1.2 Python/3.9.13
 < Date: Fri, 15 Jul 2022 17:25:21 GMT
 < Content-Type: application/json
 < Content-Length: 56
 < Connection: close
 {
   "task_id": "27ac478e-8712-4a87-a10a-b0ec2eb18eb4"
 }

 07:25 PM ~/Work/repos/per_user/blancadesal/cv-model-serve  (main|✚ 1)
 dcaro@vulcanus$ curl -vv 'http://127.0.0.1:5000/task/27ac478e-8712-4a87-a10a-b0ec2eb18eb4'
 {
   "error": null,
   "result": "{'prediction': 'suitable', 'confidence': 0.9997747540473938}",
   "state": "SUCCESS",
   "task_id": "27ac478e-8712-4a87-a10a-b0ec2eb18eb4"
 }

Installation
============

This will be focused only on cloud VPS for now, and on a single machine.

Horizon/Cloud VPS settings
~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the following class to the VM 'puppet config'->'puppet classes' section in horizon:

 profile::docker::engine

Create a security group that allows accessing the port 5000 from the horizon UI, and add the server to that group.

And at last create a proxy to point to that machine to the port 5000.

VM setup
~~~~~~~~
Then make sure puppet runs:

 $ run-puppet-agent

Install docker compose plugin (source https://docs.docker.com/compose/install/compose-plugin/):

 $ DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}

 $ mkdir -p $DOCKER_CONFIG/cli-plugins

 $ curl -SL https://github.com/docker/compose/releases/download/v2.6.1/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose

 $ chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose

Then clone this repository:

 $ git clone https://github.com/blancadesal/cv-model-serve.git

Running the app
===============

Just build the containers if you have not done it before (or the code changed):

 $ cd path/to/git/repo

 $ docker compose build

Start the containers, using 3 celery workers:

 $ docker compose up -d web celery_worker --scale celery_worker=3

Note that we don't really need the flower container for production, only for development.
Also, you can use more celery workers if needed, usually one per CPU - 1.

Restarting the app
~~~~~~~~~~~~~~~~~~
Sometimes you want to restart it, so just:

 $ docker compose stop
 $ docker compose up -d web celery_worker --scale celery_worker=3

Rebuilding the containers
~~~~~~~~~~~~~~~~~~~~~~~~~
When the code changes, or to pull fresh dependencies you might want to rebulid the containers:

 $ docker compose build
