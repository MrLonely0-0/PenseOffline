from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def try_login():
    resp = client.post("/users/login", json={"username": "alice", "password": "password"})
    print("STATUS:", resp.status_code)
    print("BODY:", resp.text)

if __name__ == '__main__':
    try_login()
    # further smoke tests
    print('\n--- SMOKE TESTS ---')
    token_resp = client.post("/users/login", json={"username": "alice", "password": "password"})
    token = token_resp.json().get('access_token')
    headers = {"Authorization": f"Bearer {token}"}

    r = client.get("/profiles/ranking", headers=headers)
    print('/profiles/ranking', r.status_code)
    print(r.text)

    r = client.get('/communities/', headers=headers)
    print('/communities/', r.status_code)
    print(r.text)

    # try to join first community
    import json
    comms = r.json()
    if comms:
        cid = comms[0].get('id')
        r2 = client.post(f'/communities/{cid}/join', headers=headers)
        print(f'/communities/{cid}/join', r2.status_code, r2.text)

    # attend first event
    r3 = client.get('/events/', headers=headers)
    print('/events/', r3.status_code)
    events = r3.json()
    if events:
        eid = events[0].get('id')
        r4 = client.post(f'/events/{eid}/attend', headers=headers)
        print(f'/events/{eid}/attend', r4.status_code, r4.text)
