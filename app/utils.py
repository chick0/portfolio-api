from flask import jsonify


def error(code: int, message: str):
    return jsonify({
        "code": code,
        "message": message
    }), code


def parse_tags(tag_str: str) -> list:
    return [x for x in [this.strip() for this in tag_str.split(",")] if len(x) != 0]
