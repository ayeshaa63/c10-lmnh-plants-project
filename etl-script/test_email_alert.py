"""Testing for the email_alert script."""

import pytest

from email_alert import create_message, send_email


def test_create_message():
    """Test create message with a single entry"""

    header = """<h1 style="font-weight: bold;text-decoration: underline;">Sensor Failures</h1>"""
    body = """<h3>ERROR :: PLANT 3 :: plant sensor fault :: </h3> """
    output_message = header+body
    error = "ERROR :: PLANT 3 :: plant sensor fault :: "
    assert create_message([error]) == output_message
