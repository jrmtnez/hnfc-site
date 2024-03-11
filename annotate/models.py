from django.db import models
from django.urls import reverse

CHECKWORTHY_CLASSIFICATION = [
    ('NF', 'Not factual'),
    ('FR', 'Factual and relevant'),
    ('FNR', 'Factual and non-relevant'),
    ('NA', 'Not applicable'),
    ('FRC', 'Factual, relevant but complex'),
    ('OOI', 'Out of news item'),
]

TRUTHFULNESS_CLASSIFICATION = [
    ('F', 'False'),
    ('PF', 'Partially false'),
    ('T', 'True'),
    ('NA', 'Not applicable'),
]

INSTANCE_TYPE = [
    ('Train', 'Train'),
    ('Dev', 'Dev'),
    ('Valid', 'Validation'),
    ('Other', 'Other'),
    ('Train_Marian_FR', 'Train_Marian_FR'),
    ('Train_Marian_IT', 'Train_Marian_IT'),
    ('Train_Marian_DE', 'Train_Marian_DE'),
    ('Train_Marian_ES', 'Train_Marian_ES'),
    ('Train_MBart_ES', 'Train_MBart_ES'),
]


class Configuration(models.Model):
    configuration_pk = models.IntegerField(primary_key=True, unique=True, default=0)
    show_tweets = models.BooleanField(default=False)
    environment_type = models.CharField(max_length=100, default='', blank=True)

    def __init__(self, *args, **kwargs):
        super(Configuration, self).__init__(*args, **kwargs)

    class Meta:
        ordering = ['configuration_pk']

    def __str__(self):
        return str(self.configuration_pk)


class Item(models.Model):
    title = models.CharField(max_length=2500, default='')
    type = models.CharField(max_length=100, default='', blank=True)
    abstract = models.TextField(default='', blank=True)
    publication_date = models.DateField()
    source_entity = models.TextField(default='')
    url = models.TextField(default='')
    text = models.TextField(default='')
    review_entity = models.CharField(max_length=100, default='')
    review_url = models.TextField(default='')
    claim = models.TextField(default='', blank=True)
    original_rating = models.TextField(default='', blank=True)
    review_summary = models.TextField(default='', blank=True)
    rating = models.FloatField(default=0)
    item_class = models.IntegerField(default=0)
    crawl_date = models.DateField()
    review_level = models.IntegerField(default=0)
    url_ok = models.BooleanField(default=False)
    no_health_useless = models.BooleanField(default=False, verbose_name='No Health/Useless')
    needs_revision = models.BooleanField(default=False)
    skip_validations = models.BooleanField(default=False)
    item_class_auto = models.IntegerField(default=0)
    item_class_4_auto = models.CharField(max_length=3, choices=TRUTHFULNESS_CLASSIFICATION, default='NA')
    item_class_4 = models.CharField(max_length=3, choices=TRUTHFULNESS_CLASSIFICATION, default='NA')
    instance_type = models.CharField(max_length=25, choices=INSTANCE_TYPE, default='Other')
    revision_reason = models.TextField(default='', blank=True)
    review_url_2 = models.TextField(default='', blank=True)
    review_entity_2 = models.CharField(max_length=100, default='', blank=True)
    lang = models.CharField(max_length=10, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    main_topic = models.CharField(max_length=100, default='')
    main_claim = models.CharField(max_length=100, default='')
    instance_type_2 = models.CharField(max_length=25, choices=INSTANCE_TYPE, default='', blank=True)
    from_item_id = models.IntegerField(default=0)
    url_2 = models.TextField(default='')

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['review_level', 'skip_validations',]),
        ]

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.prev_review_level = self.review_level

    def __str__(self):
        return str(self.id) + '\t-\t' + str(self.title) + '\t-\t' + str(self.publication_date)

    def get_absolute_url(self):
        return reverse('annotate:item_detail', args=[str(self.id)])

    @property
    def get_sentences(self):
        # now we store original title in sentence 0
        # return Sentence.objects.filter(item_id=self.id, new_sentence_id__gt=0)  # greater than 0 (> is unavailable)
        return Sentence.objects.filter(item_id=self.id)


class Sentence(models.Model):
    item_id = models.IntegerField()
    rating = models.FloatField(default=0)
    needs_revision = models.BooleanField(default=False)
    check_worthy = models.CharField(max_length=3, choices=CHECKWORTHY_CLASSIFICATION, default='NF')
    sentence = models.TextField(default='', blank=True)
    title = models.CharField(max_length=2500, default='')
    metamap_extraction_xml = models.TextField(default='', blank=True)
    metamap_extraction = models.TextField(default='', blank=True)
    common_health_terms = models.CharField(max_length=2500, default='', blank=True)
    health_terms_auto = models.IntegerField(default=0)
    health_terms = models.BooleanField(default=False)
    new_sentence_id = models.IntegerField(default=0, verbose_name='Sentence Id')
    sentence_class = models.CharField(max_length=3, choices=TRUTHFULNESS_CLASSIFICATION, default='NA')
    review_level = models.IntegerField(default=0)
    check_worthy_score_auto = models.FloatField(default=0)
    check_worthy_auto = models.CharField(max_length=3, choices=CHECKWORTHY_CLASSIFICATION, default='NF')
    subject = models.CharField(max_length=2500, default='', blank=True)
    predicate = models.CharField(max_length=2500, default='', blank=True)
    object = models.CharField(max_length=2500, default='', blank=True)
    big_subject = models.CharField(max_length=2500, default='', blank=True)
    big_object = models.CharField(max_length=2500, default='', blank=True)
    subject_cuis = models.CharField(max_length=2500, default='', blank=True)
    predicate_cuis = models.CharField(max_length=2500, default='', blank=True)
    object_cuis = models.CharField(max_length=2500, default='', blank=True)
    spo_type = models.CharField(max_length=50, default='', blank=True)
    sentence_class_auto = models.CharField(max_length=3, choices=TRUTHFULNESS_CLASSIFICATION, default='NA')
    big_predicate = models.CharField(max_length=2500, default='', blank=True)
    manually_identified_predicate = models.CharField(max_length=2500, default='', blank=True)
    sentence_class_score_auto = models.FloatField(default=0)
    skip_validations = models.BooleanField(default=False)
    instance_type = models.CharField(max_length=25, choices=INSTANCE_TYPE, default='Other')
    subject_text_cuis = models.CharField(max_length=2500, default='', blank=True)
    predicate_text_cuis = models.CharField(max_length=2500, default='', blank=True)
    object_text_cuis = models.CharField(max_length=2500, default='', blank=True)
    instance_type_2 = models.CharField(max_length=25, choices=INSTANCE_TYPE, default='')
    from_sentence_id = models.IntegerField(default=0)
    from_item_id = models.IntegerField(default=0)
    predicate_not_found = models.BooleanField(default=False)


    class Meta:
        ordering = ['item_id', 'new_sentence_id']
        indexes = [
            models.Index(fields=['item_id',]),
            models.Index(fields=['review_level', 'skip_validations',]),
        ]

    def __init__(self, *args, **kwargs):
        super(Sentence, self).__init__(*args, **kwargs)
        self.prev_review_level = self.review_level

    def __str__(self):
        return str(self.item_id) + '\t-\t' + str(self.new_sentence_id) + '\t-\t' + self.sentence

    def get_review_url_verbose_name(self):
        return Item._meta.get_field("review_url").verbose_name.title()

    def get_review_url(self):
        return Item.objects.get(pk=self.item_id).review_url


class Tweet(models.Model):
    id_str = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField()
    full_text = models.TextField(default='', blank=True)
    user_id_str = models.CharField(max_length=50, default='')
    in_reply_to_status_id_str = models.CharField(max_length=50, default='', blank=True)
    in_reply_to_user_id_str = models.CharField(max_length=50, default='', blank=True)
    in_reply_to_screen_name = models.CharField(max_length=250, default='', blank=True)
    is_quote_status = models.BooleanField(default=0)
    quoted_status_id_str = models.CharField(max_length=50, default='', blank=True)
    retweet_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    favorited = models.BooleanField(default=0)
    retweeted = models.BooleanField(default=0)
    lang = models.CharField(max_length=10, default='', blank=True)
    title = models.TextField(default='', blank=True)
    type = models.CharField(max_length=50, default='', blank=True)
    crawl_date = models.DateTimeField()
    item_rating = models.FloatField(default=0)
    item_class = models.IntegerField(default=0)
    check_worthy = models.CharField(max_length=3, choices=CHECKWORTHY_CLASSIFICATION, default='NF')
    tweet_class = models.IntegerField(default=0)
    needs_revision = models.BooleanField(default=False)
    review_level = models.IntegerField(default=0)

    class Meta:
        ordering = ['id_str']
        indexes = [
            models.Index(fields=['review_level',]),
        ]

    def __init__(self, *args, **kwargs):
        super(Tweet, self).__init__(*args, **kwargs)
        self.prev_review_level = self.review_level

    def __str__(self):
        return str(self.id_str) + '\t-\t' + str(self.full_text)


class TwitterUser(models.Model):
    id_str = models.CharField(max_length=50, default='')
    name = models.TextField(default='', blank=True)
    screen_name = models.TextField(default='', blank=True)
    location = models.TextField(default='', blank=True)
    description = models.TextField(default='', blank=True)
    followers_count = models.IntegerField(default=0)
    friends_count = models.IntegerField(default=0)
    listed_count = models.IntegerField(default=0)
    favourites_count = models.IntegerField(default=0)
    statuses_count = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    verified = models.BooleanField(default=0)
    crawl_date = models.DateTimeField()

    class Meta:
        ordering = ['id_str']

    def __str__(self):
        return str(self.name) + '\t-\t' + str(self.location)


class Claim(models.Model):
    text = models.TextField(default='')
    source_entity = models.TextField(default='')
    review_entity = models.CharField(max_length=2500, default='')
    review_url = models.TextField(default='')
    title = models.CharField(max_length=2500, default='')
    original_rating = models.CharField(max_length=2500, default='', blank=True)
    type = models.CharField(max_length=2500, default='', blank=True)
    publication_date = models.DateField()
    crawl_date = models.DateField()
    item_id = models.IntegerField()

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.id) + '\t-\t' + str(self.text) + '\t-\t' + str(self.publication_date)


class Triple(models.Model):
    item_id = models.IntegerField()
    sentence_id = models.IntegerField()
    publication_date = models.DateField()
    subject = models.CharField(max_length=2500, default='', blank=True)
    predicate = models.CharField(max_length=2500, default='', blank=True)
    object = models.CharField(max_length=2500, default='', blank=True)
    sentence_class = models.CharField(max_length=3, choices=TRUTHFULNESS_CLASSIFICATION, default='NA')
    sentence_check_worthy = models.CharField(max_length=3, choices=CHECKWORTHY_CLASSIFICATION, default='NF')
    item_class_4 = models.CharField(max_length=3, choices=TRUTHFULNESS_CLASSIFICATION, default='NA')
    instance_type = models.CharField(max_length=25, choices=INSTANCE_TYPE, default='Other')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.id) + '\t-\t' + str(self.subject) + '\t-\t' + str(self.predicate) + '\t-\t' + str(self.object)