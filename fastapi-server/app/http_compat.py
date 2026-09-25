from flask import jsonify, redirect


def JSONResponse(content=None, status_code=200):
    return jsonify(content if content is not None else {}), status_code


def RedirectResponse(url, status_code=307):
    return redirect(url, code=status_code)