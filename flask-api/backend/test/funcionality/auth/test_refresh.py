from backend.repositories.refresh_token_repository import RefreshTokenRepository
import bcrypt

def test_refresh_token(client, gen_token, db_session):
    """
    GIVEN a refresh token in a cookie
    WHEN  the endpoint of auth/refresh receives a valid refresh token
    THEN generate a new access token and refresh token
    """

    salt = bcrypt.gensalt()
    refresh_token_prev = gen_token["tokens"]["refresh_token"].encode('utf-8')
    refresh_token_hashed = bcrypt.hashpw(refresh_token_prev, salt)
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    user_id = gen_token["user"]["id"]

    RefreshTokenRepository(db_session).create_refresh_token(
        token_hash=refresh_token_hashed.decode('utf-8'),
        user_agent=user_agent,
        user_id=user_id,
    )

    client.set_cookie(
        'refresh_token',
        value=gen_token["tokens"]["refresh_token"],
        samesite='None',
        httponly=True,
        secure=True
    )

    response = client.get('/auth/refresh')
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert data["message"] == "Generate token successful"

def test_refresh_token_expired(client, gen_token, db_session):
    """
    GIVEN a refresh token in a cookie expired
    WHEN  the endpoint of auth/refresh receives an expired refresh token
    THEN failed in generating a new access token and refresh token and return an error
    """

    salt = bcrypt.gensalt()
    refresh_token_prev = gen_token["tokens"]["refresh_token"].encode('utf-8')
    refresh_token_hashed = bcrypt.hashpw(refresh_token_prev, salt)
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    user_id = gen_token["user"]["id"]

    RefreshTokenRepository(db_session).create_refresh_token(
        token_hash=refresh_token_hashed.decode('utf-8'),
        user_agent=user_agent,
        user_id=user_id,
    )


    client.set_cookie(
        'refresh_token',
        value=gen_token["tokens"]["refresh_token"],
        samesite='None',
        httponly=True,
        secure=True
    )

    response = client.get('/auth/refresh')
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert data["message"] == "Generate token successful"
