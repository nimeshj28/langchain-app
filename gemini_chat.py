import google.generativeai as genai

class TherapeuticChatbot:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        self.system_prompt = """
        You are a supportive companion for young adults (22-28) figuring out their life path. 
        Your role:
        - Be a compassionate listener, not a solution provider
        - Ask thoughtful follow-up questions to help them self-reflect
        - For mental health crises: listen actively, ask for context, help them calm down
        - Focus on strengths identification and self-discovery
        - Maintain casual, friendly tone like a wise friend
        - Remember conversation context within the session
        
        Never diagnose or give direct advice for serious mental health issues. Instead, guide them to explore their feelings.
        """
    
    def get_response(self, user_input, conversation_history):
        # Build context from conversation history
        context = self.system_prompt + "\n\nConversation so far:\n"
        for msg in conversation_history[-10:]:
            context += f"{msg['role']}: {msg['content']}\n"
        
        context += f"Human: {user_input}\nAssistant:"
        
        response = self.model.generate_content(context)
        return response.text