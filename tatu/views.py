import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


json_path = os.path.join(settings.BASE_DIR, "questions.json")
with open(json_path, "r", encoding="utf-8") as file:
    question_data = json.load(file)


QUESTION_DICT = {q["question"].strip().lower(): q["answer"][0] for q in question_data}

@csrf_exempt
def search_answe(request):
    if request.method == "POST":
        try:
           
            data = json.loads(request.body.decode("utf-8"))

            responses = [
                QUESTION_DICT.get(item.get("question", "").strip().lower(), "Not Found")
                for item in data
            ]

            return JsonResponse(responses, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
