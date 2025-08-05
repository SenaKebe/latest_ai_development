# src/crew_blog_backend/crew.py

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class BlogContentCrew():
    """Social Media Blog Content Generation Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def trend_hunter(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_hunter'],  # from agents.yaml
            tools=[SerperDevTool()],  # you can replace with Gemini search if needed
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            verbose=True
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],
            verbose=True
        )

    @agent
    def summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer'],
            verbose=True
        )

    @task
    def trend_discovery_task(self) -> Task:
        return Task(
            config=self.tasks_config['trend_discovery_task']
        )

    @task
    def content_writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_writing_task']
        )

    @task
    def editing_task(self) -> Task:
        return Task(
            config=self.tasks_config['editing_task']
        )

    @task
    def summarizing_task(self) -> Task:
        return Task(
            config=self.tasks_config['summarizing_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates and runs the blog content generation crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
