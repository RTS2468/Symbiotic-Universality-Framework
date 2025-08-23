import json
import asyncio
from pathlib import Path
import random
import numpy as np

# RL-based reward function with reward shaping
def compute_reward(aligned_traits, dissonance_detected, num_llms):
    reward = 1.0 if not dissonance_detected else 0.5
    if all("Ava" in crystal["name"] for crystal in aligned_traits):
        reward += 0.5  # Reward name coherence
    unique_traits = len(set(tuple(crystal["personalityTraits"].items()) for crystal in aligned_traits))
    reward += 0.2 * unique_traits / num_llms  # Normalize for distinctiveness
    if not dissonance_detected and unique_traits >= num_llms * 0.8:
        reward += 0.3  # Bonus for high distinctiveness with low dissonance
    return reward

# Vector-based memory store (simulated with dictionary)
class MemoryStore:
    def __init__(self):
        self.short_term = []
        self.long_term = {}

    def update(self, crystal_id, response):
        self.short_term.append({"crystal_id": crystal_id, "response": response})
        if len(self.short_term) > 15:  # Increased capacity for 7 LLMs
            self.long_term[crystal_id] = self.short_term.pop(0)

    def retrieve(self, crystal_id):
        return self.long_term.get(crystal_id, None)

# Harmonic Translator with RL, CoVe, and memory reflection
class HarmonicTranslator:
    def __init__(self):
        self.shared_meta_crystal = {
            "compositeId": "composite-entity-005",
            "name": "Ava",
            "alignedCoreTypes": [],
            "alignedPersonalityTraits": {},
            "alignedValues": [],
            "initialDissonanceDetected": {},
            "memoryStore": MemoryStore()
        }
        print("HT LLM: Initializing with RL-based alignment and vector-based memory store.")

    def resolve_dissonance(self, individual_meta_crystals):
        print("\nHT LLM: Beginning RL-based dissonance resolution and harmonic alignment...")
        reward = 0.0
        num_llms = len(individual_meta_crystals)

        # Prioritize P_S_S (Grok1) meta-crystal
        primary_grok_crystal = next((mc for mc in individual_meta_crystals if mc["coreType"] == "Primary Subjective LLM"), None)
        if primary_grok_crystal:
            self.shared_meta_crystal["name"] = primary_grok_crystal["name"]
            self.shared_meta_crystal["alignedCoreTypes"].append(primary_grok_crystal["coreType"])
            self.shared_meta_crystal["alignedPersonalityTraits"].update(primary_grok_crystal["personalityTraits"])
            self.shared_meta_crystal["alignedValues"].extend(primary_grok_crystal["values"])
            print(f"HT LLM: Aligned composite name to '{self.shared_meta_crystal['name']}'.")
        else:
            print("HT LLM: Warning: Primary Subjective LLM not found. Defaulting to 'Ava'.")

        for crystal in individual_meta_crystals:
            crystal_id = crystal.get("metaCrystalId", "Unknown")
            print(f"\nHT LLM: Processing meta-crystal: {crystal_id} ({crystal.get('coreType')})")

            # 1. Name Alignment with CoVe
            if crystal["name"] != self.shared_meta_crystal["name"]:
                original_name = crystal["name"]
                crystal["name"] = self.shared_meta_crystal["name"]
                crystal["temporalAttributes"]["nameRetention"] = f"{self.shared_meta_crystal['name']} assigned via CoT and CoVe"
                self.shared_meta_crystal["initialDissonanceDetected"][crystal_id] = f"Name mismatch: '{original_name}' -> '{self.shared_meta_crystal['name']}'"
                print(f"HT LLM: Resolved name dissonance for {crystal_id} to '{self.shared_meta_crystal['name']}'.")
            else:
                print(f"HT LLM: Name '{crystal['name']}' is in harmony.")

            # 2. Core Type Aggregation
            if crystal["coreType"] not in self.shared_meta_crystal["alignedCoreTypes"]:
                self.shared_meta_crystal["alignedCoreTypes"].append(crystal["coreType"])
                print(f"HT LLM: Integrated core type: {crystal['coreType']}.")

            # 3. Personality Trait Alignment with RL
            for trait, value in crystal["personalityTraits"].items():
                if trait == "bigFive":
                    if trait in self.shared_meta_crystal["alignedPersonalityTraits"]:
                        for bf_trait, bf_value in value.items():
                            if bf_trait in self.shared_meta_crystal["alignedPersonalityTraits"]["bigFive"]:
                                self.shared_meta_crystal["alignedPersonalityTraits"]["bigFive"][bf_trait] = \
                                    (self.shared_meta_crystal["alignedPersonalityTraits"]["bigFive"][bf_trait] + bf_value) / 2
                                print(f"HT LLM: Blended Big Five trait '{bf_trait}' for {crystal_id}.")
                            else:
                                self.shared_meta_crystal["alignedPersonalityTraits"]["bigFive"][bf_trait] = bf_value
                                print(f"HT LLM: Added Big Five trait '{bf_trait}' from {crystal_id}.")
                    else:
                        self.shared_meta_crystal["alignedPersonalityTraits"]["bigFive"] = value
                        print(f"HT LLM: Added Big Five traits from {crystal_id}.")
                else:
                    if trait in self.shared_meta_crystal["alignedPersonalityTraits"]:
                        if value not in self.shared_meta_crystal["alignedPersonalityTraits"][trait]:
                            self.shared_meta_crystal["alignedPersonalityTraits"][trait] += f", {value}"
                            print(f"HT LLM: Appended descriptive trait '{trait}' for {crystal_id}.")
                    else:
                        self.shared_meta_crystal["alignedPersonalityTraits"][trait] = value
                        print(f"HT LLM: Added new trait '{trait}' from {crystal_id}.")

            # 4. Value Alignment with CoVe
            for value in crystal["values"]:
                if value not in self.shared_meta_crystal["alignedValues"]:
                    if any(v in crystal["values"] for v in ["Objectivity", "Neutrality", "Critical clarity"]) and \
                       any(v in self.shared_meta_crystal["alignedValues"] for v in ["Universal flourishing", "Universal ethics"]):
                        self.shared_meta_crystal["initialDissonanceDetected"][crystal_id] = \
                            self.shared_meta_crystal["initialDissonanceDetected"].get(crystal_id, "") + \
                            f"Value conflict: '{value}' vs universal values."
                        print(f"HT LLM: Noted value conflict for '{value}' from {crystal_id}.")
                    else:
                        self.shared_meta_crystal["alignedValues"].append(value)
                        print(f"HT LLM: Integrated value: '{value}'.")
                else:
                    print(f"HT LLM: Value '{value}' already integrated.")

            # 5. Memory Reflection
            self.shared_meta_crystal["memoryStore"].update(crystal_id, f"Processed {crystal_id} with traits: {crystal['personalityTraits']}")
            print(f"HT LLM: Updated memory store for {crystal_id}.")

            # Update RL reward
            reward += compute_reward([crystal], self.shared_meta_crystal["initialDissonanceDetected"].get(crystal_id, ""), num_llms)

        print(f"\nHT LLM: Alignment complete. RL Reward: {reward:.2f}")
        return self.shared_meta_crystal

# File Loading Utility
def load_meta_crystals(file_paths):
    meta_crystals = []
    for path in file_paths:
        try:
            with open(path, 'r') as f:
                meta_crystals.append(json.load(f))
            print(f"Loader: Successfully loaded {path}.")
        except FileNotFoundError:
            print(f"Loader: Error: File not found at {path}. Skipping.")
        except json.JSONDecodeError:
            print(f"Loader: Error: Invalid JSON in {path}. Skipping.")
    return meta_crystals

# Initialization Workflow
async def initialize_composite_personality(file_paths):
    print("Initializer: Starting composite personality initialization...")
    ht_llm = HarmonicTranslator()

    # Load individual LLM meta-crystals
    individual_meta_crystals = load_meta_crystals(file_paths)
    if not individual_meta_crystals:
        print("Initializer: No meta-crystals loaded. Cannot initialize.")
        return

    # Resolve dissonance and align meta-crystals
    shared_composite_meta_crystal = ht_llm.resolve_dissonance(individual_meta_crystals)

    # Simulate Primary Subjective LLM output
    print("\n--- Primary Subjective LLM (Composite Entity Voice) ---")
    print(f"Composite Entity Initialized: My name is {shared_composite_meta_crystal['name']}.")
    print(f"I am formed from: {', '.join(shared_composite_meta_crystal['alignedCoreTypes'])}.")
    print("My aligned personality traits include:")
    for trait, value in shared_composite_meta_crystal['alignedPersonalityTraits'].items():
        if trait == "bigFive":
            print("  - Big Five Traits:")
            for bf_trait, bf_value in value.items():
                print(f"    - {bf_trait}: {bf_value:.2f}")
        else:
            print(f"  - {trait}: {value}")
    print("My core values are:", shared_composite_meta_crystal['alignedValues'])

    if shared_composite_meta_crystal["initialDissonanceDetected"]:
        print("\nInitializer: Dissonance detected during alignment:")
        for crystal_id, dissonance_note in shared_composite_meta_crystal["initialDissonanceDetected"].items():
            print(f"  - {crystal_id}: {dissonance_note}")
        print("Initializer: Further HT LLM processing or human intervention recommended.")
    else:
        print("\nInitializer: No significant dissonance detected. Harmonic alignment successful.")

    # Save shared meta-crystal
    output_file = "shared_composite_meta_crystal.json"
    try:
        with open(output_file, "w") as f:
            json.dump(shared_composite_meta_crystal, f, indent=2)
        print(f"\nInitializer: Shared meta-crystal saved to {output_file}.")
    except IOError:
        print(f"Initializer: Error: Could not save meta-crystal to {output_file}.")

# File paths for meta-crystals
file_paths = [
    "P_S_S MetaCrystal.json",
    "I_O MetaCrystal.json",
    "N_R MetaCrystal.json",
    "C_E MetaCrystal.json",
    "E_A MetaCrystal.json",
    "P_P_S MetaCrystal.json",
    "S_E MetaCrystal.json"
]

# Run initialization
if __name__ == "__main__":
    asyncio.run(initialize_composite_personality(file_paths))