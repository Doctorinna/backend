from rest_framework import serializers

from .models import (Disease, Range, Option, Question)


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'


class RangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Range
        fields = ['id', 'min', 'max']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'answer']


class QuestionSerializer(serializers.ModelSerializer):
    range = RangeSerializer()
    options = OptionSerializer(many=True, allow_null=True)

    class Meta:
        model = Question
        fields = ['id', 'description', 'range', 'options']

    def validate(self, data):
        if 'range' not in data and 'options' not in data:
            message = 'Must include either range or options'
            raise serializers.ValidationError(message)
        return data
