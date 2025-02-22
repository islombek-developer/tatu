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
        self.questions: Dict[str, List[str]] = {}
        self._load_questions()

    def _load_questions(self) -> None:
        """Load questions from file and store in cache"""
        json_path = os.path.join(settings.BASE_DIR, "questions.json")
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                question_data = json.load(file)
                self.questions = {
                    q["question"].strip().lower(): q["answer"]
                    for q in question_data
                }
        except FileNotFoundError:
            raise FileNotFoundError(f"Questions file not found at {json_path}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in questions file")

    @lru_cache(maxsize=1000)
    def get_answer(self, question: str) -> List[str] | None:
        """Get answer for a question (cached)"""
        question = question.strip().lower()
        return self.questions.get(question)

    def batch_get_answers(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get answers for multiple questions. Returns list of dicts."""
        responses = []
        for item in questions:
            question = item.get("question", "").strip().lower()
            answer = self.get_answer(question) or []  # None bo'lsa, bo'sh list qaytarish
            responses.append({"question": item.get("question"), "answer": answer})
        return responses

question_manager = QuestionManager()

@csrf_exempt
@require_http_methods(["POST"])
def search_answer(request) -> JsonResponse:
    """API endpoint for searching answers"""
    try:
        data = json.loads(request.body.decode("utf-8"))
        if not isinstance(data, list):
            return JsonResponse(
                {"error": "Input must be an array"}, 
                status=400
            )

        responses = question_manager.batch_get_answers(data)
        response = JsonResponse(responses, safe=False)

        # CORS settings
        response["Access-Control-Allow-Origin"] = "https://student.fbtuit.uz"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Accept"

        return response

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
