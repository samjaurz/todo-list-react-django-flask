
TOKENS
refresh token
the refresh token only used for get a new access token 
the logic decorator auth is wrong because the access token is not sent in the cookie only the refresh token is safe there
the access token is sent in the headers["authorized"]

[x] update logic sing up / login
[] update decorator
[] database blacklist for refresh tokens 
[] manage the logic of refresh token validate the refresh in database, 
    generate a new access,refresh token replace the value teh refresh token in database retrieve tokens

TEST
[] creates tests for user routes.  
    route_user =  in the endpoint where is not given and user_id, the decorator not return the user_id
[] the test for failing are corrects ?? 


LOGIN/SIGNUP
[] improve logic validation in backend
[] improve logic validation front for user experience 

REFACTOR 
[] clean de code frontend prop drilling 

DOCKER
[] Volumes user admin 1


