import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from .models import BrandData,CompetitorComparison
from pydantic import BaseModel,Field
from typing import List, Dict, Any
import typing
from dotenv import load_dotenv

#place your LLM key in the .env folder
load_dotenv()

def get_llm_competitor_analysis(main_brand: BrandData, competitors: List[BrandData]) -> Dict[str, Any]:

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

    parser = JsonOutputParser(pydantic_object=CompetitorComparison)


    def brand_to_text(brand: BrandData):
        about_text = brand.about_us.content if brand.about_us and brand.about_us.content else "No 'About Us' page found."
        product_titles = ", ".join([p.title for p in brand.product_catalog[:5]]) # First 5 products
        return f"Brand: {brand.about_us.url}\nAbout Us: {about_text[:1000]}\nKey Products: {product_titles}\n"

    main_brand_text = brand_to_text(main_brand)
    competitors_text = "\n".join([brand_to_text(c) for c in competitors])

    prompt_template = """
    You are a professional e-commerce business analyst.
    Based on the provided text from a main brand's website and its competitors,
    provide a detailed comparative analysis. Focus on the following aspects:
    - Product Comparison: What are the differences in product offerings and variety?
    - Pricing Strategy: What can you infer about their pricing (budget, mid-range, premium)?
    - Brand Voice & Target Audience: How do they communicate and who are they trying to reach?

    Here is the data:

    MAIN BRAND:
    {main_brand_data}

    COMPETITORS:
    {competitor_data}
    Please provide your analysis in a structured JSON format.
    {format_instructions}
    """
    prompt = ChatPromptTemplate.from_template(
        template=prompt_template,
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser
    
    try:
        print("Invoking LLM for competitor analysis...")
        response = chain.invoke({
            "main_brand_data": main_brand_text,
            "competitor_data": competitors_text,
        })
        print("LLM analysis successful.")
        return response
    except Exception as e:
        print(f"An error occurred during LLM analysis: {e}")
        return {"error": "Failed to generate LLM comparison."}

