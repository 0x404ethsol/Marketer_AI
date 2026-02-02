/**
 * TikTok Ad Composition
 *
 * A scroll-stopping video ad template optimized for TikTok's algorithm.
 *
 * Structure:
 * - Hook (0-3s): Pattern interrupt to stop the scroll
 * - Problem (3-7s): Agitate the pain point
 * - Solution (7-12s): Present the transformation
 * - Proof (12-18s): Social proof, results
 * - CTA (last 3s): Clear action with urgency
 */

import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
  Audio,
  Img,
  staticFile,
  AbsoluteFill,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";

const { fontFamily } = loadFont();

// Types
interface WordTiming {
  word: string;
  start: number; // seconds
  end: number; // seconds
}

interface TikTokAdProps {
  hookText: string;
  script: string;
  wordTimings: WordTiming[];
  audioFile?: string;
  brandColors: {
    primary: string;
    secondary: string;
    accent: string;
  };
  ctaText: string;
}

// Platform specs
const TIKTOK_SPECS = {
  width: 1080,
  height: 1920,
  fps: 30,
  durationInFrames: 450, // 15 seconds
};

/**
 * Main TikTok Ad Composition
 */
export const TikTokAd: React.FC<TikTokAdProps> = ({
  hookText,
  script,
  wordTimings,
  audioFile,
  brandColors,
  ctaText,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  return (
    <AbsoluteFill
      style={{
        backgroundColor: brandColors.primary,
        fontFamily,
      }}
    >
      {/* Audio track (if provided) */}
      {audioFile && <Audio src={staticFile(audioFile)} />}

      {/* Hook Sequence (0-3 seconds = 0-90 frames) */}
      <Sequence from={0} durationInFrames={fps * 3} name="Hook">
        <HookScene hookText={hookText} brandColors={brandColors} />
      </Sequence>

      {/* Main Content with Captions (3-12 seconds) */}
      <Sequence from={fps * 3} durationInFrames={fps * 9} name="MainContent">
        <MainContentScene
          wordTimings={wordTimings}
          brandColors={brandColors}
          startTime={3}
        />
      </Sequence>

      {/* CTA Sequence (last 3 seconds) */}
      <Sequence from={fps * 12} name="CTA">
        <CTAScene ctaText={ctaText} brandColors={brandColors} />
      </Sequence>
    </AbsoluteFill>
  );
};

/**
 * Hook Scene - Pattern interrupt to stop the scroll
 */
const HookScene: React.FC<{
  hookText: string;
  brandColors: { primary: string; secondary: string; accent: string };
}> = ({ hookText, brandColors }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Fade in
  const opacity = interpolate(frame, [0, fps * 0.3], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Spring scale for punch
  const scale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 200 },
  });

  // Glitch effect for pattern interrupt (first 0.5 seconds)
  const glitchOffset = frame < fps * 0.5 ? Math.sin(frame * 20) * 5 : 0;

  // Text shadow pulse
  const shadowIntensity = interpolate(
    frame,
    [0, fps * 1, fps * 2, fps * 3],
    [0, 10, 5, 10],
    { extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Background pulse */}
      <div
        style={{
          position: "absolute",
          width: "100%",
          height: "100%",
          background: `radial-gradient(circle at center, ${brandColors.accent}22 0%, transparent 70%)`,
          opacity: interpolate(frame, [0, fps, fps * 2], [0, 0.5, 0.3]),
        }}
      />

      {/* Hook text */}
      <div
        style={{
          transform: `scale(${scale}) translateX(${glitchOffset}px)`,
          opacity,
          fontSize: 72,
          fontWeight: 900,
          color: brandColors.accent,
          textAlign: "center",
          padding: "0 60px",
          textShadow: `
            ${shadowIntensity}px ${shadowIntensity}px 0 rgba(0,0,0,0.3),
            -2px -2px 0 rgba(255,255,255,0.1)
          `,
          lineHeight: 1.2,
        }}
      >
        {hookText}
      </div>
    </AbsoluteFill>
  );
};

/**
 * Main Content Scene with TikTok-style captions
 */
const MainContentScene: React.FC<{
  wordTimings: WordTiming[];
  brandColors: { primary: string; secondary: string; accent: string };
  startTime: number;
}> = ({ wordTimings, brandColors, startTime }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Calculate current time in seconds (accounting for sequence offset)
  const currentSecond = frame / fps + startTime;

  // Find active word
  const activeWordIndex = wordTimings.findIndex(
    (w) => currentSecond >= w.start && currentSecond < w.end
  );

  return (
    <AbsoluteFill>
      {/* Caption container at bottom */}
      <div
        style={{
          position: "absolute",
          bottom: "20%",
          left: "8%",
          right: "8%",
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: 12,
        }}
      >
        {wordTimings.map((wordTiming, index) => {
          const isActive = index === activeWordIndex;
          const isPast = currentSecond >= wordTiming.end;
          const isFuture = currentSecond < wordTiming.start;

          // Calculate word opacity
          const wordOpacity = interpolate(
            currentSecond,
            [wordTiming.start - 0.15, wordTiming.start],
            [0.4, 1],
            { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
          );

          // Active word spring animation
          const wordScale = isActive
            ? spring({
                frame: Math.floor((currentSecond - wordTiming.start) * fps),
                fps,
                config: { damping: 15, stiffness: 300 },
              })
            : 1;

          return (
            <span
              key={index}
              style={{
                fontSize: 52,
                fontWeight: isActive ? 900 : 700,
                color: isActive ? brandColors.accent : "white",
                opacity: isFuture ? 0.4 : wordOpacity,
                transform: `scale(${wordScale})`,
                textShadow: isActive
                  ? "3px 3px 0 rgba(0,0,0,0.5)"
                  : "2px 2px 0 rgba(0,0,0,0.3)",
                transition: "color 0.1s ease",
              }}
            >
              {wordTiming.word}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

/**
 * CTA Scene - Clear action with urgency
 */
const CTAScene: React.FC<{
  ctaText: string;
  brandColors: { primary: string; secondary: string; accent: string };
}> = ({ ctaText, brandColors }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance animation
  const slideUp = interpolate(frame, [0, fps * 0.5], [100, 0], {
    extrapolateRight: "clamp",
  });

  const opacity = interpolate(frame, [0, fps * 0.3], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Pulse animation for urgency
  const pulse = interpolate(
    frame % (fps * 0.5),
    [0, fps * 0.25, fps * 0.5],
    [1, 1.05, 1]
  );

  // Arrow bounce
  const arrowBounce = interpolate(
    frame % fps,
    [0, fps * 0.5, fps],
    [0, -15, 0]
  );

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/* Gradient overlay */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: "50%",
          background: `linear-gradient(to top, ${brandColors.primary}, transparent)`,
        }}
      />

      {/* CTA Container */}
      <div
        style={{
          transform: `translateY(${slideUp}px) scale(${pulse})`,
          opacity,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 20,
        }}
      >
        {/* CTA Text */}
        <div
          style={{
            fontSize: 64,
            fontWeight: 900,
            color: "white",
            textAlign: "center",
            textShadow: "4px 4px 0 rgba(0,0,0,0.3)",
          }}
        >
          {ctaText}
        </div>

        {/* Arrow pointing down */}
        <div
          style={{
            fontSize: 48,
            color: brandColors.accent,
            transform: `translateY(${arrowBounce}px)`,
          }}
        >
          ↓
        </div>

        {/* "Link in bio" text */}
        <div
          style={{
            fontSize: 36,
            fontWeight: 700,
            color: brandColors.accent,
            backgroundColor: "rgba(0,0,0,0.5)",
            padding: "12px 32px",
            borderRadius: 50,
          }}
        >
          Link in bio
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Export composition config
export const TikTokAdConfig = {
  id: "TikTokAd",
  component: TikTokAd,
  ...TIKTOK_SPECS,
  defaultProps: {
    hookText: "Stop scrolling. This changes everything.",
    script: "Default script content",
    wordTimings: [
      { word: "Stop", start: 3, end: 3.3 },
      { word: "scrolling.", start: 3.3, end: 3.8 },
    ],
    brandColors: {
      primary: "#0a0a0a",
      secondary: "#1a1a1a",
      accent: "#00ff88",
    },
    ctaText: "Try it FREE",
  },
};
