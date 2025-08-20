
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
[] create a test for this case  https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation
    Malicious Client then attempts to use refresh token 1 to get an access token. Auth0 recognizes that refresh token 1 is being reused, and immediately invalidates the refresh token family, including refresh token 2.

i believe they use a endpoint for manage the logic /authorize

[] i will like a test for this case but with 10 token simulated 10 devices https://auth0.com/docs/secure/tokens/refresh-tokens 
.Auth0 limits the amount of active refresh tokens to 200 tokens per user per application. 
This limit only applies to active tokens. If the limit is reached and a new refresh token is created, the system revokes and deletes the oldest token for that user and application.
    
[] /oauth/revoke. https://auth0.com/docs/secure/tokens/refresh-tokens/revoke-refresh-tokens invalidate tokens

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

logger python


