from .models import Item, Sentence
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = Item
    fields = ['id', 'review_level', 'crawl_date', 'skip_validations', 'title']
    # fields = '__all__'

class SentenceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Sentence
    fields = ['id', 'new_sentence_id', 'item_id', 'review_level', 'skip_validations', 'sentence']
