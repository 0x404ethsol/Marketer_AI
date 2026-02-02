/**
 * Skill Executor - Bridges Skills.sh content with the agent engine
 *
 * This module loads marketing skills and executes them with LLM assistance.
 */

import Anthropic from "@anthropic-ai/sdk";
import * as fs from "fs/promises";
import * as path from "path";

export interface SkillDefinition {
  name: string;
  slug: string;
  description: string;
  category: string;
  version: string;
  content: string;
  references: string[];
  localPath: string;
}

export interface SkillExecutionResult {
  skillUsed: string;
  output: string;
  metadata: {
    tokensUsed: number;
    model: string;
    executionTime: number;
  };
}

export class SkillExecutor {
  private skills: Map<string, SkillDefinition> = new Map();
  private skillsPath: string;
  private anthropic: Anthropic;

  constructor(
    skillsPath: string = "C:\\Users\\18504\\Desktop\\Skills.sh",
    apiKey?: string
  ) {
    this.skillsPath = skillsPath;
    this.anthropic = new Anthropic({
      apiKey: apiKey || process.env.ANTHROPIC_API_KEY,
    });
  }

  /**
   * Load a skill from the Skills.sh directory
   */
  async loadSkill(skillName: string): Promise<SkillDefinition> {
    // Check cache first
    if (this.skills.has(skillName)) {
      return this.skills.get(skillName)!;
    }

    const skillPath = path.join(this.skillsPath, skillName);
    const skillFile = path.join(skillPath, "SKILL.md");

    try {
      const content = await fs.readFile(skillFile, "utf-8");

      // Parse skill metadata from YAML frontmatter if present
      const metadata = this.parseSkillMetadata(content);

      const skill: SkillDefinition = {
        name: metadata.name || skillName,
        slug: metadata.slug || skillName.toLowerCase().replace(/\s+/g, "-"),
        description: metadata.description || "",
        category: metadata.category || "general",
        version: metadata.version || "1.0.0",
        content: content,
        references: metadata.references || [],
        localPath: skillPath,
      };

      this.skills.set(skillName, skill);
      return skill;
    } catch (error) {
      throw new Error(`Failed to load skill "${skillName}": ${error}`);
    }
  }

  /**
   * Preload multiple skills into memory
   */
  async preloadSkills(skillNames: string[]): Promise<void> {
    await Promise.all(skillNames.map((name) => this.loadSkill(name)));
  }

  /**
   * Execute a skill with the given context and user input
   */
  async execute(
    skillName: string,
    context: Record<string, any>,
    userInput: string
  ): Promise<SkillExecutionResult> {
    const startTime = Date.now();

    // Load skill if not already loaded
    const skill = await this.loadSkill(skillName);

    // Build system prompt with skill knowledge
    const systemPrompt = this.buildSystemPrompt(skill, context);

    // Execute with Claude
    const response = await this.anthropic.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 8192,
      system: systemPrompt,
      messages: [
        {
          role: "user",
          content: this.formatUserPrompt(userInput, context),
        },
      ],
    });

    const executionTime = Date.now() - startTime;
    const outputText =
      response.content[0].type === "text" ? response.content[0].text : "";

    return {
      skillUsed: skillName,
      output: outputText,
      metadata: {
        tokensUsed: response.usage.input_tokens + response.usage.output_tokens,
        model: response.model,
        executionTime,
      },
    };
  }

  /**
   * Build system prompt incorporating skill knowledge
   */
  private buildSystemPrompt(
    skill: SkillDefinition,
    context: Record<string, any>
  ): string {
    return `You are an expert marketing AI assistant with deep knowledge of:

# ${skill.name}
${skill.description}

## Core Knowledge
${skill.content}

## Your Role
Apply this specialized knowledge to help the user achieve their marketing goals.
Always provide actionable, specific recommendations based on the frameworks and best practices in this skill.

## Context
${JSON.stringify(context, null, 2)}

## Guidelines
1. Be specific and actionable
2. Reference frameworks from the skill when applicable
3. Provide examples when helpful
4. Consider the user's context (platform, audience, goals)
5. Think step-by-step for complex requests`;
  }

  /**
   * Format user input with context
   */
  private formatUserPrompt(
    userInput: string,
    context: Record<string, any>
  ): string {
    let prompt = userInput;

    // Add relevant context if available
    if (context.brand) {
      prompt += `\n\nBrand Context: ${context.brand}`;
    }
    if (context.platform) {
      prompt += `\nTarget Platform: ${context.platform}`;
    }
    if (context.audience) {
      prompt += `\nTarget Audience: ${context.audience}`;
    }

    return prompt;
  }

  /**
   * Parse skill metadata from YAML frontmatter
   */
  private parseSkillMetadata(content: string): Record<string, any> {
    const metadata: Record<string, any> = {};

    // Check for YAML frontmatter
    const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (frontmatterMatch) {
      const yaml = frontmatterMatch[1];
      const lines = yaml.split("\n");

      for (const line of lines) {
        const [key, ...valueParts] = line.split(":");
        if (key && valueParts.length > 0) {
          const value = valueParts.join(":").trim();
          metadata[key.trim()] = value.replace(/^["']|["']$/g, "");
        }
      }
    }

    return metadata;
  }

  /**
   * List all available skills
   */
  async listAvailableSkills(): Promise<string[]> {
    try {
      const entries = await fs.readdir(this.skillsPath, { withFileTypes: true });
      return entries
        .filter((entry) => entry.isDirectory())
        .map((entry) => entry.name);
    } catch (error) {
      console.error("Failed to list skills:", error);
      return [];
    }
  }

  /**
   * Get loaded skills
   */
  getLoadedSkills(): string[] {
    return Array.from(this.skills.keys());
  }

  /**
   * Clear skill cache
   */
  clearCache(): void {
    this.skills.clear();
  }
}

// Export singleton instance
export const skillExecutor = new SkillExecutor();

// Marketing-specific skill presets
export const MARKETING_SKILLS = {
  strategy: ["marketing-strategy-pmm", "marketing-psychology", "marketing-ideas"],
  content: ["ad-copy-writer", "content-creator", "tiktok-creator"],
  video: ["kinetic-video-creator", "video-producer"],
  sales: ["lead-qualifier", "sales-pipeline-manager", "affiliate-marketing-manager"],
  campaigns: ["executing-marketing-campaigns"],
};

/**
 * Create a skill executor with marketing skills preloaded
 */
export async function createMarketingExecutor(): Promise<SkillExecutor> {
  const executor = new SkillExecutor();

  // Preload all marketing skills
  const allSkills = Object.values(MARKETING_SKILLS).flat();
  await executor.preloadSkills(allSkills);

  return executor;
}
