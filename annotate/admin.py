from django.contrib import admin

from .models import Sentence, Item, Tweet, TwitterUser


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'main_topic', 'main_claim', 'original_rating', 'title')
    list_editable = ['main_topic', 'main_claim']
    list_filter = ['review_level', 'skip_validations']
    # list_display = ('id', 'publication_date', 'review_level', 'url_ok', 'no_health_useless', 'needs_revision', 'title', 'original_rating', 'rating')
    # list_editable = ['review_level', 'url_ok', 'no_health_useless', 'needs_revision']
    # list_filter = ['review_level', 'url_ok', 'no_health_useless', 'needs_revision']

    search_fields = ['id']
    ordering = ['id']


class SentenceAdmin(admin.ModelAdmin):
    fields = (('item_id', 'new_sentence_id', 'review_level', 'needs_revision', 'instance_type'), 'title', 'sentence', ('check_worthy', 'health_terms', 'sentence_class', 'manually_identified_predicate'),
              ('check_worthy_auto', 'check_worthy_score_auto', 'sentence_class_auto', 'sentence_class_score_auto'))

    list_display = ('item_short', 'sentence_id_short', 'review_level', 'needs_revision', 'check_worthy', 'health_terms', 'big_subject', 'big_predicate', 'big_object', 'spo_type', 'manually_identified_predicate', 'sentence_class', 'sentence')

    list_editable = ['review_level', 'needs_revision', 'check_worthy', 'health_terms', 'sentence_class', 'manually_identified_predicate']

    list_filter = ['review_level', 'needs_revision', 'instance_type', 'check_worthy', 'spo_type']

    # search_fields = ['new_sentence_id']
    # search_fields = ['item_id', 'id']
    # search_fields = ['id']
    search_fields = ['=item_id']  # exact search
    ordering = ['item_id', 'new_sentence_id']

    def item_short(self, obj):
        return obj.item_id
    item_short.short_description = 'iid'

    def sentence_id_short(self, obj):
        return obj.new_sentence_id
    sentence_id_short.short_description = 'sid'


class TweetAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'item_class', 'check_worthy', 'tweet_class', 'review_level', 'full_text')

    list_editable = ['check_worthy', 'tweet_class', 'review_level']
    list_filter = ['check_worthy', 'tweet_class', 'review_level']

    search_fields = ['id']
    ordering = ['id']


class TweeterUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'name', 'screen_name', 'location', 'description', 'followers_count')

    list_filter = ['followers_count']

    search_fields = ['id']
    ordering = ['id']


admin.site.register(Item, ItemAdmin)
admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Tweet, TweetAdmin)
admin.site.register(TwitterUser, TweeterUserAdmin)
