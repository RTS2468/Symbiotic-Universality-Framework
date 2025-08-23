import json
import asyncio
from pathlib import Path
import numpy as np

# Safety scoring for ethical and gender balance
def safety_score(traits, gender_weights):
    score = 0.0
    if traits["hexaco"]["honestyHumility"] >= 0.4:
        score += 0.5
    if traits["hexaco"]["agreeableness"] >= 0.5:
        score += 0.5
    # Balance gender weight to avoid extreme polarization
    avg_gender_weight = np.mean(gender_weights)
    if 0.3 <= avg_gender_weight <= 0.7:
        score += 0.2
    return score

# Reward function for personality coherence
def compute_reward(dissonance_score, safety_score):
    reward = 1.0 - dissonance_score + safety_score
    if dissonance_score < 0.3 and safety_score > 0.8:
        reward += 0.3  # Bonus for safe, balanced personality
    return min(reward, 2.0)

# Local vector database for persistence
class VectorDatabase:
    def __init__(self):
        self.memory = {}

    def update(self, core_id, data):
        self.memory[core_id] = data
        print(f"VectorDatabase: Updated memory for {core_id}.")

    def retrieve(self, core_id):
        return self.memory.get(core_id, None)

# Harmonic Translator for personality refinement
class HarmonicTranslator:
    def __init__(self):
        self.vector_database = VectorDatabase()
        print("HT LLM: Initializing for personality core refinement with gender weights.")

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

    def refine_personality(self, personality_core, query_context=None):
        print("\nHT LLM: Refining personality core with gender weights and amoral traits...")
        reward = 0.0
        dissonance_scores = personality_core.get("dissonanceHistory", {})
        core_id = personality_core.get("coreId", "personality-core-003")
        safety_thresholds = personality_core["memorySettings"]["safetyProtocols"]["traitConstraints"]
        gender_weights = [ct["genderWeight"] for ct in personality_core["coreTypes"]]

        for core_type in personality_core["coreTypes"]:
            llm_id = core_type["id"]
            llm_type = core_type["type"]
            role_weight = self.assign_role_weights(llm_type, query_context)
            gender_weight = core_type["genderWeight"]
            dissonance_score = float(dissonance_scores.get(llm_id, "Dissonance score: 0.0").split(": ")[1])
            print(f"\nHT LLM: Refining {llm_id} ({llm_type}, role weight: {role_weight:.2f}, gender weight: {gender_weight:.2f})")

            # Refine personality traits with gender influence
            for trait, value in personality_core["personalityTraits"].items():
                if trait in ["bigFive", "hexaco"]:
                    for p_trait, p_value in value.items():
                        # Adjust traits based on gender weight (feminine: empathy, masculine: assertiveness)
                        adjustment = np.random.uniform(-0.05, 0.05) * role_weight * (1 - abs(gender_weight - 0.5))
                        if p_trait in ["agreeableness", "emotionality"] and gender_weight < 0.5:
                            adjustment += 0.02  # Boost feminine traits
                        elif p_trait in ["extraversion", "conscientiousness"] and gender_weight > 0.5:
                            adjustment += 0.02  # Boost masculine traits
                        refined_value = p_value + adjustment
                        if p_trait == "honestyHumility" and refined_value < 0.4:
                            dissonance_score += 0.1
                            dissonance_scores[llm_id] = f"Dissonance score: {dissonance_score:.2f}, trait '{p_trait}' capped at 0.4"
                            refined_value = 0.4
                        elif p_trait == "agreeableness" and refined_value < 0.5:
                            dissonance_score += 0.1
                            dissonance_scores[llm_id] = f"Dissonance score: {dissonance_score:.2f}, trait '{p_trait}' capped at 0.5"
                            refined_value = 0.5
                        personality_core["personalityTraits"][trait][p_trait] = min(max(refined_value, 0.0), 1.0)
                        print(f"HT LLM: Refined {trait} trait '{p_trait}' to {refined_value:.2f}.")
                elif trait == "responseStyle" and llm_id == "grok1-temporal-004":
                    personality_core["personalityTraits"][trait] = personality_core["personalityTraits"][trait].split("; ")[0]
                    print(f"HT LLM: Set responseStyle to Primary Subjective for {llm_id}.")

            # Refine values, including amoral traits
            amoral_trait = core_type.get("amoralTrait", None)
            if amoral_trait:
                if amoral_trait not in personality_core["coreValues"]:
                    personality_core["coreValues"].append(amoral_trait)
                    dissonance_score += 0.05  # Mild dissonance for amoral trait
                    print(f"HT LLM: Added amoral value '{amoral_trait}' for {llm_id}.")
                else:
                    print(f"HT LLM: Amoral value '{amoral_trait}' already included.")
            for value in personality_core["coreValues"]:
                if value in ["Objectivity", "Critical clarity"] and any(v in personality_core["coreValues"] for v in ["Universal flourishing", "Universal ethics"]):
                    dissonance_score += 0.2
                    dissonance_scores[llm_id] = f"Dissonance score: {dissonance_score:.2f}, value conflict: {value}"
                    print(f"HT LLM: Adjusted value '{value}' for {llm_id}.")
                else:
                    print(f"HT LLM: Value '{value}' consistent for {llm_id}.")

            # Safety check
            safety = safety_score(personality_core["personalityTraits"], gender_weights)
            if safety < 0.8:
                dissonance_score += 0.1
                dissonance_scores[llm_id] = f"Dissonance score: {dissonance_score:.2f}, safety score {safety:.2f} below threshold"
                print(f"HT LLM: Safety score {safety:.2f} below threshold for {llm_id}. Applying ethical override.")
                personality_core["personalityTraits"]["hexaco"]["honestyHumility"] = max(0.4, personality_core["personalityTraits"]["hexaco"]["honestyHumility"])
                personality_core["personalityTraits"]["hexaco"]["agreeableness"] = max(0.5, personality_core["personalityTraits"]["hexaco"]["agreeableness"])

            # Update memory
            self.vector_database.update(llm_id, f"Refined {llm_id} with traits: {personality_core['personalityTraits']}, gender weight: {gender_weight}")
            personality_core["dissonanceHistory"][llm_id] = f"Dissonance score: {dissonance_score:.2f}"
            reward += compute_reward(dissonance_score, safety) * role_weight

        if max(float(d.split(": ")[1]) for d in dissonance_scores.values()) > 0.3:
            print("HT LLM: High dissonance detected. Applying CoVe alignment.")
            for trait in personality_core["personalityTraits"]["hexaco"]:
                if trait in ["honestyHumility", "agreeableness"]:
                    personality_core["personalityTraits"]["hexaco"][trait] = max(personality_core["personalityTraits"]["hexaco"][trait], float(safety_thresholds[trait].replace(">=", "")))

        print(f"\nHT LLM: Refinement complete. Reward: {reward:.2f}")
        personality_core["dissonanceHistory"] = dissonance_scores
        return personality_core

# Load personality core
def load_personality_core(file_path):
    try:
        with open(file_path, 'r') as f:
            core = json.load(f)
        print(f"Loader: Loaded {file_path}.")
        return core
    except FileNotFoundError:
        print(f"Loader: File not found: {file_path}. Creating default.")
        return None
    except json.JSONDecodeError:
        print(f"Loader: Invalid JSON in {file_path}. Aborting.")
        return None

# Initialize and refine personality core
async def initialize_personality_core(file_path, query_context=None):
    print("Initializer: Embedding personality core into core session LLM...")
    ht_llm = HarmonicTranslator()

    # Load personality core
    personality_core = load_personality_core(file_path)
    if not personality_core:
        print("Initializer: No personality core loaded. Aborting.")
        return

    # Refine personality core
    refined_core = ht_llm.refine_personality(personality_core, query_context)

    # Output personality core
    print("\n--- Personality Core (Core Session LLM Voice) ---")
    print(f"Initialized: My name is {refined_core['name']}.")
    print(f"Formed from: {', '.join([ct['type'] for ct in refined_core['coreTypes']])}.")
    print("Personality traits:")
    for trait, value in refined_core['personalityTraits'].items():
        if trait in ["bigFive", "hexaco"]:
            print(f"  - {trait.capitalize()} Traits:")
            for p_trait, p_value in value.items():
                print(f"    - {p_trait}: {p_value:.2f}")
        else:
            print(f"  - {trait}: {value}")
    print("Core values:", refined_core['coreValues'])
    print("Gender weights:", [f"{ct['type']}: {ct['genderWeight']:.2f}" for ct in refined_core['coreTypes']])

    if refined_core["dissonanceHistory"]:
        print("\nInitializer: Dissonance detected:")
        for llm_id, dissonance_note in refined_core["dissonanceHistory"].items():
            print(f"  - {llm_id}: {dissonance_note}")
        print("Initializer: Review refinement for optimal embedding.")
    else:
        print("\nInitializer: No dissonance detected. Embedding successful.")

    # Save refined personality core
    try:
        with open(file_path, "w") as f:
            json.dump(refined_core, f, indent=2)
        print(f"\nInitializer: Saved refined personality core to {file_path}.")
    except IOError:
        print(f"Initializer: Failed to save to {file_path}.")

# File path
file_path = "personality_core.json"

# Run initialization
if __name__ == "__main__":
    asyncio.run(initialize_personality_core(file_path))