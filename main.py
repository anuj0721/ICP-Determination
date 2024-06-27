import datetime
from typing import Optional
from enum import Enum
from fastapi import FastAPI, Request, Body, HTTPException
import requests

from decouple import config
import utils
app = FastAPI()
import crunch_main


@app.post("/fetch_company_data")
def fetch_company_data(company_url: str, status: str = "", closing_date: str = ""):
    """Fetches company data used for ICP generation."""
    
    company_offerings = utils.fetch_company_offerings(company_url)
    proxycurl_data = utils.fetchCompanyDetailsFromProxycurl(company_url)

    response = {
        "company_offerings": company_offerings
    }
    
    response.update(proxycurl_data)

    if status == "" and closing_date == "":
        from datetime import date  # Import date object to get current date

        today = date.today().strftime("%d/%m/%Y")  # Format current date (dd/mm/yyyy)
        closing_date = today
    
    if "crunchbase_profile_url" in proxycurl_data and "name" in proxycurl_data:
        if proxycurl_data["crunchbase_profile_url"] and proxycurl_data["name"]:
            crunchbase_data = crunch_main.get_growth_insights_and_news(proxycurl_data["crunchbase_profile_url"], proxycurl_data["name"], status, closing_date)
            # print("***************************************************** CRUNCHBASE DATA FOR", proxycurl_data["name"])
            # print(crunchbase_data)
            response.update(crunchbase_data)
    
    
    return {"data": response}