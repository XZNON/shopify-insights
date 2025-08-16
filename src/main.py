from fastapi import FastAPI,HTTPException,BackgroundTasks
from .models import ScrapeRequest,BrandData,Product,ContanctDetails,CompetitorAnalysis
from .competitorAnalysis import find_competitors
from pydantic import ValidationError
from .scraper.shopify_scraper import scrape_all_insights,isShopify
from .db import saveBrandData
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"message":"This is the homepage for shopify insights"}

@app.post("/get-insigts", response_model = BrandData,response_model_exclude_none=True)
def scrape_store(request : ScrapeRequest,background_tasks : BackgroundTasks):
    try:
        insigts = scrape_all_insights(str(request.websiteUrl))

        response = BrandData.from_scraper_data(insigts)

        #adding to the database
        background_tasks.add_task(saveBrandData,response,str(request.websiteUrl))


        return response
    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=404,
            detail=f"Website not found or could not reach it"
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Data validation error. The scraped data structure is unexpected. Error: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=407,
            detail=f"Error occured while fetching data from the website : {e}"
        )


@app.post("/competitorAnalysis",response_model=CompetitorAnalysis,response_model_exclude_none=True)
def competitors(request : ScrapeRequest,background_tasks : BackgroundTasks):
    main_brand_url = str(request.website_url)
    
    try:
        print(f"Scraping main brand: {main_brand_url}")
        main_insights_dict = scrape_all_insights(main_brand_url)
        main_brand_data = BrandData.from_scraper_data(main_insights_dict)

        background_tasks.add_task(saveBrandData, main_brand_data, main_brand_url)

        competitor_urls = find_competitors(main_brand_url, num_results=3)
        
        competitor_insights_list = []
        for url in competitor_urls:
            if isShopify(url):  #now we can check if its a shopify store or not

                try:
                    print(f"Scraping competitor: {url}")
                    insights = scrape_all_insights(url)
                    competitor_data = BrandData.from_scraper_data(insights)
                    competitor_insights_list.append(competitor_data)

                    background_tasks.add_task(saveBrandData, competitor_data, url)

                except Exception as e:
                    print(f"Failed to scrape competitor {url}. Reason: {e}")

                else:
                    print(f"Skipping a non shopify competitor")

        response = CompetitorAnalysis(
            brand_data=main_brand_data,
            competitors=competitor_insights_list
        )
        
        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during the process for {main_brand_url}: {e}"
        )
