import json
import random
import string

from django.http import HttpRequest, JsonResponse

from issues.models import Issue


def get_issues(request: HttpRequest) -> JsonResponse:
    if request.method != "GET":
        raise Exception("Only GET method is allowed")

    # issues = Issue.objects.create()
    # issues = Issue.objects.update()
    # issues = Issue.objects.get()
    # issues = Issue.objects.delete()
    issues: list[Issue] = Issue.objects.all()  # type: ignore

    results: list[dict] = [
        {
            "id": issue.id,  # type: ignore
            "title": issue.title,
            "body": issue.body,
            "senior_id": issue.senior_id,
            "junior_id": issue.junior_id,
        }
        for issue in issues
    ]

    return JsonResponse(data={"results": results})


def _random_string(length: int = 10) -> str:
    return "".join(
        [random.choice(string.ascii_letters) for i in range(length)]
    )


def create_random_issue(request: HttpRequest) -> JsonResponse:
    issue = Issue.objects.create(
        title=_random_string(20),
        body=_random_string(30),
        senior_id=1,
        junior_id=2,
    )

    result = {
        "id": issue.id,  # type: ignore
        "title": issue.title,
        "body": issue.body,
        "senior_id": issue.senior_id,
        "junior_id": issue.junior_id,
    }

    return JsonResponse(data=result)


def create_new_issue(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        raise Exception("Only POST method is allowed")
    data_ = json.loads(request.body)

    issue = Issue.objects.create(
        title=data_.get("title"),
        body=data_.get("body"),
        senior_id=1,
        junior_id=2,
    )

    result = {
        "id": issue.id,  # type: ignore
        "title": issue.title,
        "body": issue.body,
        "senior_id": issue.senior_id,
        "junior_id": issue.junior_id,
    }

    return JsonResponse(data=result)
