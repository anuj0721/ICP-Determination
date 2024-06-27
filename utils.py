from openai import OpenAI
from decouple import config
import requests


PERPLEXITY_API_KEY = config("PERPLEXITY_API_KEY")
PROXYCURL_API_KEY = config("PROXYCURL_API_KEY")


def fetch_company_offerings(company_url: str):

    messages = [
        {
            "role": "system",
            "content": (
                '''
                    You are an EXPERT BUSINESS RESEARCHER tasked with ANALYZING a company to IDENTIFY and SUMMARIZE their KEY PRODUCT AND SERVICE OFFERINGS as well as their PRICING MODELS AND PRICING INFORMATION.
                    REQUIREMENTS:
                    - EXTRACT 3-5 of the MOST SIGNIFICANT offerings that define the company's core business 
                    - For each offering, provide a CONCISE 1-2 sentence description capturing its KEY VALUE PROPOSITION 
                    - EXTRACT 3-5 of the MOST SIGNIFICANT pricing models that define the company's pricing strategy 
                    - For each pricing model, provide a CONCISE 1-2 sentence description capturing its KEY FEATURES and VALUE 
                    - If available, include any specific pricing information or ranges associated with each model 
                    - If pricing information is not available, clearly state that "Pricing information is not available" 
                    - ORGANIZE the findings in a CLEAR, EASY-TO-READ BULLET POINT FORMAT - Only output the bullet points
                '''
            ),
        },
        {
            "role": "user",
            "content": (
                f"Company: {company_url}"
            ),
        },
    ]

    client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="llama-3-sonar-large-32k-online",
        messages=messages,
    )
    return response.choices[0].message.content


def fetchCompanyDetailsFromProxycurl(company_domain):

    result = {}

    url = "https://nubela.co/proxycurl/api/linkedin/company/resolve"
    headers = {"Authorization": f"Bearer {PROXYCURL_API_KEY}"}
    params = {
        "company_domain": company_domain
    }

    response = requests.get(url, headers=headers, params=params)

    data = response.json()
    if "url" not in data or data["url"] is None:
        return result

    result["linkedin_url"] = data["url"]

    url = "https://nubela.co/proxycurl/api/linkedin/company"
    params = {
        "url": result["linkedin_url"],
        "extra": "include",
        "use_cache": "if-recent"
    }

    response = requests.get(url, headers=headers, params=params)

    data = response.json()

    extra_data = data.get("extra", {})

    for key, value in extra_data.items():
        result[key] = value

    keys_to_extract = [
        "name",
        "hq",
        "search_id",
        "company_size",
        "industry",
        "founding_year",
        "specialities",
        "company_type",
        "countries",
        "description",
    ]

    for key in keys_to_extract:
        result[key] = data.get(key, None)

        if key == "countries":
            locations = data.get("locations", [])
            result[key] = list({item["country"] for item in locations if "country" in item})

    if result["search_id"]:
        url = "https://nubela.co/proxycurl/api/v2/linkedin/company/job/count"
        params = {
            "search_id": result["search_id"]
        }

        response = requests.get(url, headers=headers, params=params)

        job_data = response.json()
        result["jobs_count"] = job_data.get("count")

        url2 = "https://nubela.co/proxycurl/api/v2/linkedin/company/job"

        response = requests.get(url2, headers=headers, params=params)

        job_list_data = response.json()
        result["jobs_list"] = job_list_data.get("job")

    else:
        result["jobs_count"] = None
        result["jobs_list"] = None

    return result