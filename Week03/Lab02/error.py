import logging
from flask import jsonify, request
from werkzeug.exceptions import HTTPException

class ProblemError(Exception):
    def __init__(self, status, title, detail=None, type_path="about:blank"):
        super().__init__(detail or title)
        self.status = status
        self.title = title
        self.detail = detail
        self.type_path = type_path


def make_problem_response(status, title, detail=None, type_path="about:blank"):
    payload = {
        "type": type_path,
        "title": title,
        "status": status,
        "detail": detail,
        "instance": request.path
    }
    response = jsonify(payload)

    response.headers["Content-Type"] = "application/problem+json"
    return response, status


def register_error_handlers(app):

    @app.errorhandler(ProblemError)
    def handle_problem_error(e):
        return make_problem_response(
            status=e.status,
            title=e.title,
            detail=e.detail,
            type_path=e.type_path
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return make_problem_response(
            status=e.code,
            title=e.name,
            detail=e.description,
            type_path="about:blank"
        )

    @app.errorhandler(Exception)
    def handle_unhandled_exception(e):
        app.logger.error("Unhandled Exception caught:", exc_info=e)

        return make_problem_response(
            status=500,
            title="Internal Server Error",
            detail="An unexpected error occurred on the server.",
            type_path="about:blank"
        )