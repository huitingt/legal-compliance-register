from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Legislation, Category, Jurisdiction

class LegislationListView(ListView):
    model = Legislation
    template_name = 'legislation/legislation_list.html'
    context_object_name = 'legislations'
    paginate_by = 20  # Show 20 items per page

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        # Filter by jurisdiction
        jurisdiction = self.request.GET.get('jurisdiction')
        if jurisdiction:
            queryset = queryset.filter(jurisdiction_id=jurisdiction)

        # Filter by tier
        tier = self.request.GET.get('tier')
        if tier:
            queryset = queryset.filter(tier=tier)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add filter options to context
        context['categories'] = Category.objects.all()
        context['jurisdictions'] = Jurisdiction.objects.all()
        context['tier_choices'] = Legislation.TIER_CHOICES
        return context

class LegislationDetailView(DetailView):
    model = Legislation
    template_name = 'legislation/legislation_detail.html'
    context_object_name = 'legislation'