from django.utils.safestring import mark_safe


class ViewOnlyAdminMixin:
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class ImageUrlFieldsAdminMixin:
    def render_image_field(self, image_url, max_size=200):
        return mark_safe(
            f'<a href="{image_url}" target="_blank">'
            f'<img src="{image_url}" style="max-width: {max_size}px; max-height: {max_size}px;">'
            f"</a>"
        )

    def render_url_field(self, url):
        return mark_safe(f'<a href="{url}" target="_blank">{url}</a>')
