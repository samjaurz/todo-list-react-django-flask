from backend.test.conftest import client
from backend.repositories.refresh_token_repository import RefreshTokenRepository
import bcrypt

def test_verification_user(client, gen_token, db_session):
    """
    GIVEN an authorized token and data for make the tasks
    WHEN the token is validated the tasks is created with the data
    THEN return a status code 201 and a json object with the tasks data
    """

    client.set_cookie(
        'refresh_token',
        value=gen_token["tokens"]["refresh_token"],
        samesite='None',
        httponly=True,
        secure=True
    )

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

    response = client.get(f'/auth/verification',  headers={"Authorization": f"Bearer {gen_token['tokens']['access_token']}"})

    assert response.status_code == 200
    data = response.get_json()
    print(data)