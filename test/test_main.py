from  fastapi.testclient import  TestClient
import  main
from  fastapi import  status

client  =  TestClient(main.py)

def test_return_health_check():
    respone =  client.get("/healthy")
    assert  respone.status_code == status.HTTP_200_OK
    assert  respone.json() == {"status" : "healthy"}