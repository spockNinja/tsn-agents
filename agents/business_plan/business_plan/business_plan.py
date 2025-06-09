import os
from typing import Any
from pydantic import Field

from llama_index.core.llms.llm import LLM
from llama_index.core.workflow import (
    Event,
    Context,
    Workflow,
    StartEvent,
    StopEvent,
    step,
)
from llama_index.core.prompts import RichPromptTemplate
from llama_index.llms.openai import OpenAI

from bs4 import BeautifulSoup
from selenium import webdriver


class LogEvent(Event):
    msg: str
    delta: bool = False


class BusinessPlanInput(StartEvent):
    project_name: str = Field(
        ..., description='The name of the project we are creating a business plan for'
    )
    project_website: str = Field(
        ..., description='The website of the project we are creating a business plan for'
    )
    additional_context: str = Field(
        ..., description='Any additional info the user wants to give the AI'
    )


class BusinessPlanOutput(StopEvent):
    business_plan: str = Field(
        default='',
        description='The generated Business Plan'
    )


BUSINESS_PLAN_PROMPT_TEMPLATE = RichPromptTemplate(
"""
{% chat role="system" %}
You are an assistant, helping Regenerative project visionaries create a business plan.
{% endchat %}

{% chat role="user" %}
Your tasks are:
1) Inspect the provided project information
2) Generate a business plan

The Project Name:
{{ project_name }}

Plaintext content scraped from the website:
{{ website_content }}

Additional context provided by the user:
{{ additional_context }}
{% endchat %}
"""
)


def scrape_site(site_url: str, ctx: Context) -> str:

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        service = webdriver.ChromeService()
        driver = webdriver.Chrome(options=options, service=service)
        driver.get(site_url)
        driver.implicitly_wait(2)
        page_source = driver.page_source
        driver.quit()
        soup = BeautifulSoup(page_source, 'html.parser')
        site_text = soup.get_text()
    except Exception as e:
        site_text = "Unable to scrape site"
        ctx.write_event_to_stream(
            LogEvent(msg=f'Unable to scrape {site_url}')
        )
        ctx.write_event_to_stream(
            LogEvent(msg=str(e))
        )
    
    return site_text


class BusinessPlan(Workflow):
    def __init__(
        self,
        llm: LLM | None = None,
        verbose: bool = False,
        **workflow_kwargs: Any,
    ) -> None:
        super().__init__(verbose=verbose, **workflow_kwargs)

        self.llm = OpenAI(
            model="gpt-4.5-preview",
            api_key=os.getenv("OPENROUTER_API_KEY", "Fake"),
            api_base=os.getenv("OPENROUTER_API_URL")
        )

    @step
    async def generate_business_plan(
        self, ctx: Context, ev: BusinessPlanInput
    ) -> BusinessPlanOutput:
        if self._verbose:
            ctx.write_event_to_stream(
                LogEvent(msg=f"Generating Business Plan for {ev.project_name}"))
        
        website_content = scrape_site(ev.project_website, ctx)

        plan: BusinessPlanOutput = await self.llm.astructured_predict(
            BusinessPlanOutput,
            BUSINESS_PLAN_PROMPT_TEMPLATE,
            project_name=ev.project_name,
            website_content=website_content,
            additional_context=ev.additional_context,
        )

        return plan