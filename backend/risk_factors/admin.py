from django.contrib import admin
from . import models

models_to_register = [models.Disease, models.Question, models.Range,
                      models.Option, models.Category, models.SurveyResponse,
                      models.Result]
admin.site.register(models_to_register)
