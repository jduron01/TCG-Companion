from django.conf import settings
import google.generativeai as gemini

gemini.configure(api_key=settings.GEMINI_API_KEY)

def getDeckStrategy(deck):
    try:
        model = gemini.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Analyze this Pokémon TCG deck and provide strategic advice:
        {deck}

        Consider:
        - Type balance and synergy
        - Potential combos
        - Weaknesses to watch for
        - Suggested modifications
        - General play strategy

        Keep response under 500 characters.
        """
        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        return f"Could not generate strategy: {str(e)}"