from bakery.models import BuildableModel, AutoPublishingBuildableModel

import os

class BakeryModel(BuildableModel):
    """
    An abstract class that can be mixedin to create a self building model.

    Example:

        # File: app/models.py

        from wagtail.wagtailcore.pages import Page
        from wagtail.wagtailbakery.models import BakeryModel

        class AuthorPage(Page, BakeryModel):
            bakery_views = ('app.bakery_views.AuthorPage',)
            ...

        # File: app/bakery_views.py

        from wagtail.wagtailbakery.views import BakeryView
        from . import models

        class AuthorPage(BakeryView):
            bakery_model = models.AuthorPage

        # File: project/settings.py

        BUILD_DIR = os.path.join(PROJECT_ROOT, 'baked')

    Note: 

        - Setting BAKERY_VIEWS is only required if using the "build" command.

    """

    bakery_views = []

    @property
    def build_path(self):
        return os.path.join(self.slug, 'index.html')

    @property
    def template_name(self):
        return self.template

    @property
    def detail_views(self):
        """
        Provides detail_views value for BuildableDetailView from
        bakery_views. BakeryView intends to abstract away the  
        detail/list distinction because BuildableListView is not
        needed for Wagtail Pages.
        """
        return self.bakery_views

    class Meta:
        abstract = True

class PublishingBakeryModel(BakeryModel, AutoPublishingBuildableModel):
    """
    An abstract class that can be mixedin to create a self building 
    and self publishing model which uses Celery to work in the background.
    If only background building is needed then set the following in settings:

    ALLOW_AUTO_BAKERY_PUBLISHING = False

    Example:

        # File: app/models.py

        from wagtail.wagtailcore.pages import Page
        from wagtail.wagtailbakery.models import PublishingBakeryModel

        class AuthorPage(Page, PublishingBakeryModel):
            bakery_views = ('app.bakery_views.AuthorPage',)
            ...

        # File: app/bakery_views.py

        from wagtail.wagtailbakery.views import BakeryView
        from . import models

        class AuthorPage(BakeryView):
            bakery_model = models.AuthorPage

        # File: project/settings.py

        BUILD_DIR = os.path.join(PROJECT_ROOT, 'baked')

    Note: 

        - Setting BAKERY_VIEWS is only required if using the "build" command.
    
        - PublishingBakeryModel requires that Celery be installed and configured.

    """
    
    def get_publication_status(self):
        """
        Provides publication status to AutoPublishingBuildableModel
        """
        return self.live

    class Meta:
        abstract = True
