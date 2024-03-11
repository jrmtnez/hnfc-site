from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.forms import CharField
from django.forms import TextInput, Textarea
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Item, Sentence, Tweet, TwitterUser, Configuration, Triple
from .serializers import ItemSerializer, SentenceSerializer



LIST_VIEW_PAGINATE_BY = 39


# --------------------------
# --- dashboard counters ---
# --------------------------

def index(request):
    # View function for home page

    configuration_instance = Configuration.objects.get(configuration_pk=0)
    configuration_show_tweets = configuration_instance.show_tweets
    configuration_environment_type = configuration_instance.environment_type


    # dashboard counters

    items_pending_acceptance = Item.objects.filter(review_level=0, skip_validations=False).count()
    items_pending_sentence_split_validation = Item.objects.filter(review_level=2, skip_validations=False).count()
    items_pending_sentence_cw_validation = Item.objects.filter(review_level=4, skip_validations=False).count()
    items_with_sentence_cw_annotation = Item.objects.filter(review_level=5, skip_validations=False).count()
    items_pending_sentence_spo_validation = Item.objects.filter(review_level=6, skip_validations=False).count()
    items_pending_sentence_fc_validation = Item.objects.filter(review_level=7, skip_validations=False).count()
    items_with_sentence_fc_annotation = Item.objects.filter(review_level=8, skip_validations=False).count()
    items_with_fc_annotation = Item.objects.filter(review_level=9, skip_validations=False).count()

    external_items_pending_acceptance = Item.objects.filter(review_level=0, skip_validations=True).count()
    external_items_pending_sentence_split = Item.objects.filter(review_level=1, skip_validations=True).count()
    external_items_pending_cw_classification = Item.objects.filter(review_level=3, skip_validations=True).count()
    external_items_with_sentence_cw_annotation = Item.objects.filter(review_level=5, skip_validations=True).count()
    external_items_pending_fc_classification = Item.objects.filter(review_level=7, skip_validations=True).count()
    external_items_with_fc_classification = Item.objects.filter(review_level=8, skip_validations=True).count()
    external_items_with_fc_annotation = Item.objects.filter(review_level=9, skip_validations=True).count()

    total_items = Item.objects.count()

    sentences_pending_split_validation = Sentence.objects.filter(review_level=2, skip_validations=False).count()
    sentences_pending_cw_validation = Sentence.objects.filter(review_level=4, skip_validations=False).count()
    sentences_with_cw_annotation = Sentence.objects.filter(review_level=5, skip_validations=False).count()
    sentences_pending_spo_validation = Sentence.objects.filter(review_level=6, skip_validations=False).count()
    sentences_pending_fc_validation = Sentence.objects.filter(review_level=7, skip_validations=False).count()
    sentences_with_fc_annotation = Sentence.objects.filter(review_level=8, skip_validations=False).count()
    sentences_with_item_fc_annotation = Sentence.objects.filter(review_level=9, skip_validations=False).count()

    external_sentences_pending_cw_classification = Sentence.objects.filter(review_level=3, skip_validations=True).count()
    external_sentences_with_cw_annotation = Sentence.objects.filter(review_level=5, skip_validations=True).count()
    external_sentences_pending_fc_classification = Sentence.objects.filter(review_level=7, skip_validations=True).count()
    external_sentences_with_fc_classification = Sentence.objects.filter(review_level=8, skip_validations=True).count()
    external_sentences_with_item_fc_annotation = Sentence.objects.filter(review_level=9, skip_validations=True).count()

    total_sentences = Sentence.objects.count()

    tweets_pending_acceptance = Tweet.objects.filter(review_level=0).count()
    tweets_pending_cw_validation = Tweet.objects.filter(review_level=4).count()
    tweets_with_cw_annotation = Tweet.objects.filter(review_level=5).count()
    tweets_pending_fc_validation = Tweet.objects.filter(review_level=7).count()
    tweets_with_fc_annotation = Tweet.objects.filter(review_level=8).count()

    total_tweets = Tweet.objects.count()

    total_twitter_users = TwitterUser.objects.count()

    context = {
        'configuration_show_tweets': configuration_show_tweets,
        'configuration_environment_type': configuration_environment_type,

        'items_pending_acceptance': items_pending_acceptance,
        'items_pending_sentence_split_validation': items_pending_sentence_split_validation,
        'items_pending_sentence_cw_validation': items_pending_sentence_cw_validation,
        'items_with_sentence_cw_annotation': items_with_sentence_cw_annotation,
        'items_pending_sentence_spo_validation': items_pending_sentence_spo_validation,
        'items_pending_sentence_fc_validation': items_pending_sentence_fc_validation,
        'items_with_sentence_fc_annotation': items_with_sentence_fc_annotation,
        'items_with_fc_annotation': items_with_fc_annotation,
        'external_items_pending_acceptance': external_items_pending_acceptance,
        'external_items_pending_sentence_split': external_items_pending_sentence_split,
        'external_items_pending_cw_classification': external_items_pending_cw_classification,
        'external_items_with_sentence_cw_annotation': external_items_with_sentence_cw_annotation,
        'external_items_pending_fc_classification': external_items_pending_fc_classification,
        'external_items_with_fc_classification': external_items_with_fc_classification,
        'external_items_with_fc_annotation': external_items_with_fc_annotation,
        'total_items': total_items,

        'sentences_pending_split_validation': sentences_pending_split_validation,
        'sentences_pending_cw_validation': sentences_pending_cw_validation,
        'sentences_with_cw_annotation': sentences_with_cw_annotation,
        'sentences_pending_spo_validation': sentences_pending_spo_validation,
        'sentences_pending_fc_validation': sentences_pending_fc_validation,
        'sentences_with_fc_annotation': sentences_with_fc_annotation,
        'sentences_with_item_fc_annotation': sentences_with_item_fc_annotation,
        'external_sentences_pending_cw_classification': external_sentences_pending_cw_classification,
        'external_sentences_with_cw_annotation': external_sentences_with_cw_annotation,
        'external_sentences_pending_fc_classification': external_sentences_pending_fc_classification,
        'external_sentences_with_fc_classification': external_sentences_with_fc_classification,
        'external_sentences_with_item_fc_annotation': external_sentences_with_item_fc_annotation,
        'total_sentences': total_sentences,

        'tweets_pending_acceptance': tweets_pending_acceptance,
        'tweets_pending_cw_validation': tweets_pending_cw_validation,
        'tweets_with_cw_annotation': tweets_with_cw_annotation,
        'tweets_pending_fc_validation': tweets_pending_fc_validation,
        'tweets_with_fc_annotation': tweets_with_fc_annotation,
        'total_tweets': total_tweets,

        'total_twitter_users': total_twitter_users,
    }

    return render(request, 'annotate/index.html', context=context)

# -----------------------
# --- Item list views ---
# -----------------------


class ItemIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.order_by('id')


class ItemsPendingAcceptanceIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=0, skip_validations=False).order_by('-id')


class ExternalItemsPendingAcceptanceIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=0, skip_validations=True).order_by('-id')


class ItemsPendingSentenceSplitValidationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=2).order_by('id')


class ItemsPendingSentenceCWValidationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=4).order_by('id')

class ExternalItemsPendingSentenceSplitIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=1, skip_validations=True).order_by('id')

class ExternalItemsPendingCWClassificationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=3, skip_validations=True).order_by('id')


class ItemsWithSentenceCWAnnotationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=5, skip_validations=False).order_by('id')


class ExternalItemsWithSentenceCWAnnotationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=5, skip_validations=True).order_by('id')


class ItemsPendingSentenceSPOValidationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=6).order_by('id')


class ItemsPendingSentenceFCValidationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=7).order_by('id')

class ExternalItemsPendingFCClassificationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=7, skip_validations=True).order_by('id')


class ItemsWithSentenceFCAnnotationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=8).order_by('id')

class ExternalItemsWithFCClassificationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=8, skip_validations=True).order_by('id')


class ItemsWithFCAnnotationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=9, skip_validations=False).order_by('id')


class ExternalItemsWithFCAnnotationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level=9, skip_validations=True).order_by('id')


class ItemIndexTopicsView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/item_topics_index.html'
    context_object_name = 'item_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Item.objects.filter(review_level__gt=0, skip_validations=False).order_by('id')


# ---------------------------
# --- Sentence list views ---
# ---------------------------

class SentenceIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/sentence_index.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.order_by('id')


class SentencesPendingSplitValidationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/sentence_index.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.filter(review_level=2).order_by('item_id', 'new_sentence_id')


class SentencesPendingCWValidationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/sentence_index.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.filter(review_level=4).order_by('item_id', 'new_sentence_id')


class SentencesWithCWAnnotationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/sentence_index.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.filter(review_level=5, skip_validations=False).order_by('item_id', 'new_sentence_id')


class SentencesPendingSPOValidationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/cw_sentence_index.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.filter(review_level=6).order_by('item_id', 'new_sentence_id')


class SentencesPendingFCValidationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/cw_sentence_index.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.filter(review_level=7).order_by('item_id', 'new_sentence_id')


class SentencesWithFCAnnotationSentenceIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/fact-checking.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.filter(review_level=8).order_by('item_id', 'new_sentence_id')


class SentencesWithItemFCAnnotationSentenceIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/cw_sentence_index.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.filter(review_level=9, skip_validations=False).order_by('item_id', 'new_sentence_id')


class ExternalSentencesPendingCWClassificationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/sentence_index.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.filter(review_level=3, skip_validations=True).order_by('item_id', 'new_sentence_id')


class ExternalSentencesWithCWAnnotationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/sentence_index.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.filter(review_level=5, skip_validations=True).order_by('item_id', 'new_sentence_id')

class ExternalSentencesPendingFCClassificationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/cw_sentence_index.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.filter(review_level=7, skip_validations=True).order_by('item_id', 'new_sentence_id')

class ExternalSentencesWithFCClassificationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/cw_sentence_index.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.filter(review_level=8, skip_validations=True).order_by('item_id', 'new_sentence_id')


class ExternalSentencesWithItemFCAnnotationSentenceIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/cw_sentence_index.html'
    context_object_name = 'sentence_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Sentence.objects.filter(review_level=9, skip_validations=True).order_by('item_id', 'new_sentence_id')


# -----------------------
# ---Tweet list views ---
# -----------------------

class TweetIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/tweet_index.html'
    context_object_name = 'tweet_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Tweet.objects.order_by('id')


class TweetsPendingAcceptanceIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/tweet_index.html'
    context_object_name = 'tweet_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Tweet.objects.filter(review_level=0).order_by('-id')


class TweetsPendingCWValidationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/tweet_index.html'
    context_object_name = 'tweet_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Tweet.objects.filter(review_level=4).order_by('id')


class TweetsWithCWAnnotationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/tweet_index.html'
    context_object_name = 'tweet_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Tweet.objects.filter(review_level=5).order_by('id')


class TweetsPendingFCValidationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/tweet_index.html'
    context_object_name = 'tweet_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Tweet.objects.filter(review_level=7).order_by('id')


class TweetsWithFCAnnotationIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/tweet_index.html'
    context_object_name = 'tweet_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Tweet.objects.filter(review_level=8).order_by('id')


# -------------------------
# --- Triple list views ---
# -------------------------

class TripleIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'annotate/triple_index.html'
    context_object_name = 'triple_list'
    paginate_by = LIST_VIEW_PAGINATE_BY

    def get_queryset(self):
        return Triple.objects.order_by('id')



# --------------------------------------------
# --- Item detail/create/edit/delete views ---
# --------------------------------------------

class ItemDetailView0(LoginRequiredMixin, generic.DetailView):
    model = Item
    template_name = 'annotate/item_detail_0.html'


class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    model = Item
    template_name = 'annotate/item_detail.html'


class ItemCreateForm(ModelForm):
    class Meta:
        def get_labels(fields):
            labels = {}
            for field in fields:
                labels[field] = Item._meta.get_field(field).verbose_name.title()
            return labels

        model = Item
        fields = ['title', 'source_entity', 'publication_date', 'url', 'review_url', 'text', 'item_class',
                  'item_class_4', 'crawl_date', 'review_level', 'skip_validations', 'instance_type',
                  'main_topic', 'main_claim']
        labels = get_labels(fields)
        widgets = {
           'source_entity': TextInput(),
           'url': TextInput(),
           'review_url': TextInput(),

        }

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemCreateForm(request.POST)
        if form.is_valid():
            item = form.save()
            if item.skip_validations:
                if item.review_level in [0, 5, 9]:
                    return HttpResponseRedirect(reverse_lazy('annotate:ext_item_index' + str(item.review_level)))
                else:
                    return HttpResponseRedirect(reverse_lazy('annotate:index'))
            else:
                if item.review_level in [0, 2, 4, 5, 6, 7, 8, 9]:
                    return HttpResponseRedirect(reverse_lazy('annotate:item_index' + str(item.review_level)))
                else:
                    return HttpResponseRedirect(reverse_lazy('annotate:index'))
    else:
        form = ItemCreateForm(initial={'crawl_date': datetime.now})
    return render(request, 'annotate/item_create_form.html', {'form': form})


class ItemForm(ModelForm):
    source_entity = CharField(widget=TextInput())
    url = CharField(widget=TextInput())
    text = CharField(widget=Textarea())

    class Meta:
        model = Item
        fields = ['title', 'source_entity', 'url', 'url_2', 'text', 'item_class', 'item_class_4',
                  'review_level', 'url_ok', 'no_health_useless', 'skip_validations', 'instance_type',
                  'needs_revision', 'revision_reason', 'main_topic', 'main_claim']
        widgets = {
           'revision_reason': TextInput(),
           'url_2': TextInput(),
        }

@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        print(form.errors)
        if form.is_valid():
            form.save()
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            else:
                if item.skip_validations:
                    if item.prev_review_level in [0, 5, 9]:
                        return HttpResponseRedirect(reverse_lazy('annotate:ext_item_index' + str(item.prev_review_level)))
                    else:
                        return HttpResponseRedirect(reverse_lazy('annotate:index'))
                else:
                    if item.prev_review_level in [0, 2, 4, 5, 6, 7, 8, 9]:
                        return HttpResponseRedirect(reverse_lazy('annotate:item_index' + str(item.prev_review_level)))
                    else:
                        return HttpResponseRedirect(reverse_lazy('annotate:index'))
    else:
        form = ItemForm(instance=item)
    return render(request, 'annotate/item_form.html', {'form': form, 'item': item})


class ItemDelete(DeleteView):
    model = Item
    template_name = 'annotate/confirm_delete.html'
    success_url = reverse_lazy('annotate:index')


class ItemTopicsForm(ModelForm):
    class Meta:
        model = Item
        fields = ['main_topic', 'main_claim']


@login_required
def item_topics_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemTopicsForm(request.POST, instance=item)
        print(form.errors)
        if form.is_valid():
            form.save()
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            else:
                return HttpResponseRedirect(reverse_lazy('annotate:item_topics_index'))
    else:
        form = ItemForm(instance=item)
    return render(request, 'annotate/item_topics_form.html', {'form': form, 'item': item})


# ------------------------------------------------
# --- Sentence detail/create/edit/delete views ---
# ------------------------------------------------

class SentenceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Sentence
    template_name = 'annotate/sentence_detail.html'


class SentenceCreateForm(ModelForm):
    class Meta:
        def get_labels(fields):
            labels = {}
            for field in fields:
                labels[field] = Sentence._meta.get_field(field).verbose_name.title()
            return labels

        model = Sentence
        fields = ['item_id', 'new_sentence_id', 'title', 'sentence', 'review_level', 'check_worthy',
                  'health_terms', 'manually_identified_predicate']
        labels = get_labels(fields)


@login_required
def sentence_create(request):
    if request.method == 'POST':
        form = SentenceCreateForm(request.POST)
        if form.is_valid():
            sentence = form.save()
            if sentence.skip_validations:
                if sentence.review_level in [5]:
                    return HttpResponseRedirect(reverse_lazy('annotate:ext_sentence_index' + str(sentence.review_level)))
                else:
                    return HttpResponseRedirect(reverse_lazy('annotate:index'))
            else:
                if sentence.review_level in [2, 4, 5]:
                    return HttpResponseRedirect(reverse_lazy('annotate:sentence_index' + str(sentence.review_level)))
                else:
                    return HttpResponseRedirect(reverse_lazy('annotate:index'))
    else:
        form = SentenceCreateForm()
    return render(request, 'annotate/sentence_create_form.html', {'form': form})


class UpdateSentenceForm(ModelForm):
    class Meta:
        model = Sentence
        # editable fields
        fields = ['new_sentence_id', 'sentence', 'review_level', 'check_worthy', 'health_terms', 'manually_identified_predicate']
        widgets = {
           'sentence': TextInput(),
           'new_sentence_id': TextInput(),
        }


@login_required
def sentence_update(request, pk):
    sentence = get_object_or_404(Sentence, pk=pk)

    if request.method == 'POST':
        form = UpdateSentenceForm(request.POST, instance=sentence)
        if form.is_valid():
            form.save()
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            else:
                if sentence.skip_validations:
                    if sentence.prev_review_level in [5, 9]:
                        return HttpResponseRedirect(reverse_lazy('annotate:ext_sentence_index' + str(sentence.prev_review_level)))
                    else:
                        return HttpResponseRedirect(reverse_lazy('annotate:index'))
                else:
                    if sentence.prev_review_level in [2, 4, 5, 6, 7, 8, 9]:
                        return HttpResponseRedirect(reverse_lazy('annotate:sentence_index' + str(sentence.prev_review_level)))
                    else:
                        return HttpResponseRedirect(reverse_lazy('annotate:index'))
    else:
        form = UpdateSentenceForm(instance=sentence)
    return render(request, 'annotate/sentence_form.html', {'form': form, 'sentence': sentence})


# def sentence_duplicate(request, pk):
#     sentence = get_object_or_404(Sentence, pk=pk)
#     sentence.pk = None
#     sentence.save()

#     if request.method == 'POST':
#         form = UpdateSentenceForm(request.POST, instance=sentence)
#         if form.is_valid():
#             form.save()
#             if sentence.skip_validations:
#                 if sentence.prev_review_level in [5, 9]:
#                     return HttpResponseRedirect(reverse_lazy('annotate:ext_sentence_index' + str(sentence.prev_review_level)))
#                 else:
#                     return HttpResponseRedirect(reverse_lazy('annotate:index'))
#             else:
#                 if sentence.prev_review_level in [2, 4, 5, 6, 7, 8, 9]:
#                     return HttpResponseRedirect(reverse_lazy('annotate:sentence_index' + str(sentence.prev_review_level)))
#                 else:
#                     return HttpResponseRedirect(reverse_lazy('annotate:index'))
#     else:
#         form = UpdateSentenceForm(instance=sentence)
#     return render(request, 'annotate/sentence_form.html', {'form': form, 'sentence': sentence})

@login_required
def sentence_duplicate(request, pk):
    sentence = get_object_or_404(Sentence, pk=pk)
    sentence.pk = None
    sentence.save()

    if sentence.skip_validations:
        if sentence.prev_review_level in [5, 9]:
            return HttpResponseRedirect(reverse_lazy('annotate:ext_sentence_index' + str(sentence.prev_review_level)))
        else:
            return HttpResponseRedirect(reverse_lazy('annotate:index'))
    else:
        if sentence.prev_review_level in [2, 4, 5, 6, 7, 8, 9]:
            return HttpResponseRedirect(reverse_lazy('annotate:sentence_index' + str(sentence.prev_review_level)))
        else:
            return HttpResponseRedirect(reverse_lazy('annotate:index'))


class SentenceDelete(LoginRequiredMixin, DeleteView):
    model = Sentence
    template_name = 'annotate/confirm_delete.html'
    success_url = reverse_lazy('annotate:index')


# ------------------------------------------------------------------
# --- check-worthy (FR) Sentence detail/create/edit/delete views ---
# ------------------------------------------------------------------

class CWSentenceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Sentence
    template_name = 'annotate/cw_sentence_detail.html'


class CWSentenceForm(ModelForm):
    class Meta:
        model = Sentence
        # editable fields
        fields = ['review_level', 'check_worthy', 'sentence_class', 'manually_identified_predicate']


@login_required
def cw_sentence_update(request, pk):
    sentence = get_object_or_404(Sentence, pk=pk)

    if request.method == 'POST':
        form = CWSentenceForm(request.POST, instance=sentence)
        if form.is_valid():
            form.save()
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            else:
                if sentence.skip_validations:
                    if sentence.prev_review_level in [9]:
                        return HttpResponseRedirect(reverse_lazy('annotate:ext_cw_sentence_index' + str(sentence.prev_review_level)))
                    else:
                        return HttpResponseRedirect(reverse_lazy('annotate:index'))
                else:
                    if sentence.prev_review_level in [6, 7, 8, 9]:
                        return HttpResponseRedirect(reverse_lazy('annotate:cw_sentence_index' + str(sentence.prev_review_level)))
                    else:
                        return HttpResponseRedirect(reverse_lazy('annotate:index'))
    else:
        form = CWSentenceForm(instance=sentence)
    return render(request, 'annotate/cw_sentence_form.html', {'form': form, 'sentence': sentence})


# ---------------------------------------------
# --- Tweet detail/create/edit/delete views ---
# ---------------------------------------------

class TweetDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tweet
    template_name = 'annotate/tweet_detail.html'


# ----------------------------------------------
# --- Triple detail/create/edit/delete views ---
# ----------------------------------------------

class TripleForm(ModelForm):
    class Meta:
        model = Triple
        fields = ['subject', 'predicate', 'object', 'instance_type']

@login_required
def triple_update(request, pk):
    triple = get_object_or_404(Triple, pk=pk)
    if request.method == 'POST':
        form = TripleForm(request.POST, instance=triple)
        print(form.errors)
        if form.is_valid():
            form.save()
            if 'next' in request.GET:
                return HttpResponseRedirect(request.GET['next'])
            else:
                return HttpResponseRedirect(reverse_lazy('annotate:triple_index'))
    else:
        form = TripleForm(instance=triple)
    return render(request, 'annotate/triple_form.html', {'form': form, 'triple': triple})




# ------------------------------------------------------------------
# --- configuration form ---
# ------------------------------------------------------------------

class ConfigurationForm(ModelForm):
    class Meta:
        model = Configuration
        # editable fields
        fields = ['show_tweets', 'environment_type']


@login_required
def configuration_update(request, pk):
    configuration = get_object_or_404(Configuration, pk=pk)

    if request.method == 'POST':
        form = ConfigurationForm(request.POST, instance=configuration)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('annotate:index'))
    else:
        form = ConfigurationForm(instance=configuration)
    return render(request, 'annotate/configuration_form.html', {'form': form, 'configuration': configuration})


# ------------------------------------------------------------------
# --- API ---
# ------------------------------------------------------------------


class APIItemDetail(APIView):

    permission_classes = ()         # necesario para evitar error CSRF token no válido cuando el usuario ha iniciado sesión
    authentication_classes = ()     # aunque no se haya restringido el acceso a la api rest framework, si el usuario no ha iniciado
                                    # sesión sí que funciona ¿?
                                    # TODO cambiar cuando se implemente autenticación de tipo sesión

    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APISentenceDetail(APIView):

    permission_classes = ()         # necesario para evitar error CSRF token no válido cuando el usuario ha iniciado sesión
    authentication_classes = ()     # aunque no se haya restringido el acceso a la api rest framework, si el usuario no ha iniciado
                                    # sesión sí que funciona ¿?
                                    # TODO cambiar cuando se implemente autenticación de tipo sesión

    def get_object(self, pk):
        try:
            return Sentence.objects.get(pk=pk)
        except Sentence.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        sentence = self.get_object(pk)
        serializer = SentenceSerializer(sentence)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        sentence = self.get_object(pk)
        serializer = SentenceSerializer(sentence, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)