import requests
import json
from typing import List, Dict

from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

class WordPressHostingService(BaseModel):
    unqiue_service_name: str
    starting_price: Optional[str] = None
    description: Optional[str] = None
    features: Optional[str] = None
    uptime_guarantee: Optional[str] = None
    security_features: Optional[str] = None
    backup_options: Optional[str] = None
    free_domain: Optional[str] = None
    money_back_guarantee: Optional[str] = None
    details: Optional[str] = None
    affiliate_link: Optional[str] = None

from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.generic_loader import load_content
from SimplerLLM.language.llm_addons import generate_pydantic_json_model

llm_instance = LLM.create(provider=LLMProvider.OPENAI, model_name="chatgpt-4o-latest")

def get_url_content(url: str) -> str:
    web_content = load_content(url)
    return web_content.content

def extract_hosting_info(content: str) -> str:
    prompt = f"""
    Analyze the following web page content about a WordPress hosting service and extract the following information :
    - the service name (website name)
    - pricing
    - service description
    - features desciption
    - uptime guarantee info
    - security features info
    - backup options
    - provides free domain ?
    - money back guarantee
    - details (any additional important information about the service)

    If info is not found, just skip it

    Content:
    {content}
    """

    response = llm_instance.generate_response(max_tokens=16000,prompt=prompt)
    return response

def generate_hosting_json(content: str) -> WordPressHostingService:
    prompt = f"""
    Analyze the following content about WordPress hosting service and turn into JSON format with these fields:
    - unqiue_service_name
    - starting_price
    - description
    - features desciption
    - uptime_guarantee
    - security features
    - backup_options
    - free_domain
    - money_back_guarantee
    - details (any additional important information)

    If a field is not found, use null.

    Content:
    {content}
    """

    json_response = generate_pydantic_json_model(max_tokens=16000,prompt=prompt, model_class=WordPressHostingService, llm_instance=llm_instance)
    return json_response

def generate_affiliate_link(url: str, service_name: str) -> str:
    return f"https://affiliate.link/{service_name.lower().replace(' ', '-')}"

def scrape_wordpress_hosting(urls: List[str]) -> List[WordPressHostingService]:
    all_services = []

    for url in urls:
        try:

            content = get_url_content(url)
            text_info = extract_hosting_info(content)
            service_info = generate_hosting_json(text_info)
            
            if isinstance(service_info, WordPressHostingService):
                service_info.affiliate_link = generate_affiliate_link(url, service_info.unqiue_service_name)
                all_services.append(service_info)
            elif isinstance(service_info, (list, tuple)):
                for service in service_info:
                    service.affiliate_link = generate_affiliate_link(url, service.unqiue_service_name)
                    all_services.append(service)
        except Exception as e:
            print(e)
            pass

    return all_services

def main():
    urls = [
        "https://www.hostinger.com/wordpress-hosting",
        "https://world.siteground.com/wordpress-hosting.htm",
        "https://www.bluehost.com/wordpress/wordpress-hosting",
        "https://www.greengeeks.com/wordpress-hosting",
    ]

    wordpress_hosting_services = scrape_wordpress_hosting(urls)

    with open('wordpress_hosting_services.json', 'w') as f:
        json.dump([service.dict() for service in wordpress_hosting_services], f, indent=2)

if __name__ == "__main__":
    main()