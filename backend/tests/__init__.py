# Test initialization code
import unittest
from flask import Flask
from flask_testing import TestCase

from .. import create_app
from database import db


class TestBase(TestCase):
    def create_app(self):
        config_name = "testing"
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
            SECRET_KEY="mysecretkey",
            DEBUG=True,
            WTF_CSRF_ENABLED=False,
        )

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
