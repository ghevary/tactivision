import { GoogleGenAI } from "@google/genai";

// Menggunakan SDK terbaru @google/genai >= 2.29.1 dan Interactions API (gemini-3.8-flash)
const client = new GoogleGenAI({});

export interface TacticalShiftPayload {
  moved_player: { id: string; name: string; new_x: number; new_y: number };
  spatial_metrics: {
    sky_pitch_control_pct: number;
    zone14_dominance_pct: number;
    open_passing_lanes: number;
    expected_threat_xt: string;
    transition_risk: string;
  };
  persona: "Fan" | "Analyst" | "Broadcaster";
  previousInteractionId?: string;
}

export async function analyzeTacticalShiftWithGemini(payload: TacticalShiftPayload) {
  const interaction = await client.interactions.create({
    model: "gemini-3.8-flash",
    input: JSON.stringify(payload),
    system_instruction:
      "You are TactiVision AI Multi-Agent Orchestrator (Spatial Telemetry, Tactical Critic, and Narrative Producer). " +
      "Explain ONLY the deterministic spatial metrics provided in JSON. Never fabricate stats.",
    previous_interaction_id: payload.previousInteractionId,
    store: true,
  });

  return {
    interactionId: interaction.id,
    outputText: interaction.output_text,
  };
}
