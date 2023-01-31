import os

from geocube import sdk
import multiprocessing



class TestClient:
    client = None
    @staticmethod
    def print_version(thread):
        if TestClient.client is None or not TestClient.client.is_pid_ok():
            print("create", os.getpid())
            TestClient.client = sdk.ConnectionParams("127.0.0.1:8080").new_client()
        print(thread, os.getpid(), TestClient.client.version())


    def test_multiprocess(self):
        TestClient.print_version("main")
        with multiprocessing.Pool(5) as p:
            p.map(TestClient.print_version, ["fork"]*10)




