from django.urls import path

from . import views

app_name = 'annotate'
urlpatterns = [
    path('', views.index, name='index'),


    # sidenav zone
    path('items/', views.ItemIndexView.as_view(), name='item_index'),
    path('items_topics/', views.ItemIndexTopicsView.as_view(), name='item_topics_index'),
    path('triples/', views.TripleIndexView.as_view(), name='triples_index'),
    path('sentences/', views.SentenceIndexView.as_view(), name='sentence_index'),
    path('tweets/', views.TweetIndexView.as_view(), name='tweet_index'),

    path('items0/', views.ItemsPendingAcceptanceIndexView.as_view(), name='item_index0'),
    path('items2/', views.ItemsPendingSentenceSplitValidationIndexView.as_view(), name='item_index2'),
    path('items4/', views.ItemsPendingSentenceCWValidationIndexView.as_view(), name='item_index4'),
    path('items5/', views.ItemsWithSentenceCWAnnotationIndexView.as_view(), name='item_index5'),
    path('items6/', views.ItemsPendingSentenceSPOValidationIndexView.as_view(), name='item_index6'),
    path('items7/', views.ItemsPendingSentenceFCValidationIndexView.as_view(), name='item_index7'),
    path('items8/', views.ItemsWithSentenceFCAnnotationIndexView.as_view(), name='item_index8'),
    path('items9/', views.ItemsWithFCAnnotationIndexView.as_view(), name='item_index9'),

    path('items/create/', views.item_create, name='item_create'),
    path('items0/<int:pk>/', views.ItemDetailView0.as_view(), name='item_detail0'),
    path('items/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('items/<int:pk>/update/', views.item_update, name='item_update'),
    path('items/<int:pk>/delete/', views.ItemDelete.as_view(), name='item_delete'),

    path('items_topics/<int:pk>/update/', views.item_topics_update, name='item_topics_update'),

    path('triples/<int:pk>/update/', views.triple_update, name='triple_update'),

    path('extitems0/', views.ExternalItemsPendingAcceptanceIndexView.as_view(), name='ext_item_index0'),
    path('extitems1/', views.ExternalItemsPendingSentenceSplitIndexView.as_view(), name='ext_item_index1'),
    path('extitems3/', views.ExternalItemsPendingCWClassificationIndexView.as_view(), name='ext_item_index3'),
    path('extitems5/', views.ExternalItemsWithSentenceCWAnnotationIndexView.as_view(), name='ext_item_index5'),
    path('extitems7/', views.ExternalItemsPendingFCClassificationIndexView.as_view(), name='ext_item_index7'),
    path('extitems8/', views.ExternalItemsWithFCClassificationIndexView.as_view(), name='ext_item_index8'),
    path('extitems9/', views.ExternalItemsWithFCAnnotationIndexView.as_view(), name='ext_item_index9'),

    path('sentences2/', views.SentencesPendingSplitValidationIndexView.as_view(), name='sentence_index2'),
    path('sentences4/', views.SentencesPendingCWValidationIndexView.as_view(), name='sentence_index4'),
    path('sentences5/', views.SentencesWithCWAnnotationIndexView.as_view(), name='sentence_index5'),
    path('sentences6/', views.SentencesPendingSPOValidationIndexView.as_view(), name='cw_sentence_index6'),
    path('sentences7/', views.SentencesPendingFCValidationIndexView.as_view(), name='cw_sentence_index7'),
    path('sentences8/', views.SentencesWithFCAnnotationSentenceIndexView.as_view(), name='cw_sentence_index8'),
    path('sentences9/', views.SentencesWithItemFCAnnotationSentenceIndexView.as_view(), name='cw_sentence_index9'),

    path('sentences/create/', views.sentence_create, name='sentence_create'),
    path('sentences/<int:pk>/', views.SentenceDetailView.as_view(), name='sentence_detail'),
    path('sentences/<int:pk>/update/', views.sentence_update, name='sentence_update'),
    path('sentences/<int:pk>/duplicate/', views.sentence_duplicate, name='sentence_duplicate'),
    path('sentences/<int:pk>/delete/', views.SentenceDelete.as_view(), name='sentence_delete'),

    path('cwsentences/<int:pk>/', views.CWSentenceDetailView.as_view(), name='cw_sentence_detail'),
    path('cwsentences/<int:pk>/update/', views.cw_sentence_update, name='cw_sentence_update'),
    path('configuration/<int:pk>/update/', views.configuration_update, name='configuration_update'),

    path('extsentences3/', views.ExternalSentencesPendingCWClassificationIndexView.as_view(), name='ext_sentence_index3'),
    path('extsentences5/', views.ExternalSentencesWithCWAnnotationIndexView.as_view(), name='ext_sentence_index5'),
    path('extsentences7/', views.ExternalSentencesPendingFCClassificationIndexView.as_view(), name='ext_sentence_index7'),
    path('extsentences8/', views.ExternalSentencesWithFCClassificationIndexView.as_view(), name='ext_sentence_index8'),
    path('extsentences9/', views.ExternalSentencesWithItemFCAnnotationSentenceIndexView.as_view(), name='ext_cw_sentence_index9'),

    path('tweets0/', views.TweetsPendingAcceptanceIndexView.as_view(), name='tweet_index'),
    path('tweets4/', views.TweetsPendingCWValidationIndexView.as_view(), name='tweet_index'),
    path('tweets5/', views.TweetsWithCWAnnotationIndexView.as_view(), name='tweet_index'),
    path('tweets7/', views.TweetsPendingFCValidationIndexView.as_view(), name='tweet_index'),
    path('tweets8/', views.TweetsWithFCAnnotationIndexView.as_view(), name='tweet_index'),

    path('tweets/<int:pk>/', views.TweetDetailView.as_view(), name='tweet_detail'),

    path('api_v1/item/<int:pk>/', views.APIItemDetail.as_view(), name='apiv1_item_detail'),
    path('api_v1/sentence/<int:pk>/', views.APISentenceDetail.as_view(), name='apiv1_sentence_detail'),

]
