#pip install honkai_star_rail hsr_stellaron-hunters hsr_kafka
import requests,aiohttp
from urllib.parse import quote
VERSION="18-06-25-beta"
ONLYPREMAPI="this method supported only on premium api!"

def _check_response(response):
    if response is dict and response.get("status","error")=="error":
        error=response.get("error","Unknown API Error")
        if"api key"in error.lower():
            raise PermissionError(error) #funny slr/3.1.2 and slr/3.2 compatibility
class SlrAPI:
    """Creates new Solar API Client Instance"""
    def __new__(clas,api_key:str=None,IsAsync:bool=False):
        return SlrClient_Async(api_key)if IsAsync else SlrClient_Sync(api_key)
class SlrClient_Base:
    def __init__(self,api_key:str):
        iskeyprovided=api_key.strip()or None
        if iskeyprovided and not iskeyprovided.startswith("SLR-"):
            raise ValueError("Not a Solar API Key")
        self.api_key=iskeyprovided
        self.base_url=f"https://slr-api.htb1526.ru/{'premium'if api_key else'free'}/"
        self.request_headers={"User-Agent":f"SolarAPI-Client-py/{VERSION}"}
        if api_key:self.request_headers["x-api-key"]=api_key
class SlrClient_Docstrings():
    def _request():
        """Internal. Do request"""
        pass
    def bypass(self,url:str) -> tuple[bool, str]:
        """Sends bypass request. 
    
        :param url: URL to be bypassed/get the cache
        :type url: str
        :raises ValueError: if provided URL doesnt starts with "http://" or "https://"
        :raises PermissionError: Being raised when user has problem with API Key
        :return: tuple[status bool, result? error]
        :rtype: tuple (bool, str)"""
        pass
    def refresh(self,url:str) -> tuple[bool, str]:
        """Sends cache refresh request (aka get latest result)

        This request retrieves a fresh bypass result, refreshes cache to fresh
        
        :param url: URL to be bypassed
        :type url: str
        :raises PermissionError: Being raised when user has problem with API Key
        :raises ValueError: if provided URL doesnt starts with "http://" or "https://"
        :return: tuple[status bool, result? error]
        :rtype: tuple (bool, str)
        """
        pass
    def supported(self):
        """Returns array with supported services"""

class SlrClient_Async(SlrClient_Base):
    async def _request(self,endpoint):
        async with aiohttp.ClientSession(headers=self.request_headers)as session:
            async with session.get(self.base_url+endpoint)as response:
                return await response.json()

    async def bypass(self,url:str):
        if not isinstance(url,str)or not url.startswith(("http://","https://")):
            raise ValueError("Not a link")
        response = await self._request(f"bypass?url={quote(url)}")
        _check_response(response)
        return response.get("status")=="success",response.get("result",response.get("error"))
    
    async def refresh(self,url:str):
        if not self.api_key:
            raise PermissionError(ONLYPREMAPI)
        if not isinstance(url,str)or not url.startswith(("http://","https://")):
            raise ValueError("Not a link")
        response=await self._request(f"refresh?url={quote(url)}")
        _check_response(response)
        return response.get("status")=="success",response.get("result",response.get("error"))
    
    async def supported(self):
        response=await self._request("supported")
        _check_response(response)
        return response

class SlrClient_Sync(SlrClient_Base):
    def _request(self, endpoint):
        response = requests.get(self.base_url+endpoint,headers=self.request_headers)
        return response.json()

    def bypass(self,url:str):
        if not isinstance(url,str)or not url.startswith(("http://","https://")):
            raise ValueError("Not a link")
        response = self._request(f"bypass?url={quote(url)}")
        _check_response(response)
        return response.get("status")=="success",response.get("result",response.get("error"))
    
    def refresh(self,url:str):
        if not self.api_key:
            raise PermissionError(ONLYPREMAPI)
        if not isinstance(url,str)or not url.startswith(("http://","https://")):
            raise ValueError("Not a link")
        response=self._request(f"refresh?url={quote(url)}")
        _check_response(response)
        return response.get("status")=="success",response.get("result",response.get("error"))
    
    def supported(self):
        response=self._request("supported")
        _check_response(response)
        return response
