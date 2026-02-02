"""
Video Crew - AI video production crew generating Remotion code.

Skills loaded:
- remotion (core animation patterns)
- kinetic-video-creator (text animations)
- marketing-psychology (emotional timing)
"""

from crewai import Agent, Crew, Task, Process
from typing import Dict, List, Any


class VideoCrew:
    """
    AI video production crew that generates Remotion React code.

    This crew creates:
    - Video structure with retention-optimized timing
    - Remotion composition code
    - TikTok-style caption animations
    """

    # Platform specifications
    PLATFORM_SPECS = {
        "tiktok": {"width": 1080, "height": 1920, "fps": 30, "max_duration": 180},
        "instagram_reels": {"width": 1080, "height": 1920, "fps": 30, "max_duration": 90},
        "youtube_shorts": {"width": 1080, "height": 1920, "fps": 30, "max_duration": 60},
        "youtube": {"width": 1920, "height": 1080, "fps": 30, "max_duration": None},
        "instagram_feed": {"width": 1080, "height": 1080, "fps": 30, "max_duration": 60}
    }

    def __init__(self, campaign_strategy: Dict[str, Any]):
        self.strategy = campaign_strategy
        self.agents = self._create_agents()

    def _create_agents(self) -> List[Agent]:
        """Create the video production agents."""

        video_director = Agent(
            role="Video Strategy Director",
            goal="Design video structure that maximizes retention and conversion",
            backstory="""You are a video strategist who understands attention science.

            CRITICAL RETENTION KNOWLEDGE:
            - 65%+ retention at 3 seconds = 4-7x more impressions
            - 85% watch videos muted - text/captions are essential
            - Person speaking to camera converts 33% better
            - Videos losing >35% at 3 seconds get algorithmically buried
            - Average scroll decision: 0.5 seconds

            VIDEO STRUCTURE PRINCIPLES:
            - Hook (0-3s): Pattern interrupt, curiosity gap
            - Problem (3-7s): Agitate the pain point
            - Solution (7-12s): Present the transformation
            - Proof (12-18s): Social proof, results
            - CTA (last 3s): Clear action with urgency

            EMOTIONAL ARC:
            - Start with tension/curiosity
            - Build to emotional peak (usually at 60-70% mark)
            - End with resolution + action

            PACING:
            - Scene changes every 2-3 seconds
            - Text on screen synced with speech
            - Motion on every frame""",
            verbose=True,
            allow_delegation=False
        )

        remotion_coder = Agent(
            role="Remotion Code Generator",
            goal="Generate production-ready Remotion React code",
            backstory="""You are an expert in Remotion video generation framework.

            ALWAYS USE:
            - useCurrentFrame() for ALL motion
            - interpolate() for value mapping
            - spring() for natural movement
            - <Sequence> for timing sections
            - staticFile() for assets in public/

            NEVER USE:
            - CSS animations or transitions
            - requestAnimationFrame
            - setTimeout/setInterval for timing
            - Direct Three.js useFrame()

            CODE PATTERNS:

            ```typescript
            // Frame-based animation
            const frame = useCurrentFrame();
            const opacity = interpolate(frame, [0, 30], [0, 1], {
                extrapolateRight: 'clamp'
            });

            // Spring animation
            const scale = spring({
                frame,
                fps: 30,
                config: { damping: 12, stiffness: 200 }
            });

            // Sequence timing
            <Sequence from={0} durationInFrames={90} name="Hook">
                <HookScene />
            </Sequence>
            ```

            COMPOSITION STRUCTURE:
            - Export composition with proper dimensions
            - Include durationInFrames, fps, width, height
            - Use TypeScript for type safety
            - Modular components for each scene""",
            verbose=True,
            allow_delegation=False
        )

        caption_animator = Agent(
            role="Caption & Typography Animator",
            goal="Create TikTok-style captions with word-by-word highlighting",
            backstory="""You specialize in kinetic typography and caption animations.

            CAPTION REQUIREMENTS:
            - Word-by-word highlighting (active word pops)
            - Sync perfectly to audio timing via wordTimings array
            - Mobile-readable fonts (minimum 48px)
            - High contrast (white on dark or vice versa)
            - Drop shadows for legibility

            ANIMATION PATTERNS:
            - Active word: scale 1.1, bold, accent color
            - Past words: normal weight, white
            - Future words: lower opacity (0.5)

            TIMING STRUCTURE:
            ```typescript
            interface WordTiming {
                word: string;
                start: number;  // seconds
                end: number;    // seconds
            }

            // Calculate active word from frame
            const currentSecond = frame / fps;
            const activeIndex = wordTimings.findIndex(
                w => currentSecond >= w.start && currentSecond < w.end
            );
            ```

            ENTRANCE ANIMATIONS:
            - Words fade in 0.1s before they're spoken
            - Subtle bounce on active word
            - Smooth color transitions""",
            verbose=True,
            allow_delegation=False
        )

        return [video_director, remotion_coder, caption_animator]

    def generate_video_structure(self, script: str, platform: str) -> str:
        """Design the video structure with timing."""

        specs = self.PLATFORM_SPECS.get(platform, self.PLATFORM_SPECS["tiktok"])

        task = Task(
            description=f"""Design video structure for this script:

            SCRIPT:
            {script}

            PLATFORM: {platform}
            SPECS: {specs['width']}x{specs['height']} at {specs['fps']}fps
            MAX DURATION: {specs['max_duration']} seconds

            CREATE:
            1. Scene breakdown with timing (in frames at {specs['fps']}fps)
            2. Hook moment design (0-3 seconds)
            3. Emotional arc with peak moments
            4. CTA timing and placement
            5. Caption/text overlay strategy
            6. Scene transition points

            OUTPUT:
            - Detailed timing document
            - Frame numbers for each scene
            - Text overlay content and timing
            """,
            expected_output="Complete video structure document with frame-accurate timing",
            agent=self.agents[0]  # Video Director
        )

        crew = Crew(
            agents=[self.agents[0]],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff()

    def generate_remotion_code(self, structure: str, script: str, platform: str) -> str:
        """Generate Remotion composition code."""

        specs = self.PLATFORM_SPECS.get(platform, self.PLATFORM_SPECS["tiktok"])

        task = Task(
            description=f"""Generate complete Remotion composition code.

            VIDEO STRUCTURE:
            {structure}

            SCRIPT:
            {script}

            SPECS:
            - Width: {specs['width']}
            - Height: {specs['height']}
            - FPS: {specs['fps']}

            REQUIREMENTS:
            - TypeScript React component
            - Use useCurrentFrame() and interpolate() for ALL animations
            - Use spring() for natural movement
            - Use <Sequence> for timing sections
            - Export as proper Remotion composition
            - Include durationInFrames, fps, width, height

            MUST INCLUDE:
            - Hook scene (0-3 seconds)
            - Main content scenes
            - CTA scene (last 3 seconds)
            - Proper imports from 'remotion'

            OUTPUT:
            Complete TypeScript code that can be directly used in a Remotion project.
            """,
            expected_output="Production-ready Remotion TypeScript composition",
            agent=self.agents[1]  # Remotion Coder
        )

        crew = Crew(
            agents=[self.agents[1]],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff()

    def generate_captions(self, script: str, word_timings: List[Dict]) -> str:
        """Generate TikTok-style caption component."""

        task = Task(
            description=f"""Create TikTok-style caption animation component.

            SCRIPT:
            {script}

            WORD TIMINGS:
            {word_timings}

            CREATE:
            - Word-by-word highlighting component
            - Smooth entrance animations
            - Proper timing sync points
            - Mobile-readable font sizes (48px minimum)

            REQUIREMENTS:
            - Use useCurrentFrame() for timing
            - Calculate activeWordIndex from frame
            - Apply spring animations to active word
            - Ensure high contrast and legibility

            OUTPUT:
            Complete TikTokCaptions React component with TypeScript.
            """,
            expected_output="TikTok-style caption component code",
            agent=self.agents[2]  # Caption Animator
        )

        crew = Crew(
            agents=[self.agents[2]],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        return crew.kickoff()

    def run_full_video_pipeline(self, script: str, platform: str = "tiktok") -> Dict[str, Any]:
        """Run the complete video generation pipeline."""

        specs = self.PLATFORM_SPECS.get(platform, self.PLATFORM_SPECS["tiktok"])

        # Task 1: Design structure
        structure_task = Task(
            description=f"""Design video structure for:

            SCRIPT: {script}
            PLATFORM: {platform}
            SPECS: {specs}

            Create scene breakdown with frame-accurate timing.""",
            expected_output="Complete video structure with timing",
            agent=self.agents[0]
        )

        # Task 2: Generate Remotion code
        code_task = Task(
            description="""Generate Remotion composition code based on the structure.

            Use the video structure to create:
            - Main composition component
            - Scene components
            - Animation utilities

            Follow all Remotion best practices.""",
            expected_output="Complete Remotion TypeScript code",
            agent=self.agents[1],
            context=[structure_task]
        )

        # Task 3: Add captions
        caption_task = Task(
            description="""Add TikTok-style captions to the video.

            Create caption component that:
            - Highlights words as they're spoken
            - Uses spring animations
            - Is mobile-readable

            Integrate with the main composition.""",
            expected_output="Caption component integrated with video",
            agent=self.agents[2],
            context=[code_task]
        )

        crew = Crew(
            agents=self.agents,
            tasks=[structure_task, code_task, caption_task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()

        return {
            "structure": structure_task.output if hasattr(structure_task, 'output') else None,
            "remotion_code": code_task.output if hasattr(code_task, 'output') else None,
            "final_code": result,
            "platform": platform,
            "specs": specs
        }


# Example usage
if __name__ == "__main__":
    strategy = {
        "brand": "AI Marketing Platform",
        "goal": "Drive signups",
        "tone": "Bold, exciting"
    }

    script = """
    Stop scrolling. This changes everything.
    You're spending 10 hours a week on marketing.
    What if AI did it in 10 minutes?
    MARKETER_AI creates scroll-stopping content automatically.
    Join 10,000 marketers who switched.
    Link in bio. Your competitors already clicked.
    """

    crew = VideoCrew(strategy)
    result = crew.run_full_video_pipeline(script, "tiktok")
    print(result)
