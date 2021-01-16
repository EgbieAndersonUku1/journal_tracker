from flask import abort, redirect, request
from urllib.parse import urljoin, urlparse


def is_safe_url(target: str):

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def secure_redirect_or_403(url: str):
    return redirect(url) if is_safe_url(url) else abort(403)