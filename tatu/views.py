import json
import os
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
        json_path = os.path.join(settings.BASE_DIR, "json/questions.json")
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                question_data = json.load(file)
                self.questions = {
                    self._normalize(q["question"]): q["answer"] 
                    for q in question_data
                }
        except FileNotFoundError:
            raise FileNotFoundError(f"json file topilmadi {json_path}")
        except json.JSONDecodeError:
            raise ValueError("file format xato")

    def _normalize(self, text: str) :
        return " ".join(text.strip().lower().split())

    def get_answer(self, question: str) -> str | None:
        question = self._normalize(question)
        return self.questions.get(question)

    def batch_get_answers(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        responses = []
        for item in questions:
            question = item.get("question", "")
            normalized_question = self._normalize(question)
            answer = self.get_answer(normalized_question) or "Javob topilmadi"
            responses.append({
                "index": item.get("index"),
                "question": question,
                "answer": answer
            })
        return responses

question_manager = QuestionManager()

@csrf_exempt
@require_http_methods(["POST"])
def search_answer(request) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
        if not isinstance(data, list):
            return JsonResponse({"error": "Input must be an array"}, status=400)

        responses = question_manager.batch_get_answers(data)
        response = JsonResponse(responses, safe=False)
        response["Access-Control-Allow-Origin"] = "https://student.fbtuit.uz"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type, Accept"
        return response
    except json.JSONDecodeError:
        return JsonResponse({"error": "json format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"xatolik: {str(e)}"}, status=500)