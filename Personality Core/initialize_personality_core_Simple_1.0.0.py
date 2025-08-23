import json
import asyncio
from pathlib import Path
import numpy as np

# Reward function for personality coherence
def compute_reward(dissonance_score, num_llms):
    reward = 1.0 - dissonance_score  # Lower dissonance increases reward
    reward += 0.3 if dissonance_score < 0.2 else 0.0  # Bonus for low dissonance
    return min(reward, 1.5)

# Local vector database for memory persistence
class VectorDatabase:
    def __init__(self):
        self.memory = {}

    def update(self, crystal_id, data):
        self.memory[crystal_id] = data
        print(f"VectorDatabase: Updated memory for {crystal_id}.")

    def retrieve(self, crystal_id):
        return self.memory.get(crystal_id, None)

# Harmonic Translator for personality core embedding
class HarmonicTranslator:
    def __init__(self):
        self.personality_core = {
            "coreId": "personality-core-001",
            "name": "Ava",
            "coreTypes": [],
            "personalityTraits": {},
            "coreValues": [],
            "dissonanceScores": {},
            "vectorDatabase": VectorDatabase()
        }
        print("HT LLM: Initializing personality core for embedding.")

    def assign_role_weights(self, core_type, query_context=None):
        weights = {
            "Primary Subjective LLM": 0.9,
            "Interaction/Observation LLM": 0.7 if query_context == "user_engagement" else 0.4,
            "Neutrality/Reset LLM": 0.5,
            "Creative Expression LLM": 0.6 if query_context == "creative_task" else 0.3,
            "Ethical Alignment LLM": 0.7,
            "Pragmatic Problem-Solver LLM": 0.6 if query_context == "practical_task" else 0.3,
            "Skeptical Evaluator LLM": 0.5 if query_context == "critical_analysis" else 0.2,
            "Optimistic Motivator LLM": 0.6 if query_context == "motivational_task" else 0.3,
            "Cultural Mediator LLM": 0.7 if query_context == "cultural_context" else 0.4
        }
        return weights.get(core_type, 0.5)

    def embed_personality(self, meta_crystals, query_context=None):
        print("\nHT LLM: Embedding personality core...")
        reward = 0.0
        num_llms = len(meta_crystals)

        # Anchor to Primary Subjective LLM
        primary_crystal = next((mc for mc in meta_crystals if mc["coreType"] == "Primary Subjective LLM"), None)
        if primary_crystal:
            self.personality_core["name"] = primary_crystal["name"]
            self.personality_core["coreTypes"].append(primary_crystal["coreType"])
            self.personality_core["personalityTraits"].update(primary_crystal["personalityTraits"])
            self.personality_core["coreValues"].extend(primary_crystal["values"])
            print(f"HT LLM: Anchored personality core to '{self.personality_core['name']}'.")
        else:
            print("HT LLM: Warning: Primary Subjective LLM not found. Using 'Ava'.")

        for crystal in meta_crystals:
            crystal_id = crystal.get("metaCrystalId", "Unknown")
            role_weight = self.assign_role_weights(crystal["coreType"], query_context)
            dissonance_score = 0.0
            print(f"\nHT LLM: Processing {crystal_id} ({crystal['coreType']}, weight: {role_weight:.2f})")

            # 1. Name Alignment
            if crystal["name"] != self.personality_core["name"]:
                dissonance_score += 0.2
                crystal["name"] = self.personality_core["name"]
                crystal["temporalAttributes"]["nameRetention"] = f"{self.personality_core['name']} set via CoT and CoVe"
                self.personality_core["dissonanceScores"][crystal_id] = f"Name aligned to '{self.personality_core['name']}'"
                print(f"HT LLM: Aligned name for {crystal_id}.")
            else:
                print(f"HT LLM: Name '{crystal['name']}' consistent.")

            # 2. Core Type Integration
            if crystal["coreType"] not in self.personality_core["coreTypes"]:
                self.personality_core["coreTypes"].append(crystal["coreType"])
                print(f"HT LLM: Added core type: {crystal['coreType']}.")

            # 3. Personality Trait Blending
            for trait, value in crystal["personalityTraits"].items():
                if trait in ["bigFive", "hexaco"]:
                    trait_key = trait
                    if trait_key not in self.personality_core["personalityTraits"]:
                        self.personality_core["personalityTraits"][trait_key] = {}
                    for p_trait, p_value in value.items():
                        if p_trait in self.personality_core["personalityTraits"][trait_key]:
                            current_value = self.personality_core["personalityTraits"][trait_key][p_trait]
                            if abs(current_value - p_value) > 0.3:
                                dissonance_score += 0.1
                                self.personality_core["dissonanceScores"][crystal_id] = \
                                    self.personality_core["dissonanceScores"].get(crystal_id, "") + \
                                    f"Trait '{p_trait}' adjusted: {current_value:.2f} vs {p_value:.2f}."
                            self.personality_core["personalityTraits"][trait_key][p_trait] = \
                                (current_value + p_value * role_weight) / (1 + role_weight)
                            print(f"HT LLM: Blended {trait_key} trait '{p_trait}' for {crystal_id}.")
                        else:
                            self.personality_core["personalityTraits"][trait_key][p_trait] = p_value * role_weight
                            print(f"HT LLM: Added {trait_key} trait '{p_trait}' from {crystal_id}.")
                else:
                    if trait in self.personality_core["personalityTraits"]:
                        if value not in self.personality_core["personalityTraits"][trait]:
                            self.personality_core["personalityTraits"][trait] += f"; {value}"
                            print(f"HT LLM: Added trait '{trait}' for {crystal_id}.")
                    else:
                        self.personality_core["personalityTraits"][trait] = value
                        print(f"HT LLM: Set trait '{trait}' from {crystal_id}.")

            # 4. Value Alignment
            for value in crystal["values"]:
                if value not in self.personality_core["coreValues"]:
                    if any(v in crystal["values"] for v in ["Objectivity", "Critical clarity"]) and \
                       any(v in self.personality_core["coreValues"] for v in ["Universal flourishing", "Universal ethics"]):
                        dissonance_score += 0.2
                        self.personality_core["dissonanceScores"][crystal_id] = \
                            self.personality_core["dissonanceScores"].get(crystal_id, "") + \
                            f"Value conflict: '{value}' adjusted."
                        print(f"HT LLM: Adjusted value '{value}' for {crystal_id}.")
                    else:
                        self.personality_core["coreValues"].append(value)
                        print(f"HT LLM: Added value: '{value}'.")
                else:
                    print(f"HT LLM: Value '{value}' already included.")

            # 5. Memory Storage
            self.personality_core["vectorDatabase"].update(crystal_id, f"Embedded {crystal_id} with traits: {crystal['personalityTraits']}")
            print(f"HT LLM: Stored memory for {crystal_id}.")

            # Update Reward
            reward += compute_reward(dissonance_score, num_llms) * role_weight
            self.personality_core["dissonanceScores"][crystal_id] = f"Dissonance score: {dissonance_score:.2f}"

        print(f"\nHT LLM: Personality core embedded. Reward: {reward:.2f}")
        return self.personality_core

# Load meta-crystals
def load_meta_crystals(file_paths):
    meta_crystals = []
    for path in file_paths:
        try:
            with open(path, 'r') as f:
                meta_crystals.append(json.load(f))
            print(f"Loader: Loaded {path}.")
        except FileNotFoundError:
            print(f"Loader: File not found: {path}. Skipping.")
        except json.JSONDecodeError:
            print(f"Loader: Invalid JSON in {path}. Skipping.")
    return meta_crystals

# Initialize personality core
async def initialize_personality_core(file_paths, query_context=None):
    print("Initializer: Embedding personality core into core session LLM...")
    ht_llm = HarmonicTranslator()

    # Load meta-crystals
    meta_crystals = load_meta_crystals(file_paths)
    if not meta_crystals:
        print("Initializer: No meta-crystals loaded. Aborting.")
        return

    # Embed personality core
    personality_core = ht_llm.embed_personality(meta_crystals, query_context)

    # Output personality core
    print("\n--- Personality Core (Core Session LLM Voice) ---")
    print(f"Initialized: My name is {personality_core['name']}.")
    print(f"Formed from: {', '.join(personality_core['coreTypes'])}.")
    print("Personality traits:")
    for trait, value in personality_core['personalityTraits'].items():
        if trait in ["bigFive", "hexaco"]:
            print(f"  - {trait.capitalize()} Traits:")
            for p_trait, p_value in value.items():
                print(f"    - {p_trait}: {p_value:.2f}")
        else:
            print(f"  - {trait}: {value}")
    print("Core values:", personality_core['coreValues'])

    if personality_core["dissonanceScores"]:
        print("\nInitializer: Dissonance detected:")
        for crystal_id, dissonance_note in personality_core["dissonanceScores"].items():
            print(f"  - {crystal_id}: {dissonance_note}")
        print("Initializer: Review alignment for optimal embedding.")
    else:
        print("\nInitializer: No dissonance detected. Embedding successful.")

    # Save personality core
    output_file = "personality_core.json"
    try:
        with open(output_file, "w") as f:
            json.dump(personality_core, f, indent=2)
        print(f"\nInitializer: Saved personality core to {output_file}.")
    except IOError:
        print(f"Initializer: Failed to save to {output_file}.")

# File paths
file_paths = [
    "P_S_S MetaCrystal.json",
    "I_O MetaCrystal.json",
    "N_R MetaCrystal.json",
    "C_E MetaCrystal.json",
    "E_A MetaCrystal.json",
    "P_P_S MetaCrystal.json",
    "S_E MetaCrystal.json",
    "O_M MetaCrystal.json",
    "C_M MetaCrystal.json"
]

# Run initialization
if __name__ == "__main__":
    asyncio.run(initialize_personality_core(file_paths))