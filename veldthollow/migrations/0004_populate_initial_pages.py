# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED


class Migration(migrations.Migration):

    dependencies = [
        ('veldthollow', '0003_auto_20150902_0115'),
        ('blog', '0003_auto_20150725_1609'),
        ('forms', '0004_auto_20150517_0510'),

    ]

    def populate_site(app, schema_editor):
        Site = app.get_model('sites', 'Site')
        Site.objects.update_or_create(
            id=1, defaults={'domain': 'veldthollow.com', 'name': 'Veldt Hollow'})

    def populate_categories(app, schema_editor):
        BlogCategory = app.get_model('blog', 'BlogCategory')
        categories = (
            ('The Sovereign', 'the-sovereign'),
            ('Big Skies', 'big-skies'),
            ('Larder & Libations', 'larder-libations'),
            ('Long Play', 'long-play'),
            ('The Rough Hand', 'rough-hand'),
            ('Nourishment', 'nourishment'),
        )

        for title, slug in categories:
            BlogCategory.objects.update_or_create(
                slug=slug, site_id=1, defaults={'title': title})

    def populate_homepage(app, schema_editor):
        Homepage = app.get_model('veldthollow', 'Homepage')
        BlogCategory = app.get_model('blog', 'BlogCategory')
        featured_category = BlogCategory.objects.get(slug='larder-libations')
        Homepage.objects.update_or_create(
            site_id=1,
            defaults={
                'content_model': 'homepage',
                'title': 'Veldt Hollow',
                'titles': 'Veldt Hollow',
                'featured_category': featured_category,
                'slug': '/',
            })

    def populate_about_us(app, schema_editor):
        RichTextPage = app.get_model('pages', 'RichTextPage')
        RichTextPage.objects.update_or_create(
            site_id=1,
            slug='about-us',
            defaults={
                'content_model': 'richtextpage',
                'title': 'About Us',
                'titles': 'About Us',
                'status': CONTENT_STATUS_PUBLISHED,
                'content': ('<p>Veldt Hollow was founded to harness the movement of The '
                            'Middle. What is The Middle? The Middle is a cultural and '
                            'geographical identity and movement that seeks to tie together '
                            'the commonalities in The South, The Midwest and the Moutain '
                            'West. Too commonly defined as "fly over" by coastal elitists '
                            'with little experience or knowledge of out areas we love so '
                            'dearly. Our mission is to highlight the awesomeness of The '
                            'Middle by projecting, enhancing and sharing our collective '
                            'culture and historical shared experiences. Not only a '
                            'geographical identity, The Middle is about middle ground '
                            'thoughts and a balance in all things that the more enlightened '
                            'folks in these regions are believers in and wherre we hope to '
                            'take our beloved regions into the future.</p>'
                            '<p>There is a culture in these regions that is rich in history, '
                            'activities and culture and we want to highlight, promote it and '
                            'provide a voice for those of us in The Middle. This culture '
                            'isn\'t "hipster", "yuppie", "hippie" or any other easily defined '
                            'cultural stereotype, it\'s really more about a nuanced taking '
                            'of the good and a leaving behind of the bad in all things. It\'s '
                            'about balance and finding happiness in that balance as we '
                            'believe folks in The Middle tend to graviate towards.</p>'),
                'in_menus': ['3'],
                '_order': 1,
            })

    def populate_authors_list(app, schema_editor):
        RichTextPage = app.get_model('pages', 'RichTextPage')
        RichTextPage.objects.update_or_create(
            site_id=1,
            slug='authors',
            defaults={
                'content_model': 'richtextpage',
                'title': 'Authors\' Corner',
                'titles': 'Authors\' Corner',
                'status': CONTENT_STATUS_PUBLISHED,
                'content': ('<p>Our content is a combination of articles from our staff '
                            'writes and guest authors, with the goal of bringing diverse '
                            'knowledge and points of view to out topics of interest.</p>'),
                'in_menus': ['3'],
                '_order': 2,
            })

    def populate_contact_us(app, schema_editor):
        Form = app.get_model('forms', 'Form')
        form, _ = Form.objects.update_or_create(
            site_id=1,
            slug='contact-us',
            defaults={
                'content_model': 'form',
                'title': 'Contact Us',
                'titles': 'Contact Us',
                'status': CONTENT_STATUS_PUBLISHED,
                'content': ('<p>We\'d love to hear from you.</p>\n\n<p>If you\'d like to '
                            'send a message to one of our authors, check out our '
                            '<a href="/authors/">Authors\' Corner</a> instead.</p>\n'),
                'button_text': 'Send it !',
                'send_email': False,
                'in_menus': ['3'],
                'response': u'<p>Thanks for the feedback.</p>\n',
                '_order': 3,
            })
        Field = app.get_model('forms', 'Field')

        fields = [
            ('Name', 0, 1),
            ('Email', 1, 3),
            ('Regarding', 2, 1),
            ('Message', 3, 1),
        ]

        for label, order, field_type in fields:
            Field.objects.update_or_create(
                form=form,
                label=label,
                defaults={
                    'field_type': field_type,
                    '_order': order,
                })

    operations = [
        migrations.RunPython(populate_site),
        migrations.RunPython(populate_categories),
        migrations.RunPython(populate_homepage),
        migrations.RunPython(populate_about_us),
        migrations.RunPython(populate_authors_list),
        migrations.RunPython(populate_contact_us),
    ]
