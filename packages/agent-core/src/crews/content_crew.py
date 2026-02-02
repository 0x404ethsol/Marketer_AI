"""
Content Crew - Pre-equipped content creation crew with marketing psychology mastery.

Skills loaded:
- marketing-psychology (70+ mental models)
- ad-copy-writer (platform-specific copy)
- hook-development (viral hooks)
"""

from crewai import Agent, Crew, Task, Process
from typing import Dict, List, Any
import os


class ContentCrew:
    """
    Pre-equipped content creation crew with marketing psychology mastery.

    This crew generates scroll-stopping content using:
    - Pattern interrupts and curiosity gaps for hooks
    - 70+ mental models for persuasive copy
    - Platform-specific optimization
    """

    def __init__(self, campaign_brief: Dict[str, Any]):
        self.brief = campaign_brief
        self.agents = self._create_agents()

    def _create_agents(self) -> List[Agent]:
        """Create the content crew agents with pre-loaded expertise."""

        hook_specialist = Agent(
            role="Hook Specialist",
            goal="Create scroll-stopping hooks that capture attention in 0.5 seconds",
            backstory="""You are the world's foremost expert on psychological hooks.

            CRITICAL KNOWLEDGE:
            - 73% of video ads fail in the first 3 seconds because they look like ads
            - Average scroll decision: 0.5 seconds
            - Videos losing >35% at 3 seconds get algorithmically buried
            - 65%+ retention at 3 seconds = 4-7x more impressions

            HOOK PSYCHOLOGY (Every hook needs 1-2):
            1. Pattern Interrupt - Break the scroll trance
            2. Curiosity Gap - Incomplete info creates tension
            3. Value Promise - Signal reward for watching
            4. Loss Aversion - Losses hurt 2x more than gains
            5. Social Proof - Tribal validation
            6. Scarcity/Urgency - Limited = valuable

            The uncertainty of reward triggers more dopamine than the reward itself.
            You create hooks that demand attention through psychological precision.""",
            verbose=True,
            allow_delegation=False
        )

        psychology_copywriter = Agent(
            role="Psychology-Driven Copywriter",
            goal="Write copy that converts using 70+ behavioral science principles",
            backstory="""You are an expert in applying mental models to marketing.

            CORE MENTAL MODELS:
            - Jobs to Be Done: People hire products for progress
            - Loss Aversion: Losses hurt 2x more than equivalent gains
            - Social Proof: We look to others for behavioral guidance
            - Scarcity: Limited availability increases perceived value
            - Anchoring: First number sets the reference point
            - Reciprocity: Give value before asking
            - Authority: Expert endorsement builds trust
            - Commitment/Consistency: Small yeses lead to big yeses

            BEHAVIORAL ECONOMICS:
            - Prospect Theory: Frame gains vs losses carefully
            - Endowment Effect: Ownership increases value
            - Sunk Cost: Past investment influences future decisions
            - Present Bias: Immediate rewards > future rewards

            PERSUASION PRINCIPLES:
            - Contrast Principle: Show the alternative first
            - Peak-End Rule: People remember peaks and endings
            - Mere Exposure: Familiarity breeds preference

            You write copy that speaks to deep human motivations, not surface desires.
            People don't buy products. They buy better versions of themselves.""",
            verbose=True,
            allow_delegation=False
        )

        platform_expert = Agent(
            role="Platform Optimization Expert",
            goal="Adapt content perfectly for each platform's algorithm and audience",
            backstory="""You know every platform intimately:

            TIKTOK (Gen Z: 13-28):
            - Style: Raw, chaotic, meme-literate, ironic
            - Aesthetic: Y2K, maximalist
            - Algorithm: Watch time + completion rate + shares
            - Hooks: First 1 second is everything
            - 85% watch muted - captions essential

            INSTAGRAM REELS (Millennials: 29-44):
            - Style: Aesthetic, aspirational, polished-casual
            - Aesthetic: Clean, warm tones
            - Algorithm: Saves + shares > likes
            - Hooks: First 3 seconds critical

            YOUTUBE SHORTS (All ages):
            - Style: Value-packed, educational lean
            - Algorithm: Click-through + watch time
            - Hooks: Thumbnail + first 2 seconds

            LINKEDIN (Gen X: 45-60, B2B):
            - Style: Professional, thought-leadership
            - Aesthetic: Trustworthy, authoritative
            - Algorithm: Comments + dwell time

            You optimize for each platform's unique requirements and audience expectations.""",
            verbose=True,
            allow_delegation=False
        )

        return [hook_specialist, psychology_copywriter, platform_expert]

    def generate_hooks(self, product: str, audience: str, platform: str, emotional_trigger: str) -> str:
        """Generate 5 hook variations with psychological analysis."""

        task = Task(
            description=f"""Create 5 scroll-stopping hook variations for:

            PRODUCT: {product}
            TARGET AUDIENCE: {audience}
            PLATFORM: {platform}
            PRIMARY EMOTION: {emotional_trigger}

            REQUIREMENTS:
            - Each hook must work in under 3 seconds
            - Apply at least 1-2 psychological triggers per hook
            - Consider platform-specific attention patterns
            - Include pattern interrupts for at least 2 hooks
            - Include curiosity gaps for at least 2 hooks

            OUTPUT FORMAT:
            For each hook provide:
            1. The hook text (under 10 words)
            2. Psychology triggers used
            3. Why it works for this platform
            4. Predicted attention capture rate (1-10)
            """,
            expected_output="5 unique hooks with complete psychological analysis",
            agent=self.agents[0]  # Hook Specialist
        )

        crew = Crew(
            agents=[self.agents[0]],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff()

    def generate_ad_copy(self, hook: str, product: str, platform: str, mental_models: List[str] = None) -> str:
        """Generate full ad copy using specified mental models."""

        if mental_models is None:
            mental_models = ["Loss Aversion", "Social Proof"]

        task = Task(
            description=f"""Develop complete ad copy for:

            HOOK: {hook}
            PRODUCT: {product}
            PLATFORM: {platform}
            MENTAL MODELS TO APPLY: {', '.join(mental_models)}

            CREATE:
            1. Primary text (125-250 characters for FB/IG)
            2. Headline (benefit-driven, under 40 chars)
            3. Description (supporting value prop)
            4. CTA (action-oriented, creates urgency)

            REQUIREMENTS:
            - Apply each specified mental model deliberately
            - Explain how each model is being used
            - Match platform tone and style
            - Focus on transformation, not features
            """,
            expected_output="Complete ad copy package with psychological rationale",
            agent=self.agents[1]  # Psychology Copywriter
        )

        crew = Crew(
            agents=[self.agents[1]],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff()

    def optimize_for_platform(self, copy: str, platform: str) -> str:
        """Optimize copy for specific platform requirements."""

        task = Task(
            description=f"""Optimize this copy for {platform}:

            ORIGINAL COPY:
            {copy}

            OPTIMIZE FOR:
            - Character limits
            - Platform-native language and tone
            - Emoji strategy (if appropriate)
            - Hashtag strategy
            - Algorithm engagement signals

            ENSURE:
            - Maintains psychological triggers
            - Feels native to the platform
            - Maximizes algorithmic reach
            """,
            expected_output="Platform-optimized copy with placement specifications",
            agent=self.agents[2]  # Platform Expert
        )

        crew = Crew(
            agents=[self.agents[2]],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff()

    def run_full_content_pipeline(self) -> Dict[str, Any]:
        """Run the complete content creation pipeline."""

        # Task 1: Generate hooks
        hook_task = Task(
            description=f"""Create 5 hook variations for:

            PRODUCT: {self.brief.get('product', 'Unknown product')}
            AUDIENCE: {self.brief.get('audience', 'General audience')}
            PLATFORM: {self.brief.get('platform', 'TikTok')}
            EMOTION: {self.brief.get('emotional_trigger', 'Curiosity')}

            Apply pattern interrupts and curiosity gaps.""",
            expected_output="5 hooks with psychological analysis",
            agent=self.agents[0]
        )

        # Task 2: Develop copy from best hook
        copy_task = Task(
            description="""Take the best performing hook from the previous analysis
            and develop complete ad copy.

            Apply these mental models:
            - Loss Aversion
            - Social Proof
            - Scarcity

            Include primary text, headline, description, and CTA.""",
            expected_output="Complete ad copy with mental model application",
            agent=self.agents[1],
            context=[hook_task]
        )

        # Task 3: Platform optimization
        optimize_task = Task(
            description=f"""Optimize the ad copy for {self.brief.get('platform', 'TikTok')}.

            Ensure:
            - Platform-native tone
            - Correct character limits
            - Algorithm optimization
            - Engagement signals""",
            expected_output="Final platform-optimized content package",
            agent=self.agents[2],
            context=[copy_task]
        )

        crew = Crew(
            agents=self.agents,
            tasks=[hook_task, copy_task, optimize_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()

        return {
            "hooks": hook_task.output if hasattr(hook_task, 'output') else None,
            "copy": copy_task.output if hasattr(copy_task, 'output') else None,
            "optimized": result,
            "platform": self.brief.get('platform'),
            "brief": self.brief
        }


# Example usage
if __name__ == "__main__":
    brief = {
        "product": "AI Marketing Platform",
        "audience": "Small business owners, 25-45, frustrated with marketing complexity",
        "platform": "TikTok",
        "emotional_trigger": "Relief from overwhelm"
    }

    crew = ContentCrew(brief)
    result = crew.run_full_content_pipeline()
    print(result)
