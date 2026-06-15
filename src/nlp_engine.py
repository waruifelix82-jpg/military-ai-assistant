import os
import json

class NLPEngine:
    def __init__(self, kb_path="data/knowledge_base.json"):
        """Initializes the NLP engine and loads the local tactical database."""
        self.kb_path = kb_path
        self.knowledge_base = self.load_knowledge_base()

    def load_knowledge_base(self):
        """Loads the JSON file containing tactical procedures."""
        if not os.path.exists(self.kb_path):
            print(f"Error: Knowledge base file not found at {self.kb_path}")
            return {}
        
        with open(self.kb_path, "r") as file:
            return json.load(file)

    def process_query(self, text):
        """Processes the text input and searches for relevant military protocols."""
        # Convert text to lowercase to make matching case-insensitive
        clean_text = text.lower().strip()
        
        # Look for keywords inside the user's spoken input
        for key, procedure in self.knowledge_base.items():
            if key in clean_text:
                return procedure
                
        # Graceful handling for queries outside military parameters
        return "Error: Query outside of tactical parameters. Please restrict questions to standard operating procedures."

# Quick local test to make sure it works independently
if __name__ == "__main__":
    # This block only runs if you run nlp_engine.py directly
    engine = NLPEngine()
    
    print("Testing NLP Engine locally...")
    test_phrase = "Can you give me the protocol for a radio check?"
    response = engine.process_query(test_phrase)
    
    print(f"Test Input: '{test_phrase}'")
    print(f"Response: {response}")