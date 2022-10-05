"""Mixin classes for Django admin filters."""


class Collapsed:
    """State for collapsed status for filter."""

    is_collapsed = False

    @property
    def collapsed_state(self):
        """Return string for CSS stype."""
        return '' if self.is_collapsed else 'open'
