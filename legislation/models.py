from django.db import models

class Category(models.Model):
    """Categories like C22 - Governance"""
    code = models.CharField(max_length=10)  # e.g., "C22"
    name = models.CharField(max_length=200)  # e.g., "Governance"
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['code']

class Jurisdiction(models.Model):
    """Jurisdictions like Tas, Cth"""
    code = models.CharField(max_length=10)  # e.g., "TAS", "CTH"
    name = models.CharField(max_length=100)  # e.g., "Tasmania"
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Legislation(models.Model):
    """Main legislation model"""
    TIER_CHOICES = [
        ('1', 'Tier 1'),
        ('2', 'Tier 2'),
        ('3H', 'Tier 3 High'),
        ('3L', 'Tier 3 Low'),
    ]

    # Core fields
    title = models.CharField(
        max_length=500,
        verbose_name="Obligation"  # Match Excel column name
    )
    description = models.TextField()
    tier = models.CharField(
        max_length=2,
        choices=TIER_CHOICES,
        db_index=True  # Add index for better query performance
    )
    
    # Foreign Keys
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT,
        related_name='legislations'
    )
    jurisdiction = models.ForeignKey(
        Jurisdiction, 
        on_delete=models.PROTECT,
        related_name='legislations'
    )
    
    # Owner and Administration fields
    compliance_owner = models.CharField(
        max_length=200,
        verbose_name="Compliance Owner"
    )
    business_owner = models.CharField(
        max_length=200,
        verbose_name="Process / Business Owner"
    )
    admin_department = models.CharField(
        max_length=200,
        verbose_name="Administering department",
        blank=True  # Allow empty values based on Excel analysis
    )
    administering_body = models.CharField(
        max_length=200,
        verbose_name="Administering Body",
        blank=True,  # Allow empty values based on Excel analysis
        help_text="Previously 'pe' in Excel"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_review_date = models.DateField(null=True, blank=True)
    next_review_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.jurisdiction})"
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Legislation"
        # Add indexes for commonly searched fields
        indexes = [
            models.Index(fields=['tier', 'jurisdiction']),
            models.Index(fields=['title']),
        ]

class LegislationReview(models.Model):
    """Track legislation reviews"""
    legislation = models.ForeignKey(
        Legislation,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    review_date = models.DateField()
    reviewed_by = models.CharField(max_length=200)
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"Review of {self.legislation.title} on {self.review_date}"
    
    class Meta:
        ordering = ['-review_date']