from pydantic import BaseModel,HttpUrl,Field,field_validator,ConfigDict
from typing import List,Dict,Optional,Any


class ScrapeRequest(BaseModel):
    website_url : HttpUrl = Field(...,alias='websiteUrl')

class Product(BaseModel):
    id : Optional[int] = None
    title  : Optional[str] = None
    # vendor : Optional[str] = None
    # product_type : Optional[str] = None
    # tags : Optional[List[str]] = None

    # class Config:
    #     extra = 'allow'
    
class ContanctDetails(BaseModel):
    emails : Optional[List[str]] = None
    phoneNumbers : Optional[List[str]] = None

class PageContent(BaseModel):
    url : Optional[HttpUrl] = None
    content : Optional[str] = None



class BrandData(BaseModel):
    product_catalog : List[Product] = []
    social_handles : Dict[str,Optional[HttpUrl]] = {}
    contact_details : Optional[ContanctDetails] = None

    privacy_policy: Optional[PageContent] = None
    refund_policy: Optional[PageContent] = None
    about_us: Optional[PageContent] = None
    contact_us: Optional[PageContent] = None
    faqs: Optional[PageContent] = None
    blogs: Optional[PageContent] = None
    track_order: Optional[PageContent] = None

    #if any field is empty we return None 
    #check before passing in to the model
    @field_validator('*',mode='before')
    @classmethod
    def emptyStr(cls,v):
        if isinstance(v,str) and not v:
            return None
        return v

    @classmethod
    def from_scraper_data(cls, data: Dict[str, Any]) -> 'BrandData':
        transformed_data = data.copy() # Start with the base data
        links = data.get('important_links', {})

        for key in ['privacy_policy', 'refund_policy', 'about_us', 'contact_us', 'faqs', 'blogs', 'track_order']:
            content_key = f'{key}_content'
            page_data = {
                'url': links.get(key),
                'content': data.get(content_key)
            }
            if page_data['url'] or page_data['content']:
                transformed_data[key] = PageContent(**page_data)

        return cls.model_validate(transformed_data)


class CompetitorAnalysis(BaseModel):
    brand_data : BrandData
    competitors : List[BrandData] = []

    model_config = ConfigDict(populate_by_name=True)

class CompetitorComparison(BaseModel):
    product_comparison: str = Field(description="A comparison of the product catalogs, variety, and unique selling propositions.")
    pricing_strategy: str = Field(description="An analysis of the likely pricing strategies (e.g., budget, premium, competitive).")
    brand_voice_and_target_audience: str = Field(description="A comparison of the brand messaging, tone, and likely target audience.")
    overall_summary: str = Field(description="A concluding summary of the competitive landscape.")

class LLMResponse(BaseModel):
    brand_data : BrandData
    competitors : List[BrandData] = []
    comparison_summary : CompetitorComparison


