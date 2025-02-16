import json
import os
from functools import lru_cache
from typing import List, Dict, Any
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

class QuestionManager:
    def __init__(self):
        self.questions: Dict[str, str] = {}
        self._load_questions()

    def _load_questions(self) -> None:
        """Savollarni fayldan yuklash va keshda saqlash"""
        json_path = os.path.join(settings.BASE_DIR, "questions.json")
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                question_data = json.load(file)
                self.questions = {
                    q["question"].strip().lower(): q["answer"][0]
                    for q in question_data
                }
        except FileNotFoundError:
            raise FileNotFoundError(f"Questions file not found at {json_path}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in questions file")

    @lru_cache(maxsize=1000)
    def get_answer(self, question: str) -> str | None:
        """Savolga javob qaytarish (keshlangan)"""
        question = question.strip().lower()
        return self.questions.get(question) if question else None

    def batch_get_answer(self, questions: List[Dict[str, Any]]) -> List[str]:
        """Bir nechta savollarga javob qaytarish. Topilmagan savollarni o'tkazib yuborish"""
        responses = []
        
        for item in questions:
            question = item.get("question", "")
            answer = self.get_answer(question)
            if answer:  
                responses.append(answer)
        
        return responses if responses else ["No valid answer found"]

question_manager = QuestionManager()

@csrf_exempt
@require_http_methods(["POST"])
def search_answer(request) -> JsonResponse:
    """API endpoint for searching answer"""
    try:
        data = json.loads(request.body.decode("utf-8"))
        if not isinstance(data, list):
            return JsonResponse(
                {"error": "Input must be an array"}, 
                status=400
            )

        responses = question_manager.batch_get_answer(data)
        
       
        if not responses:
            return JsonResponse(
                {"message": "No valid questions found"}, 
                status=404
            )

        return JsonResponse(responses, safe=False)

    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON format"}, 
            status=400
        )
    except Exception as e:
        return JsonResponse(
            {"error": f"Internal server error: {str(e)}"}, 
            status=500
        )