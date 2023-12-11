# ParallelReddit-gRPC
`ParallelReddit-gRPC` is a gRPC-based, Reddit-style social media project. It includes API endpoints for posts, comments, and voting, with a focus on client-server communication and optional real-time updates. Ideal for demonstrating API design and networking.
Important commands:
python3 -m unittest test_api_endpoints.py 
python3 high_level_function.py   
python3 test_high_level_function.py   
python3 reddit_server.py  
python3 reddit_client.py  
python3 -m grpc_tools.protoc -I../protos --python_out=. --pyi_out=. --grpc_python_out=. ../protos/reddit.proto