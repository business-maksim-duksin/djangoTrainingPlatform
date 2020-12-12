class OwnerPerformCreateMixin:
    """Mixin to pass user as owner of an obj to serializer"""
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)