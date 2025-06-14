# Solar API Wrapper (Python)
#### This is Solar API client wrapper for interacting w/Solar Bypass API, allowing bypass ad-links

## Features of wrapper:
#### simple initialization and usage
#### sync/async
#### automatically detects free/premium usage mode

## Quick start:
### Initialize client
```python
from SolarBypass import SlrAPI, SlrClient_Docstrings

api_key="SLR-your-api-key-here"
client:SlrClient_Docstrings=SlrAPI(api_key,IsAsync=False) # sync client
client_async:SlrClient_Docstrings=SlrAPI(api_key,IsAsync=True) # async client
```
#### If no API Key provided, client operates in Free API Mode
### Usage
```python
Success_0,Result_0=client.bypass("https://example.com")
print(Success_0,Result_0) # True, "Example bypass result"
Success_1,Result_1=await client_async.refresh("https://example.com")
print(Success_1,Result_1) #True, "Example new, fresh result"
```
