# Friends graph

In order to persists profiles and their relationships Neo4j is used. 

Neo4j is a graph oriented database. It helps to execute operations on graphs really quickly. It perfectly fits a production workload.

Backend is implemented by using FastApi. And it exposes 2 APIs:

1) GET get-friends/<profile_id>. According to tech requirements it accepts an id of a profile and returns list of it's friends ids.
    
    Example query:
    GET http://localhost/get-friends/9 returns [2,4,5,6,7,8] (that was in my particular case, in your case ids can be different)
2) POST /find-shortest-connection. According to requirements it should return a list of shortest friends connection between 2 profiles.

    Example: 
    POST http://localhost/find-shortest-connection with body {"from_id": 3, "to_id": 7} returns [3,2,9,7] (in my case, in your env the result may be different)

    I exported postman collection with POST request configuration, so that you can simply import it into postman and use. the configuration is located in the project root - 'New Collection.postman_collection.json'

## How to run
1) `docker-compose build`
2) `docker-compose run web python profiles_generator.py` It will run the seeder script and ask you for input 2 values: ProfilesTotal and FriendsConnectionsTotal.
2) `docker-compose up`
3) go to http://localhost/ in order to make an API calls.

## How to check the generated graph
1) go to http://localhost:7474/browser/ and click 'Connect' as default creds are used
2) In the command input run `MATCH (n:Profile) RETURN n LIMIT 25` it will show you the generated graph.
![Screenshot link] (https://drive.google.com/file/d/13-xXXovwS7PgmAZPccKnDyZ0Oo0gRj0u/view?usp=sharing)

    
## API examples:

My randomly generated graph looks like this:
https://drive.google.com/file/d/13-xXXovwS7PgmAZPccKnDyZ0Oo0gRj0u/view?usp=sharing

1) GET http://localhost/get-friends/9
As a result we see [2,4,5,6,7,8] - that is profiles directly connected with with 9th profile.
Screenshot link: https://drive.google.com/file/d/1XwjCcQXAsLMbSHWqAwqzWLq-s37TQuBF/view?usp=sharing

2) POST http://localhost/find-shortest-connection with body {"from_id": 3, "to_id": 7} returns [3,2,9,7] - that is the shortest path from 3 to 7
Screenshot link: https://drive.google.com/file/d/1fgQ4VXbQN0y9qHeFzMIcZ1Yo67rnaUJm/view?usp=sharing

## How to reset the system
1) `docker rm $(docker ps -aq) -f` in case you work on mac/linux
2) repeat steps from 'How to run'